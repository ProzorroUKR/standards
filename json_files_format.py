import json
import os


INDENT = 2

def get_files_paths(root):
    files = []
    for name in os.listdir(root):
        if name.startswith(root):
            continue

        path = os.path.join(root, name)
        if os.path.isdir(path):
            files.extend(get_files_paths(path))
        else:
            files.append(path)
    return files


def format_json_files(path):
    for file_path in get_files_paths("."):
        if file_path.endswith(".json"):
            try:
                with open(file_path, "r") as fr:
                    text = fr.read()
                    data = json.loads(text)
                text_formatted = json.dumps(data, indent=INDENT, ensure_ascii=False) + "\n"
                if text != text_formatted:
                    with open(file_path, "w") as fw:
                        fw.write(text_formatted)
                    print(f"{file_path}: Formatted")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"{file_path}: {e}")


if __name__ == "__main__":
    format_json_files(".")
