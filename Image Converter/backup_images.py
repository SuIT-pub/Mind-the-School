import os
import pathlib
import shutil
import subprocess
from typing import Tuple
import pyautogui

def move_files(move_mode: str, s_file: str, dest_file: str, overwrite: str) -> Tuple[int, str]:
    if os.path.exists(dest_file):
        # File already exists at destination
        
        response = overwrite
        if overwrite == '':
            if dest_file.endswith('.webm'):
                response = pyautogui.confirm(text = f"The file '{s_file}' already exists at the destination ({dest_file}). \nWhat would you like to do?", title = "File already exists", buttons = ['Overwrite', 'Ignore', 'Overwrite all', 'Ignore all', 'Ignore all webm', 'Cancel'])
            else:
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
        elif response == 'Ignore all webm' and dest_file.endswith('.webm'):
            # Ignore all occurrences of webm
            overwrite = 'Ignore all webm'
            return (1, overwrite)
        elif response == 'Cancel':
            # Cancel operation
            overwrite = 'Cancel'
            return (2, overwrite)

        if (move_mode == 'Backup images' or 
            move_mode == 'Copy new images to Extract' or 
            move_mode == 'Return modified images' or 
            move_mode == 'Move Backup to Extract' or 
            move_mode == 'Move Images to Versioned Backup' or
            move_mode == 'Return Images from Versioned Backup' or
            move_mode == 'Return Videos'
        ):
            shutil.copy2(s_file, dest_file)
        elif move_mode == 'Extract new images':
            shutil.move(s_file, dest_file)
    else:
        # File doesn't exist at destination, copy it
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)  # Create necessary directories
        if (move_mode == 'Backup images' or 
            move_mode == 'Copy new images to Extract' or 
            move_mode == 'Return modified images' or 
            move_mode == 'Move Backup to Extract' or 
            move_mode == 'Move Images to Versioned Backup' or
            move_mode == 'Return Images from Versioned Backup' or
            move_mode == 'Return Videos'
        ):
            shutil.copy2(s_file, dest_file)
        elif move_mode == 'Extract new images':
            shutil.move(s_file, dest_file)
    return (0, overwrite)

def main():
    source_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../game/images'))

    file_target = ['.png']
    end_file_target = ['.png']

    mode = pyautogui.confirm(text = 'What would you like to do?', title = 'Backup Images', buttons = ['Backup images', 'Extract new images', 'Convert images', 'Return modified images', 'Clean Extract', 'Move Backup to Extract', 'Versioned Backup', 'Return Videos', 'Count', 'Compare images', 'Close'])
    if mode == 'Versioned Backup':
        mode = pyautogui.confirm(text = 'What would you like to do?', title = 'Backup Images', buttons = ['Move Images to Versioned Backup', 'Return Images from Versioned Backup', 'Cancel'])

    destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))  # Destination folder 3 levels above the current directory
    destination_path2 = ""
    if mode == 'Close':
        exit()
    elif mode == 'Extract new images':
        destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))  # Destination folder 3 levels above the current directory
        purge = pyautogui.confirm(text = 'Purge extract folder?', title = 'Copy to extract', buttons = ['Yes', 'No', 'Cancel'])
        if purge == 'Yes':
            clean_dir = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
            dirs = [name for name in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, name))]
            for dir in dirs:
                shutil.rmtree(os.path.join(clean_dir, dir))
            pyautogui.alert(text = "Purged extract folder!", title = "Done", button = "OK")
        elif purge == "Cancel":
            return
    elif mode == 'Copy new images to Extract':
        destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
    elif mode == 'Backup images':
        file_target = ['.png', '.webm']
        destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))  # Destination folder 3 levels above the current directory
        destination_path2 = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Full Image Backup'))
    elif mode == 'Return modified images':
        destination_path = source_path
        source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
        file_target = ['.webp']
    elif mode == 'Convert images':
        source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
    elif mode == 'Move Backup to Extract':
        destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
        source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
        file_target = ['.png']
    elif mode == 'Return Videos':
        file_target = ['.webm']
        destination_path = source_path
        source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
    elif mode == 'Move Images to Versioned Backup':
        versions = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups"))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + name)))]
        versions.append("Cancel")
        dest_choice = pyautogui.confirm(text = 'Where would you like to move the images to?', title = 'Versioned Backup', buttons = versions)
        if dest_choice == "Cancel":
            return
        lossy_variant = pyautogui.confirm(text = 'Would you like to move to lossy or lossless?', title = 'Convert images', buttons = ['lossless', 'lossy', 'Cancel'])
        if lossy_variant == "Cancel":
            return
        if not os.path.exists(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))):
            os.mkdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant)))
        destination_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))
        file_target = ['.png', '.webm', '.webp']
    elif mode == 'Return Images from Versioned Backup':
        versions = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups"))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + name)))]
        versions.append("Cancel")
        dest_choice = pyautogui.confirm(text = 'Where would you like to move the images from?', title = 'Versioned Backup', buttons = versions)
        if dest_choice == "Cancel":
            return
        lossy_variant = pyautogui.confirm(text = 'Would you like to move from lossy or lossless?', title = 'Convert images', buttons = ['lossless', 'lossy', 'Cancel'])
        if lossy_variant == "Cancel":
            return
        if not os.path.exists(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))):
            os.mkdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant)))
        destination_path = source_path
        source_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))
        file_target = ['.png', '.webm', '.webp']
    elif mode == 'Count':
        first_dest_choice = pyautogui.confirm(text = 'Where would you like to count the images from?', title = 'Count Images', buttons = ['Game', 'Image Extract', 'Image Backup', 'Versioned Backup', 'Cancel'])
        if first_dest_choice == "Cancel":
            return
        if first_dest_choice == "Image Extract":
            source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
        elif first_dest_choice == "Image Backup":
            source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
        elif first_dest_choice == "Versioned Backup":

            versions = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups"))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + name)))]
            versions.append("Cancel")
            dest_choice = pyautogui.confirm(text = 'Where would you like to move the images from?', title = 'Versioned Backup', buttons = versions)
            if dest_choice == "Cancel":
                return

            lossy_folders = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + name)))]

            if 'lossy' in lossy_folders and 'lossless' in lossy_folders:
                lossy_variant = pyautogui.confirm(text = 'Would you like to move from lossy or lossless?', title = 'Convert images', buttons = ['lossless', 'lossy', 'Cancel'])
                if lossy_variant == "Cancel":
                    exit()
                if not os.path.exists(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))):
                    os.mkdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant)))
                source_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))
            elif 'lossy' in lossy_folders:
                source_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/lossy"))
            elif 'lossless' in lossy_folders:
                source_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/lossless"))
            else:
                source_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice))

        file_target = ['.png', '.webp', '.webm']
    elif mode == 'Compare images':
        comp_mode = pyautogui.confirm(text = 'What would you like to compare?', title = 'Compare Images', buttons = ['game -> backup', 'backup -> game', 'game -> (full) backup', 'Cancel'])
        if comp_mode == 'Cancel':
            return
        if comp_mode == 'game -> backup':
            destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
            file_target = ['.webp']
            end_file_target = ['.png']
        elif comp_mode == 'game -> (full) backup':
            destination_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
            destination_path2 = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Full Image Backup'))
            file_target = ['.webp']
            end_file_target = ['.png']
        elif comp_mode == 'backup -> game':
            destination_path = source_path
            source_path = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Backup'))
            file_target = ['.png']
            end_file_target = ['.webp']
        elif comp_mode == "Versioned Backup":

            versions = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups"))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + name)))]
            versions.append("Cancel")
            dest_choice = pyautogui.confirm(text = 'What version would you like to compare the game to?', title = 'Versioned Backup', buttons = versions)
            if dest_choice == "Cancel":
                return

            lossy_folders = [name for name in os.listdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice))) if os.path.isdir(os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + name)))]

            if 'lossy' in lossy_folders and 'lossless' in lossy_folders:
                lossy_variant = pyautogui.confirm(text = 'Would you like to compare lossy or lossless?', title = 'Compare images', buttons = ['lossless', 'lossy', 'Cancel'])
                if lossy_variant == "Cancel":
                    exit()
                destination_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/" + lossy_variant))
            elif 'lossy' in lossy_folders:
                destination_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/lossy"))
            elif 'lossless' in lossy_folders:
                destination_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice + "/lossless"))
            else:
                destination_path = os.path.abspath(os.path.join(source_path, "../../../Versioned Image Backups/" + dest_choice))
            file_target = ['.webp']
            end_file_target = 'compare_versioned'
    elif mode == 'Clean Extract':
        clean_confirm = pyautogui.confirm(text = 'Do you really want to purge everything in the Extract Folder?', title = 'Compare Images', buttons = ['YES', 'NO'])
        if clean_confirm == 'NO':
            return
        clean_dir = os.path.abspath(os.path.join(source_path, '../../../Image Extracter/Mind the School Image Extract'))
        dirs = [name for name in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, name))]
        for dir in dirs:
            shutil.rmtree(os.path.join(clean_dir, dir))
        pyautogui.alert(text = "Purged extract folder!", title = "Done", button = "OK")
        return      




    print("Source path: " + str(source_path))
    print("Destination path: " + destination_path)
    if destination_path2 != "":
        print("Destination path 2: " + destination_path2)

    overwrite_setting = ''

    paths = []

    count = 0

    vid_count = 0

    # Recursively traverse the source directory
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if any(file.endswith(target) for target in file_target):
                if mode == 'Count':
                    if file.endswith('.webm'):
                        vid_count += 1
                    else:
                        count += 1
                    continue


                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_path, os.path.relpath(source_file, source_path))
                destination_file2 = os.path.join(destination_path2, os.path.relpath(source_file, source_path))

                if mode == 'Convert images':
                    paths.append(source_file)
                    continue

                if mode == 'Compare images':
                    estimated_destination_file = os.path.join(destination_path, os.path.relpath(source_file, source_path))
                    if not end_file_target == 'compare_versioned':
                        estimated_destination_file = estimated_destination_file.replace('.png', '.2')
                        estimated_destination_file = estimated_destination_file.replace('.webp', '.png')
                        estimated_destination_file = estimated_destination_file.replace('.2', '.webp')
                    estimated_destination_file2 = destination_path2
                    if destination_path2 != "":
                        estimated_destination_file2 = os.path.join(destination_path2, os.path.relpath(source_file, source_path))
                        if not end_file_target == 'compare_versioned':
                            estimated_destination_file2 = estimated_destination_file2.replace('.png', '.2')
                            estimated_destination_file2 = estimated_destination_file2.replace('.webp', '.png')
                            estimated_destination_file2 = estimated_destination_file2.replace('.2', '.webp')
                    if not os.path.exists(estimated_destination_file):
                        if (destination_path2 == "" or not os.path.exists(estimated_destination_file2)):
                            source_file = source_file.replace('h:', 'H:')
                            source_file = source_file.replace('H:\Dateien\OneDrive\RenPy Project\Mind the School\game\images\\', '')
                            source_file = source_file.replace('H:\Dateien\OneDrive\RenPy Project\Image Extracter\Mind the School Image Backup\\', '')
                            estimated_destination_file = estimated_destination_file.replace('h:', 'H:')
                            estimated_destination_file = estimated_destination_file.replace('H:\Dateien\OneDrive\RenPy Project\Mind the School\game\images\\', '')
                            estimated_destination_file = estimated_destination_file.replace('H:\Dateien\OneDrive\RenPy Project\Image Extracter\Mind the School Image Backup\\', '')
                            print(f"Counterpart missing for: {source_file}\n    expected at {estimated_destination_file}")
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
        response = pyautogui.confirm(text = f"Would you like to convert lossy or lossless?", title = "Convert images", buttons = ['Lossless', 'Lossy', 'Cancel'])
        if response != 'Cancel':
            for i, path in enumerate(paths):
                nconvert_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'NConvert/nconvert.exe'))
                print(f"\n\nConverting {i + 1}/{len(paths)}: {path}\n---------------------------------")
                if response == 'Lossless' or not '\\events\\' in path:
                    print('overriding quality')
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
    elif mode == 'Move Images to Versioned Backup':
        pyautogui.alert(text = "Moved all " + str(count) + " images to Versioned Backup!", title = "Done", button = "OK")
    elif mode == 'Return Images from Versioned Backup':
        pyautogui.alert(text = "Returned all " + str(count) + " images from Versioned Backup!", title = "Done", button = "OK")
    elif mode == 'Return Videos':
        pyautogui.alert(text = "Returned all " + str(count) + " videos!", title = "Done", button = "OK")
    elif mode == 'Count':
        pyautogui.alert(text = "Images: " + str(count) + "\nVideos: " + str(vid_count) + "\nIn " + first_dest_choice, title = "Count", button = "OK")
    else:
        pyautogui.alert(text = "Finished: " + str(count), title = "Done", button = "OK")

while True:
    main()