import json
import os
import pkg_resources

def create_files_and_dirs_from_json():
    json_file = pkg_resources.resource_filename(__name__, 'folder_structure.json')
    with open(json_file, 'r') as json_data:
        load_json = json.load(json_data)
        for dir_path, files in load_json.items():
            os.makedirs(dir_path, exist_ok=True)
            for file in files:
                try:
                    with open(file['path'], 'w') as f:
                        f.write(file['content'])
                except FileNotFoundError:
                    print(f"File {file['path']} not found")

if __name__ == '__main__':
    create_files_and_dirs_from_json()