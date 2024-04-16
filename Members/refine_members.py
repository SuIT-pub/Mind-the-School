import os
import csv

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
        return self.name + ';' + self.tier

    def set_blacklist(self, is_blacklisted: bool):
        self.blacklist = is_blacklisted

    def set_alias(self, alias: str):
        self.alias = alias

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Define the folder path for the game folder
game_folder = os.path.join(parent_dir, 'game')

# Create the game folder if it doesn't exist
if not os.path.exists(game_folder):
    os.makedirs(game_folder)

# Get a list of all CSV files in the current directory with 'Members' in the filename
csv_files = [file for file in os.listdir(current_dir) if file.endswith('.csv') and 'Members' in file]
# Sort the CSV files by modification time and get the youngest file
youngest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(current_dir, x)))

print('Use ' + youngest_file + ' as the source file.')
# Read the names from the second column onwards of the youngest file, ignoring the first row
names = {}

with open(os.path.join(current_dir, youngest_file), 'r') as file:
    csv_reader = csv.reader(file)
    # next(csv_reader)  # Skip the first row (header)
    name_index = 0
    tier_index = 10
    for i, row in enumerate(csv_reader):
        if i == 0:
            name_index = row.index('Name')
            tier_index = row.index('Tier')
        name = row[name_index].strip()
        tier = row[tier_index].strip()
        print(name + ", " + tier)
        names[name] = Member(name, tier)

# Read the names from the blacklist.txt file
blacklist = []
with open(os.path.join(current_dir, 'blacklist.txt'), 'r') as file:
    for line in file:
        name = line.strip()
        if name in names.keys():
            names[name].set_blacklist(True)

# Read the aliases from the alias.csv file
aliases = {}
with open(os.path.join(current_dir, 'alias.csv'), 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        name = row[0].strip()
        if name in names.keys():
            names[name].set_alias(row[1].strip())


# Replace names with aliases if available
filtered_names = []
for member in sorted(list(names.values()), key=lambda x: x.name):
    filtered_names.append(str(member))

print("Filtered to {} names.".format(len(filtered_names)))

# Write the names or aliases to the members.txt file in the game folder
with open(os.path.join(game_folder, 'members.csv'), 'w') as file:
    for name in filtered_names:
        file.write(name + '\n')

print("Written to members.txt in the game folder.")

# Pause the console
input("Press Enter to exit...")
