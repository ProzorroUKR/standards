from jsonschema import RefResolver, Draft7Validator, _utils as json_shema_utils
from collections import defaultdict
import json
import os.path
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SCHEMA_DIR = os.path.join(CURRENT_PATH, "schema")
DATA_DIR = os.path.join(CURRENT_PATH, "data")
errors = []
counts = defaultdict(int)


def get_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


def get_schema(name):
    schema = get_json(os.path.join(SCHEMA_DIR, f"{name}.json"))
    return schema


def validate(instance, schema):
    resolver = RefResolver(base_uri=f'file://{SCHEMA_DIR}/', referrer=schema)
    v = Draft7Validator(schema, resolver=resolver)
    return v.iter_errors(instance)


def check_errors(title):
    if errors:
        print(title)
        for e in errors:
            print("-" * 72)
            print(e)
        exit(1)


def process_schema_files(validator, directory, count_name="schema"):
    global counts
    for file_name in os.listdir(directory):
        full_name = os.path.join(directory, file_name)
        if os.path.isdir(full_name):
            process_schema_files(validator, full_name)
        else:
            schema_json = get_json(full_name)
            for e in validator.iter_errors(schema_json):
                errors.append(e)
            counts[count_name] += 1


def main():
    # validate schema files
    meta_validator = Draft7Validator(json_shema_utils.load_schema("draft7"))
    process_schema_files(meta_validator, SCHEMA_DIR)
    check_errors("Invalid schema")

    # validate data files
    for schema_name in os.listdir(DATA_DIR):
        schema = get_schema(schema_name)
        resolver = RefResolver(base_uri=f'file://{SCHEMA_DIR}/', referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver)
        examples_dir = os.path.join(DATA_DIR, schema_name)
        process_schema_files(validator, examples_dir, count_name="data")
    check_errors("Invalid data")

    print(f"Successfully checked {counts['schema']} schema and {counts['data']} data files")


if __name__ == "__main__":
    main()
