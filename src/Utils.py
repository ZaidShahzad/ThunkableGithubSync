"""
MIT License

Copyright (c) 2024 Zaid Shahzad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from github import Github, InputGitTreeElement, GithubException
import random
import string
import os
import base64
from pathlib import Path
import mimetypes
import chardet

def getOutDirPath():
    """
    Returns the path to the 'out' directory.
    """
    return Path.cwd() / 'out'

def getProjectIDFromURL(url):
    """
    Extracts the project ID from a given URL.

    Parameters:
    url (str): The URL of the project.

    Returns:
    str: The project ID extracted from the URL.
    """
    parts = url.split('/')
    project_id = parts[4]
    return project_id

def getGithubAuthToken():
    """
    Retrieves the GitHub authentication token from the config file.

    Returns:
        str: The GitHub authentication token.
    """
    with open('config.json') as f:
        config_data = json.load(f)
    return config_data['GITHUB_AUTH_TOKEN']

def getGithubRepoName():
    """
    Retrieves the GitHub repository name from the config file.

    Returns:
        str: The GitHub repository name.
    """
    with open('config.json') as f:
        config_data = json.load(f)
    return config_data['GITHUB_REPO_NAME']

def getGithubMainBranchName():
    """
    Retrieves the name of the main branch from the 'config.json' file.

    Returns:
        str: The name of the main branch.
    """
    with open('config.json') as f:
        config_data = json.load(f)
    return config_data['GITHUB_MAIN_BRANCH_NAME']

def getMainAppThunkableSiteURL():
    """
    Retrieves the main app Thunkable site URL from the config file.

    Returns:
        str: The main app Thunkable site URL.
    """
    with open('config.json') as f:
        config_data = json.load(f)
    return config_data['MAIN_APP_THUNKABLE_SITE_URL']

def setProjectNameInMetaDataFile(project_name):
    """
    Sets the project name in the metadata file.

    Args:
        project_name (str): The new project name.

    Returns:
        None
    """
    # Load the JSON file
    json_file_path = os.path.join(getOutDirPath(), 'meta.json') 
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Modify the "projectName" field
    data['data']['project']['projectName'] = project_name

    # Save the modified JSON back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def isConfigDataMissing():
    """
    Checks if the config file is missing or if any of the required fields are missing.

    Returns:
        bool: True if the config file is missing or if any of the required fields are missing, False otherwise.
    """
    try:
        with open('config.json') as f:
            config_data = json.load(f)
        if 'GITHUB_AUTH_TOKEN' not in config_data or 'GITHUB_REPO_NAME' not in config_data or 'GITHUB_MAIN_BRANCH_NAME' not in config_data or 'MAIN_APP_THUNKABLE_SITE_URL' not in config_data:
            return True
        if '' in config_data.values():
            return True
        return False
    except FileNotFoundError:
        return True
  
  
def authenticateWithGithub():
    """
    Authenticates with Github using the provided authentication token (in config.json).
    
    Returns:
        An instance of the Github class if authentication is successful, None otherwise.
    """
    try:
        github = Github(getGithubAuthToken())
      
        user = github.get_user()
      
        print("Authenticated with Github as:", user.login)
        return github
    except GithubException as e:
        print("Failed to authenticate with Github:", str(e))
        return None
      
def createBranchAndCommit(github, repo_name, commitMessage):
    """
    Creates a new branch and commits all the files in the "out" directory to the "src" directory in the specified repository.

    Args:
        github (Github): An instance of the Github class for authentication.
        repo_name (str): The name of the repository to operate on.
        commitMessage (str): The commit message for the new commit.

    Raises:
        GithubException: If there is an error creating the branch and submitting the commit.

    Returns:
        None
    """
    try:
        # Get the repository by searching for the repository by name
        repo = None
        
        user = github.get_user()
        for userRepo in user.get_repos():
            if(userRepo.name == repo_name):
                repo = userRepo
        
        if repo is None:
            print(f"Repository '{repo_name}' not found.")
            return
        
        source_branch = getGithubMainBranchName()
        source_branch_sha = repo.get_branch(source_branch).commit.sha
        
        # Generate a 4-letter unique ID
        unique_id = ''.join(random.choices(string.ascii_lowercase, k=4))

        # Create the branch name
        branch_name = f"{repo.owner.login}-devbranch-{unique_id}"

        # Commit all the files in the "out" directory to the "src" directory in the branch
        files = os.listdir(getOutDirPath())
        commit_files = []
        for file in files:
            file_path = getOutDirPath() / file
            with open(file_path, "rb") as f:
                content = f.read()
                content = base64.b64encode(content)
                content = base64.b64decode(content).decode('utf-8')
                src_file_path = f"src/{file}"
                element = InputGitTreeElement(path=src_file_path, mode='100644', type='blob', content=content)
                commit_files.append(element)
                
        tree = repo.create_git_tree(tree=commit_files, base_tree=repo.get_git_tree(source_branch_sha))
        parent = repo.get_git_commit(source_branch_sha)
        commit = repo.create_git_commit(message=commitMessage, tree=tree, parents=[parent])
        repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=commit.sha)

        print(f"Branch '{branch_name}' updated with new commit successfully.")
    except GithubException as e:
        print(f"Failed to create branch and submit commit in repository '{repo_name}': {e}")
        
def downloadFilesFromMainBranch(github, repo_name):
    """
    Downloads files from the 'src' directory in the main branch of a GitHub repository.

    Args:
        github (Github): An instance of the `Github` class from the `PyGithub` library.

    Raises:
        GithubException: If there is an error while downloading the files.

    Returns:
        None
    """
    try:
        # Get the repository by searching for it by name
        repo = None
        user = github.get_user()
        for userRepo in user.get_repos():
            if userRepo.name == repo_name:
                repo = userRepo
                break

        if repo is None:
            print(f"Repository '{repo_name}' not found.")
            return
        
        # Get the branch
        branch_name = 'main'  # Change if necessary
        branch = repo.get_branch(branch_name)
        
        # Get the tree of the branch, targeting the 'src' directory
        tree = repo.get_git_tree(branch.commit.sha, recursive=True).tree
        src_items = [item for item in tree if item.path.startswith('src/') and (item.path.endswith('.json') or item.path.endswith('.xml'))]
        
        # Iterate over filtered items and download files
        for item in src_items:
            # Get the file content
            content = repo.get_git_blob(item.sha).content
            
            # Check the MIME type
            mime_type, _ = mimetypes.guess_type(item.path)
            text_file_types = {'application/json', 'text/xml'}
            
            # Remove 'src/' from the path for local storage
            local_path = item.path[4:]
            file_path = os.path.join(getOutDirPath(), local_path)  # Adjust output_dir to your desired path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if mime_type in text_file_types:
                content_bytes = base64.b64decode(content)
                
                # Detect encoding
                detected_encoding = chardet.detect(content_bytes)['encoding']

                if detected_encoding:
                    try:
                        # Decode using detected encoding
                        decoded_content = content_bytes.decode(detected_encoding)
                        # Write to the file
                        with open(file_path, 'w') as f:
                            f.write(decoded_content)
                    except UnicodeDecodeError as e:
                        print(f"Failed to decode content for {item.path}: {e}")
                        continue
                else:
                    continue
            else:
                # Write binary content directly
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(content))

        print("Files from 'src' directory downloaded successfully.")

    except GithubException as e:
        print(f"Failed to download files from 'src' directory: {e}")