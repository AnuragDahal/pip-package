import os
import json

def get_folder_structure(rootdir):
    folder_structure = {}
    for dirpath, dirnames, filenames in os.walk(rootdir):
        folder_structure[dirpath] = []
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r') as file:
                try:
                    content = file.read()
                except UnicodeDecodeError:
                    content = "Unable to read file content"
                folder_structure[dirpath].append({
                    'path': filepath,
                    'content': content
                })
    return folder_structure


# replace with your directory
rootdir = './fastapi-mongo'
folder_structure = get_folder_structure(rootdir)

with open('folder_structure.json', 'w') as json_file:
    json.dump(folder_structure, json_file, indent=4)
