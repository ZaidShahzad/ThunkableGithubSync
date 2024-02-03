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

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from thunkd.thunkd import pull, push, getThunkableToken
import Utils
from PyQt5.QtWidgets import QGridLayout
import os

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Thunkable Github Sync')
        self.setGeometry(100, 100, 700, 400)  # Increase the size of the window

        layout = QGridLayout()

        self.label_title = QLabel('Thunkable Github Sync', self)
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold")  # Increase the font size and add bold
        layout.addWidget(self.label_title, 0, 0)

        self.label_description = QLabel('Streamlines the process of pushing and pulling project versions between Thunkable and GitHub.', self)
        self.label_description.setStyleSheet("font-size: 14px")  # Increase the font size
        layout.addWidget(self.label_description, 1, 0)

        self.config_title = QLabel('Config', self)
        self.config_title.setStyleSheet("font-size: 16px; font-weight: bold; padding-top: 20px")  # Increase the font size and add bold
        layout.addWidget(self.config_title, 2, 0)
        
        self.label_main_app_thunkable_site_url_valid = QLabel("Main App URL: Please add your app url to config.json", self)
        self.label_main_app_thunkable_site_url_valid.setStyleSheet("font-size: 14px; color: red")  # Increase the font size
        if Utils.getMainAppThunkableSiteURL() != "":
            self.label_main_app_thunkable_site_url_valid.setText("Main App URL: " + Utils.getMainAppThunkableSiteURL()[:5] + "***")  # Add a missing comma between the string and the function call
            self.label_main_app_thunkable_site_url_valid.setStyleSheet("font-size: 14px; color: green")  # Increase the font size
        layout.addWidget(self.label_main_app_thunkable_site_url_valid, 3, 0)

        self.label_thunk_token_valid = QLabel("Thunk Token: Please add your thunk token to config.json", self)
        self.label_thunk_token_valid.setStyleSheet("font-size: 14px; color: red")  # Increase the font size
        if getThunkableToken() != "":
            self.label_thunk_token_valid.setText("Thunk Token: " + getThunkableToken()[:5] + "***")  # Add a missing comma between the string and the function call
            self.label_thunk_token_valid.setStyleSheet("font-size: 14px; color: green")  # Increase the font size
        layout.addWidget(self.label_thunk_token_valid, 4, 0)

        self.label_github_auth_token_valid = QLabel("Github Auth Token: Please add your github auth token to config.json", self)
        self.label_github_auth_token_valid.setStyleSheet("font-size: 14px; color: red")  # Increase the font size
        if Utils.getGithubAuthToken() != "":
            self.label_github_auth_token_valid.setText("Github Token: " + Utils.getGithubAuthToken()[:5] + "***")  # Add a missing comma between the string and the function call
            self.label_github_auth_token_valid.setStyleSheet("font-size: 14px; color: green")  # Increase the font size
        layout.addWidget(self.label_github_auth_token_valid, 5, 0)

        self.label_github_repo_name_valid = QLabel("Github Repo Name: Please add your github repo name to config.json", self)
        self.label_github_repo_name_valid.setStyleSheet("font-size: 14px; color: red")  # Increase the font size
        if Utils.getGithubRepoName() != "":
            self.label_github_repo_name_valid.setText("Github Repo Name: " + Utils.getGithubRepoName())  # Add a missing comma between the string and the function call
            self.label_github_repo_name_valid.setStyleSheet("font-size: 14px; color: green")  # Increase the font size
        layout.addWidget(self.label_github_repo_name_valid, 6, 0)

        self.label_push_info = QLabel('Pushing Dev App To Github Information', self)
        self.label_push_info.setStyleSheet("font-size: 16px; font-weight: bold;  margin-top: 20px")  # Increase the font size and add bold
        layout.addWidget(self.label_push_info, 7, 0)

        self.label_thunkable_site_url_dev = QLabel('Dev App Site Thunkable URL (This is your dev app with the new update (feature/fix/bug/change)):', self)
        self.label_thunkable_site_url_dev.setStyleSheet("font-size: 14px")  # Increase the font size
        layout.addWidget(self.label_thunkable_site_url_dev, 8, 0)

        self.textbox_thunkable_site_url_dev = QLineEdit(self)
        self.textbox_thunkable_site_url_dev.setStyleSheet("font-size: 14px")  # Increase the font size
        layout.addWidget(self.textbox_thunkable_site_url_dev, 9, 0)

        self.label_github_commit_message = QLabel('GitHub Commit Message:', self)
        self.label_github_commit_message.setStyleSheet("font-size: 14px")  # Increase the font size
        layout.addWidget(self.label_github_commit_message, 10, 0)

        self.textbox_github_commit_message = QLineEdit(self)
        self.textbox_github_commit_message.setStyleSheet("font-size: 14px")  # Increase the font size
        layout.addWidget(self.textbox_github_commit_message, 11, 0)

        layout.rowStretch(1)  # Add spacing

        self.button_download_and_push = QPushButton('Download and Push', self)
        self.button_download_and_push.setStyleSheet("font-size: 14px; background-color: #c2410c; padding: 10px; color: white; font-weight: bold; margin-top: 30px")  # Increase the font size and set background color to green
        self.button_download_and_push.clicked.connect(self.buttonDownloadAndCommitSubmitClicked)
        layout.addWidget(self.button_download_and_push, 12, 0)
        
        self.label_first_button_instructions = QLabel("This button will automatically download your dev project files, then make a new branch in your repo with\n your files, under the commit message you entered above.", self)
        self.label_first_button_instructions.setStyleSheet("color: black; font-size: 14px; text-align: center")  # Set color to red, increase font size, and center align
        self.label_first_button_instructions.setAlignment(Qt.AlignCenter)  # Align text to center
        layout.addWidget(self.label_first_button_instructions, 13, 0)
        
        self.button_update_main_thunkable_app = QPushButton('Update Main Thunkable App', self)
        self.button_update_main_thunkable_app.setStyleSheet("font-size: 14px; background-color: #15803d; padding: 10px; color: white; font-weight: bold; margin-top: 30px")  # Increase the font size and set background color to green
        self.button_update_main_thunkable_app.clicked.connect(self.buttonUpdateMainThunkableAppSubmitClicked)
        layout.addWidget(self.button_update_main_thunkable_app, 14, 0)
        
        self.label_second_button_instructions = QLabel("This button will automatically update your main thunkable app with the latest files in your main branch\n  your github repo.", self)
        self.label_second_button_instructions.setStyleSheet("color: black; font-size: 14px; text-align: center")  # Set color to red, increase font size, and center align
        self.label_second_button_instructions.setAlignment(Qt.AlignCenter)  # Align text to center
        layout.addWidget(self.label_second_button_instructions, 15, 0)
        
        layout.rowStretch(2)  # Add spacing
        
        self.label_status_message_title = QLabel("Status", self)
        self.label_status_message_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px; text-align: center")  # Set color to red, increase font size, and center align
        self.label_status_message_title.setAlignment(Qt.AlignCenter)  # Align text to center
        layout.addWidget(self.label_status_message_title, 16, 0)
        
        self.label_status_message_description = QLabel("Nothing in the works.", self)
        self.label_status_message_description.setStyleSheet("font-size: 14px; text-align: center; margin-bottom: 10px")  # Set color to red, increase font size, and center align
        self.label_status_message_description.setAlignment(Qt.AlignCenter)  # Align text to center
        layout.addWidget(self.label_status_message_description, 17, 0)
    
        self.setLayout(layout)
        self.show()   
    
    def updateStatusMessage(self, status, text):
        """
        Update the status message description based on the given status and text.

        Args:
            status (str): The status of the message. Possible values are "success", "error", or "working".
            text (str): The text to be displayed in the status message description.

        Returns:
            None
        """
        if status == "success":
            self.label_status_message_description.setStyleSheet("font-size: 14px; text-align: center; margin-bottom: 10px; color: green")
            self.label_status_message_description.setText(text)
        elif status == "error":
            self.label_status_message_description.setStyleSheet("font-size: 14px; text-align: center; margin-bottom: 10px; color: red")
            self.label_status_message_description.setText(text)
        elif status == "working":
            self.label_status_message_description.setStyleSheet("font-size: 14px; text-align: center; margin-bottom: 10px; color: #b45309")
            self.label_status_message_description.setText(text)

    def buttonDownloadAndCommitSubmitClicked(self):
        """
        Downloads all files from the dev branch to the "out" directory,
        creates a new branch, and commits the files to the branch.

        This method requires the following inputs:
        - thunkable_site_url_dev: The URL of the Thunkable site in the dev branch.
        - github_commit_message: The commit message for the GitHub commit.

        If any of the required inputs are empty, an error message is displayed.

        After successfully creating the branch and committing the files,
        a success message is displayed.

        Returns:
        None
        """
        
        if Utils.isConfigDataMissing():
            self.updateStatusMessage("error", "Please fill in all fields in the config.json file.")
            return
        
        self.updateStatusMessage("working", "Working on it...")
        
        # Get the values from the textboxes
        thunkable_site_url_dev = self.textbox_thunkable_site_url_dev.text()
        github_commit_message = self.textbox_github_commit_message.text()
        
        # Check if the values are empty
        if not all([thunkable_site_url_dev, github_commit_message]):
            self.updateStatusMessage("error", "Please fill in all fields.")
            return
        
        # Get the project ID from the URL
        devProjectID = Utils.getProjectIDFromURL(thunkable_site_url_dev)
        
        # Authenticate with Github
        github = Utils.authenticateWithGithub()
        
        # Download all files from the dev branch to the "out" directory
        pull(devProjectID, Utils.getOutDirPath(), True, True)
        
        # Create a new branch and commit the files
        Utils.createBranchAndCommit(github, github_commit_message)
        self.updateStatusMessage("success", "Successfully Created Branch and Committed Files, Completed!")
        
    def buttonUpdateMainThunkableAppSubmitClicked(self):
        """
        This method handles the button click event for updating the main Thunkable app.

        It performs the following steps:
        1. Authenticates with GitHub.
        2. Downloads all files from the main branch to the "out" directory.
        3. Retrieves the main app project ID.
        4. Pushes the downloaded files from the main branch to the main app in Thunkable.

        Args:
            self: The current instance of the class.

        Returns:
            None
        """
        
        if Utils.isConfigDataMissing():
            self.updateStatusMessage("error", "Please fill in all fields in the config.json file.")
            return
        
        # Authenticate with Github
        github = Utils.authenticateWithGithub()
        
        # Download all files from the main branch to the "out" directory
        Utils.downloadFilesFromMainBranch(github)
        print("Downloaded files from the main branch.")
        
        # Get main app project ID
        mainProjectID = Utils.getProjectIDFromURL(Utils.getMainAppThunkableSiteURL())
        
        # Push the downloaded files from main branch to the main app in thunkable
        push(mainProjectID, Utils.getOutDirPath(), True)
        self.updateStatusMessage("success", "Successfully Pushed Main Branch Files to Main Thunkable App.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    out_dir = Utils.getOutDirPath()
    os.makedirs(out_dir, exist_ok=True)
    sys.exit(app.exec_())
