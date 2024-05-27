import os
import csv
from datetime import datetime
import time
import pytz

import requests
import base64
import json
import git

# Setze diese Variablen mit deinen Informationen
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Stelle sicher, dass du dein Token sicher speicherst
CLONE_DIR = '/sandbox'
REPO_URL = 'https://github.com/SuIT-pub/Mind-the-School.git'
REPO_OWNER = 'SuIT-pub'
REPO_NAME = 'Mind-the-School'
FILE_PATH = 'game/members copy.csv'
COMMIT_MESSAGE = 'updated members.csv'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}', 
    'Accept': 'application/vnd.github.v3+json'
    }

def main():
    
    # Clone the repository
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)
    repo = git.Repo.clone_from(REPO_URL, CLONE_DIR)

    # Path to the file in the local clone
    file_path = os.path.join(CLONE_DIR, FILE_PATH)

    # Modify the file
    with open(file_path, 'w') as file:
        file.write("New file content here")

    # Add the file to the staging area
    repo.index.add([file_path])

    # Commit the changes
    repo.index.commit(COMMIT_MESSAGE)

    # Push the changes
    origin = repo.remote(name='origin')
    origin.push()


main()