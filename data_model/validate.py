from jsonschema import RefResolver, Draft7Validator, _utils as json_shema_utils
import json
import os.path
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SCHEMA_DIR = os.path.join(CURRENT_PATH, "schema")
DATA_DIR = os.path.join(CURRENT_PATH, "data")
errors = []


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


def main():
    schema_count = data_count = 0

    meta_validator = Draft7Validator(json_shema_utils.load_schema("draft7"))
    for schema_name in os.listdir(SCHEMA_DIR):
        full_name = os.path.join(SCHEMA_DIR, schema_name)
        schema_json = get_json(full_name)
        for e in meta_validator.iter_errors(schema_json):
            errors.append(e)
        schema_count += 1

    check_errors("Invalid schema")

    # validate data
    for schema_name in os.listdir(DATA_DIR):
        schema = get_schema(schema_name)
        resolver = RefResolver(base_uri=f'file://{SCHEMA_DIR}/', referrer=schema)
        validator = Draft7Validator(schema, resolver=resolver)
        examples_dir = os.path.join(DATA_DIR, schema_name)
        for file_name in os.listdir(examples_dir):
            full_name = os.path.join(examples_dir, file_name)
            for e in validator.iter_errors(instance=get_json(full_name)):
                errors.append(e)
            data_count += 1

    check_errors("Invalid data")
    print(f"Successfully checked {schema_count} schema and {data_count} data files")


if __name__ == "__main__":
    main()

