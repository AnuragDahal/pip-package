import os
import json


def get_folder_structure(rootdir):
    folder_structure = {}
    for dirpath, dirnames, filenames in os.walk(rootdir):
        # String slicing is done to get the relative path
        relative_dirpath = '.' + dirpath[len(rootdir):]
        # path is created as a key in the dictionary as the values are created as list
        folder_structure[relative_dirpath] = []
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # string slicing
            relative_filepath = '.' + filepath[len(rootdir):]
            with open(filepath, 'r') as file:
                try:
                    content = file.read()
                except UnicodeDecodeError:
                    content = "Unable to read file content"
                folder_structure[relative_dirpath].append({
                    'path': relative_filepath,
                    'content': content
                })
    return folder_structure


rootdir = './fastapi-mongo'
folder_structure = get_folder_structure(rootdir)




with open('folder_structure.json', 'w') as json_file:
    json.dump(folder_structure, json_file, indent=4)
