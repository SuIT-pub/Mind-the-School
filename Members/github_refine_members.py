import os
import csv
from datetime import datetime
import time
import pytz

import requests
import base64
import json

# Setze diese Variablen mit deinen Informationen
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Stelle sicher, dass du dein Token sicher speicherst
REPO_OWNER = 'SuIT-pub'
REPO_NAME = 'Mind-the-School'
FILE_PATH = 'game/members_copy.csv'
COMMIT_MESSAGE = 'updated members.csv'
GITHUB_HEADER = {
    'Authorization': f'token {GITHUB_TOKEN}', 
    'Accept': 'application/vnd.github.v3+json'
    }

PATREON_TOKEN = os.getenv('PATREON_TOKEN')
PATREON_HEADER = {
    'Authorization': f'Bearer {PATREON_TOKEN}',
}

def get_file_sha(file_path, repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    response = requests.get(url, headers=GITHUB_HEADER)
    response.raise_for_status()
    return response.json()['sha']

def update_file_content(file_path, new_content, sha, repo_owner, repo_name, commit_message):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    encoded_content = base64.b64encode(new_content.encode()).decode()
    data = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha
    }
    response = requests.put(url, json=data, headers=GITHUB_HEADER)
    # response.raise_for_status()
    return response.json()

def get_patreon_data():
    url = 'https://www.patreon.com/api/oauth2/v2/campaigns/10492412/members'
    params = {
        'include': 'currently_entitled_tiers',
        'fields[member]': 'full_name,patron_status'
    }
    response = requests.get(url, headers=PATREON_HEADER, params=params)
    response.raise_for_status()
    print(response.json())
    return response.json()

def main():
    # Hole den aktuellen SHA-Wert der Datei
    sha = get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME)
    
    get_patreon_data()

    # Hole den neuesten SHA-Wert der Datei
    latest_sha = get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME)
    
    # Überprüfe, ob der SHA-Wert aktualisiert wurde
    if sha != latest_sha:
        print('Der SHA-Wert hat sich geändert. Aktualisiere den SHA-Wert und versuche es erneut.')
        sha = latest_sha
    else:
        # Update die Datei im Repository
        update_file_content(FILE_PATH, "test", sha, REPO_OWNER, REPO_NAME, COMMIT_MESSAGE)
        print('Datei erfolgreich aktualisiert.')

main()