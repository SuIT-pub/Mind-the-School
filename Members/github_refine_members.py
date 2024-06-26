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
FILE_PATH = 'game/members.csv'
COMMIT_MESSAGE = 'updated members.csv'
GITHUB_HEADER = {
    'Authorization': f'token {GITHUB_TOKEN}', 
    'Accept': 'application/vnd.github.v3+json'
    }

PATREON_BLACKLIST = os.getenv('PATREON_BLACKLIST')
PATREON_ALIAS = os.getenv('PATREON_ALIAS')

PATREON_TOKEN = os.getenv('PATREON_TOKEN')
PATREON_HEADER = {
    'authorization': f'Bearer {PATREON_TOKEN}',
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

class Member:
    def __init__(self, name: str, tier: str):
        self.name = name
        self.alias = ''
        self.blacklist = False
        self.tier = tier

    def __str__(self):
        if self.blacklist:
            return '*blacklisted*;' + self.tier
        if self.alias != '':
            return '*alias*' + self.alias + ';' + self.tier
        return self.name.strip() + ';' + self.tier

    def set_blacklist(self, is_blacklisted: bool):
        self.blacklist = is_blacklisted

    def set_alias(self, alias: str):
        self.alias = alias

def get_patreon_data():
    url = 'https://www.patreon.com/api/oauth2/v2/campaigns/10492412/members'
    params = {
        'include': 'currently_entitled_tiers',
        'fields[member]': 'full_name,patron_status'
    }
    members_data = []

    while True:
        response = requests.get(url, headers=PATREON_HEADER, params=params)
        response.raise_for_status()
        data = response.json()

        for member in data['data']:
            members_data.append(member)

        if 'links' in data.keys() and 'next' in data['links'].keys():
            url = data['links']['next']
        else:
            break

    blacklist = PATREON_BLACKLIST.split("\r\n")
    alias = PATREON_ALIAS.split("\r\n")

    members = {}

    for member in members_data:
        patreon_status = member['attributes']['patron_status']
        if patreon_status != 'active_patron':
            continue
        tier = "free"
        for entitlement in member['relationships']['currently_entitled_tiers']['data']:
            if entitlement['id'] == '10070150' and tier == 'free':
                tier = 'Student'
            elif entitlement['id'] == '10070157':
                tier = 'Teacher'
        
        name = member['attributes']['full_name']

        members[name] = Member(name, tier)

    for blacklisted_name in blacklist:
        if blacklisted_name in members:
            members[blacklisted_name].set_blacklist(True)

    for alias_name in alias:
        name, alias = alias_name.split(";")
        if name in members:
            members[name].set_alias(alias)

    filtered_names = []
    for member in sorted(list(members.values()), key=lambda x: x.name):
        filtered_names.append(str(member).strip())

    cet = pytz.timezone('CET')
    current_time = datetime.now(cet)

    # Write current date and time to the file
    output = 'Last updated: ' + current_time.strftime('%d %B, %Y - %H:%M') + ' CET\n'
    trimmed_output = ''

    for name in filtered_names:
        output += name.strip() + '\n'
        trimmed_output += name.strip() + '\n'

    print(output)

    return output, trimmed_output

def is_different(old_content: str) -> bool:
    try:
        response = requests.get('https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/master/game/members.csv')
        members = response.text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        members = ""
        print('Failed Download')
        exit()
    members = members.split("\n")
    del members[0]
    members = "\n".join(members)
    print('members:' + members)
    return old_content != members

def main():
    # Hole den aktuellen SHA-Wert der Datei
    sha = get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME)
    
    output, trimmed_output = get_patreon_data()

    if not is_different(trimmed_output):
        print("Member-list is unchanged. Stopping operation.")
        return

    # Hole den neuesten SHA-Wert der Datei
    latest_sha = get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME)
    
    # Überprüfe, ob der SHA-Wert aktualisiert wurde
    if sha != latest_sha:
        print('Der SHA-Wert hat sich geändert. Aktualisiere den SHA-Wert und versuche es erneut.')
        sha = latest_sha
    
    # Update die Datei im Repository
    update_file_content(FILE_PATH, output, sha, REPO_OWNER, REPO_NAME, COMMIT_MESSAGE)
    print('Datei erfolgreich aktualisiert.')

main()