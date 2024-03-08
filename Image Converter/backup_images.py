import os
import shutil
import subprocess
from typing import Tuple
import pyautogui

def move_files(move_mode: str, s_file: str, dest_file: str, overwrite: str) -> Tuple[int, str]:
    if os.path.exists(dest_file):
        # File already exists at destination
        
        response = overwrite
        if overwrite == '':
            response = pyautogui.confirm(text = f"The file '{s_file}' already exists at the destination ({dest_file}). \nWhat would you like to do?", title = "File already exists", buttons = ['Overwrite', 'Ignore', 'Overwrite all', 'Ignore all', 'Cancel'])

        if response == 'Overwrite all':
            # Overwrite all occurrences
            overwrite = 'Overwrite all'

        elif response == 'Ignore':
            # Ignore this occurrence only
            return (1, overwrite)
        elif response == 'Ignore all':
            # Ignore all occurrences
            overwrite = 'Ignore all'
            return (1, overwrite)
        elif response == 'Cancel':
            # Cancel operation
            overwrite = 'Cancel'
            return (2, overwrite)

        if move_mode == 'Backup images' or move_mode == 'Copy new images to Extract' or move_mode == 'Return modified images' or move_mode == 'Backup to Extract':
            shutil.copy2(s_file, dest_file)
        elif mode == 'Extract new images':
            shutil.move(s_file, dest_file)
    else:
        # File doesn't exist at destination, copy it
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)  # Create necessary directories
        if move_mode == 'Backup images' or move_mode == 'Copy new images to Extract' or move_mode == 'Return modified images' or move_mode == 'Backup to Extract':
            shutil.copy2(s_file, dest_file)
        elif move_mode == 'Extract new images':
            shutil.move(s_file, dest_file)
    return (0, overwrite)

source_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../game/images'))

file_target = '.png'

mode = pyautogui.confirm(text = 'What would you like to do?', title = 'Backup Images', buttons = ['Backup images', 'Copy new images to Extract', 'Extract new images', 'Return modified images', 'Convert images', 'Backup to Extract', 'Cancel'])

destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))  # Destination folder 3 levels above the current directory
destination_path2 = ""
if mode == 'Cancel':
    exit()
elif mode == 'Extract new images':
    destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))  # Destination folder 3 levels above the current directory
elif mode == 'Copy new images to Extract':
    destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
elif mode == 'Backup images':
    destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))  # Destination folder 3 levels above the current directory
    destination_path2 = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Full Image Backup'))
elif mode == 'Return modified images':
    destination_path = source_path
    source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
    file_target = '.webp'
elif mode == 'Convert images':
    source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
elif mode == 'Backup to Extract':
    destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
    source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))


print("Source path: " + str(source_path))
print("Destination path: " + destination_path)
if destination_path2 != "":
    print("Destination path 2: " + destination_path2)

overwrite_setting = ''

paths = []

count = 0

# Recursively traverse the source directory
for root, dirs, files in os.walk(source_path):
    for file in files:
        if file.endswith(file_target):
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_path, os.path.relpath(source_file, source_path))
            destination_file2 = os.path.join(destination_path2, os.path.relpath(source_file, source_path))

            if mode == 'Convert images':
                paths.append(source_file)
                continue

            result, overwrite_setting = move_files(mode, source_file, destination_file, overwrite_setting)

            if result == 1:
                continue
            elif result == 2:
                break
            else:
                count += 1

            if destination_path2 != "":
                result, overwrite_setting = move_files(mode, source_file, destination_file2, overwrite_setting)

                if result == 1:
                    continue
                elif result == 2:
                    break

    if overwrite_setting == 'Cancel':
        break

if mode == 'Convert images':
    response = pyautogui.confirm(text = f"Would you like to convert lossy or lossless?", title = "Convert images", buttons = ['Lossy', 'Lossless', 'Cancel'])
    if response != 'Cancel':
        for i, path in enumerate(paths):
            nconvert_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'NConvert/nconvert.exe'))
            print(f"Converting {i + 1}/{len(paths)}: {path}")
            if response == 'Lossless':
                subprocess.run([nconvert_path, "-overwrite", "-out", "webp", "-q", "-1", path])
            else:
                subprocess.run([nconvert_path, "-overwrite", "-out", "webp", "-q", "90", path])
            count += 1

if mode == 'Backup images':
    pyautogui.alert(text = "Created Backup for " + str(count) + " images!", title = "Done", button = "OK")
elif mode == 'Copy new images to Extract':
    pyautogui.alert(text = "Copied all " + str(count) + " images to Extract!", title = "Done", button = "OK")
elif mode == 'Extract new images':
    pyautogui.alert(text = "Extracted all " + str(count) + " images!", title = "Done", button = "OK")
elif mode == 'Return modified images':
    pyautogui.alert(text = "Returned all " + str(count) + " modified images!", title = "Done", button = "OK")
elif mode == 'Convert images':
    pyautogui.alert(text = "Converted all " + str(count) + " images!", title = "Done", button = "OK")
else:
    pyautogui.alert(text = "Finished: " + str(count), title = "Done", button = "OK")
