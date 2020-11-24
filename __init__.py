import os.path
from json import loads

def load(path):
    this_dir, this_filename = os.path.split(__file__)
    file_path = os.path.join(this_dir, path)
    with open(file_path) as f:
        data = f.read()
    return loads(data)
