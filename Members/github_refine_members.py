import os
import csv
from datetime import datetime
import pytz

import requests
import base64

# Setze diese Variablen mit deinen Informationen
WORKFLOW_TOKEN = os.getenv('WORKFLOW_TOKEN')  # Stelle sicher, dass du dein Token sicher speicherst
REPO_OWNER = 'SuIT-pub'
REPO_NAME = 'Mind-the-School'
FILE_PATH = 'game/members copy.csv'
COMMIT_MESSAGE = 'updated members.csv'

def get_file_sha(file_path, repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    response = requests.get(url, headers={'Authorization': f'token {WORKFLOW_TOKEN}'})
    response.raise_for_status()
    return response.json()['sha']

def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def update_file_content(file_path, new_content, sha, repo_owner, repo_name, commit_message):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }
    response = requests.put(url, json=data, headers={'Authorization': f'token {WORKFLOW_TOKEN}'})
    response.raise_for_status()
    return response.json()

def main():
    # Hole den aktuellen SHA-Wert der Datei
    sha = get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME)

    # Lese die aktuelle Datei und modifiziere den Inhalt
    current_content = get_file_content(FILE_PATH)
    new_content = current_content + '\nNeue Zeile hinzugefügt durch Skript.'

    # Update die Datei im Repository
    update_file_content(FILE_PATH, new_content, sha, REPO_OWNER, REPO_NAME, COMMIT_MESSAGE)
    print('Datei erfolgreich aktualisiert.')

if __name__ == '__main__':
    main()