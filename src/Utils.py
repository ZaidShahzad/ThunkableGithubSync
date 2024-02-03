import json
from github import Github, InputGitTreeElement, GithubException
import random
import string
import os
import base64
from pathlib import Path

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
    except Github.GithubException as e:
        print("Failed to authenticate with Github:", str(e))
        return None
      
def createBranchAndCommit(github, commitMessage):
    """
    Creates a new branch and commits all the files in the "out" directory to the branch.

    Args:
        github (Github): An instance of the Github class for authentication.
        commitMessage (str): The commit message for the new commit.

    Raises:
        GithubException: If there is an error creating the branch and submitting the commit.

    Returns:
        None
    """
    try:
        # Get the authenticated user
        user = github.get_user()

        # Get the repository
        repo = github.get_repo(f"{user.login}/{getGithubRepoName()}")
        
        source_branch = getGithubMainBranchName()
        source_branch_sha = repo.get_branch(source_branch).commit.sha
        
        # Generate a 4-letter unique ID
        unique_id = ''.join(random.choices(string.ascii_lowercase, k=4))

        # Create the branch name
        branch_name = f"{user.login}-devbranch-{unique_id}"

        # Commit all the files in the "out" directory
        files = os.listdir(getOutDirPath())
        commit_files = []
        for file in files:
            file_path = getOutDirPath() / file
            with open(file_path, "rb") as f:  # Open as binary for reading file content
                content = f.read()
                # Create a new InputGitTreeElement
                content = base64.b64encode(content)
                content = base64.b64decode(content).decode('utf-8')
                element = InputGitTreeElement(path=file, mode='100644', type='blob', content=content)
                commit_files.append(element)

        # Create a new tree
        tree = repo.create_git_tree(tree=commit_files, base_tree=repo.get_git_tree(source_branch_sha))

        # Create a new commit
        parent = repo.get_git_commit(source_branch_sha)
        commit = repo.create_git_commit(message=commitMessage, tree=tree, parents=[parent])

        # Update the branch to point to the new commit
        repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=commit.sha)

        print(f"Branch '{branch_name}' updated with new commit successfully.")
    except GithubException as e:
        print(f"Failed to create branch and submit commit: {e}")
        
def downloadFilesFromMainBranch(github):
    """
    Downloads files from the main branch of a GitHub repository.

    Args:
        github (Github): An instance of the `Github` class from the `PyGithub` library.

    Raises:
        GithubException: If there is an error while downloading the files.

    Returns:
        None
    """
    try:
        # Get the authenticated user
        user = github.get_user()

        # Get the repository
        repo = github.get_repo(f"{user.login}/{getGithubRepoName()}")
        
        # Get the branch
        branch = repo.get_branch(getGithubMainBranchName())
        
        # Get the tree of the branch
        tree = repo.get_git_tree(branch.commit.sha, recursive=True)
        
        # Iterate over the tree and download files
        for item in tree.tree:
            if item.type == 'blob':
                # Get the file content
                content = repo.get_git_blob(item.sha).content
                
                # Decode the content from base64
                decoded_content = base64.b64decode(content).decode('utf-8')
                
                # Create the file path
                file_path = os.path.join(getOutDirPath(), item.path)
                
                # Create the directories if they don't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Write the content to the file
                with open(file_path, 'w') as f:
                    f.write(decoded_content)
        
        print("Files downloaded successfully.")
    except GithubException as e:
        print(f"Failed to download files from branch: {e}")
