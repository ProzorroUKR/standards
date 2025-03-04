import os.path
from json import loads


def load(path):
    this_dir, this_filename = os.path.split(__file__)
    file_path = os.path.join(this_dir, path)
    
    # Verify the normalized path is still within the intended directory
    real_path = os.path.realpath(file_path)
    if not real_path.startswith(os.path.realpath(this_dir)):
        raise ValueError("Invalid path: path escapes the base directory")
    
    with open(file_path) as f:
        data = f.read()
    return loads(data)
