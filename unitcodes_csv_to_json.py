import json
from collections import OrderedDict
filepath = 'Unitcodes.csv'

def split_csv(line):
    return [x.strip() for x in line.split(',')]

def replace_minus(entry):
    return "" if entry == '-' else entry

result = {}
with open(filepath) as fp:  
    line = fp.readline()
    _, *key_names = split_csv(line)
    line = fp.readline()
    while line:
        code, *keys = split_csv(line)
        result[code] = OrderedDict(zip(key_names, [replace_minus(key) for key in keys]))

        line = fp.readline()

print(json.dumps(result, indent=4, sort_keys=False, ensure_ascii=False))