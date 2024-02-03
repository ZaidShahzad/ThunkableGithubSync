# Thunkable Github Sync
A user-friendly application designed to bridge Thunkable with GitHub, providing an intuitive GUI for managing version control of Thunkable projects. Built on top of "thunkd" open-source library, this application streamlines the process of pushing and pulling project versions between Thunkable and GitHub.

[Click to view thukd Repository](https://github.com/SupurCalvinHiggins/thunkd)

## Installation
This application requires **Python 3.11.0** 

[Install Python 3.11.0 Here](https://www.python.org/downloads/release/python-3110/)

Check your python version to make sure you have 3.11.0 installed.
```
python --version
```

Install Pip
```
pip -m ensurepip
```

Clone the repository
```
git clone <repository>
```

Install required dependencies
```
python -m pip install -r requirements.txt
```
If above does not work, manually do this
```
pip install PyGithub
```
```
pip install PyQt5
```

## Usage

### Fill Out Config.json

*MAIN_APP_THUNKABLE_SITE_URL*: This would be your main application in thunkable.

*THUNKABLE_TOKEN*: This is your thunkable token which is required for authentication with thunkable

*GITHUB_AUTH_TOKEN*: This is your github developer auth token which is required for authentication with github

*GITHUB_REPO_NAME*: This is your github repository name that you will store your main app src code

*GITHUB_MAIN_BRANCH_NAME*: This is your github repository main branch name, it's defaulting to "main". If your main branch is somehow "master", change it to "master" in the config.json

### Run Application
Run the program application with the following
```
python Program.py
```

### In The Application

#### Dev App Site Thunkable URL (TEXTBOX)
When you want to add a update to your main app in thunkable, you would click on the three dots next to your main app in your "My Projects" category, then click "Duplicate", so you can duplicate your main app. This duplicated version of your application is where you would add your update. **This input requires the website url of the duplicated version (thunkable app).**

#### Github Commit Message (TEXTBOX)
You would put the github commit message here describing the update you made.

#### Download and Push (BUTTON)
After you have put the required information in the text boxes, this button will automatically download your dev project files (The duplicated version fo your main app), then make a new branch in your repository with these downloaded files under the commit message you entered.

#### Update Main Thunkable App (BUTTON)
This button does not require any of the textboxes to be filled. It will automatically update your main thunkable app with the latest files in your main branch from your github repository.


## FAQ

### How do I find my Thunk token?
The Thunk token can be found in the "https://x.thunkable.com/" cookie under the field "thunk_token". On Chrome, this can be found via the following procedure.

1. Open a Thunkable project.
2. Press F12 to open the developer console.
3. On the top bar, click on the Application tab.
4. On the side bar, click on Cookies and then "https://x.thunkable.com/".
5. Scroll to find the "thunk_token" field. The value is your Thunk token.

### How do I find my Github Auth Token?
The Github Auth Token will be in your github account settings. Follow the instructions below.

1. Go to github.com and log into your account
2. Click your Profile Icon on the top right
3. Click "Settings"
4. Scroll down and click on "Developer Settings" on the bottom left
5. Click on "Personal access tokens" on the top left
6. Click on "Tokens (classic)"
7. Click on "Generate new token"
8. From that dropdown menu, click "Generate new token (classic)"
9. If you have 2fa setup, confirm using 2fa, if not, ignore this step
10. Name the token whatever you like in the "Note" textfield
11. Set expiration date to whatever you'd like. If it expires, you would have to re-create a new token and put that new token in the config.json.
12. Select all the scopes
13. Click the green "Generate token" button
14. Copy the token and put it in the config.json for GITHUB_AUTH_TOKEN

### Why is my code logic not working?
Since we are using thunkd, it states "Thunkable caches generated code in the project file. By default, thunkd strips this generated code when downloading to enable version control. This means that when you push to Thunkable, it cannot find the cached code. To regenerate the cached code, click through each screen on the blocks tab and everything should work fine."








