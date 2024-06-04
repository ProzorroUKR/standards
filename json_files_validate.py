import json
import os


def get_files_paths(root):
    files = []
    for name in os.listdir(root):
        if name.startswith("."):
            # skip hidden files
            continue

        path = os.path.join(root, name)
        if os.path.isdir(path):
            files.extend(get_files_paths(path))
        else:
            files.append(path)
    return files

def validate_json_files(path):
    is_valid = True
    for file_path in get_files_paths("."):
        if file_path.endswith(".json"):
            try:
                with open(file_path, "r") as f:
                    json.loads(f.read())
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(file_path, e)
                is_valid = False
    return is_valid


if __name__ == "__main__":
    if not validate_json_files("."):
        exit(1)
