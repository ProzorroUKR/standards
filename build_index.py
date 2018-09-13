#! /usr/bin/python
from collections import defaultdict
import os

LAYOUT = """---
layout: default
---
<body>{}</body>"""

LANG_CODES = ("en", "uk", "ru", "ro")
IGNORE_EXT = ("py", "txt", "html")
IGNORE_FILES = ("CNAME", "_config.yml")


def find_versions(file_names):
    versions = defaultdict(list)
    for name, full_name in file_names:
        options = []

        if name in IGNORE_FILES:
            continue

        name_parts = name.split(".")
        if name_parts[-1] in IGNORE_EXT:
            continue

        name = name_parts[0]
        options.extend(name_parts[1:])

        if name.endswith("_pretty"):
            name = name[:-7]
            options.append("pretty")

        if name.endswith("_annotated"):
            name = name[:-10]
            options.append("annotated")

        if name[-2:] in LANG_CODES:
            options.append(name[-2:])
            name = name[:-2]

        versions[name].append(
            (".".join(reversed(options)), full_name)
        )
    return versions


def convert_to_list(strings):
    if strings:
        return "<ul><li>{}</li></ul>".format("</li><li>".join(strings))


def versions_to_html(args):
    response = " ".join(
        '<a href="{}" target="_blank">{}</a>'.format(full_name, v_name)
        for v_name, full_name in args
    )
    return response


def get_files(path):
    files, dirs = [], []
    for f_name in os.listdir(path):
        if f_name.startswith(path):
            continue

        full_name = os.path.join(path, f_name)
        if os.path.isdir(full_name):
            line = get_files(full_name)
            if line:
                dirs.append("{} {}".format(f_name, line))
        else:
            files.append(
                (f_name, full_name)
            )

    file_versions = find_versions(files)
    items = []
    for f_name, versions in sorted(file_versions.items()):
        items.append(
            "{} [ {} ]".format(
                f_name,
                versions_to_html(versions)
            )
        )

    items.extend(dirs)
    response = ""
    if items:
        if len(items) > 1:
            response = convert_to_list(items)
        else:
            response = items[0]

    return response


if __name__ == "__main__":
    data = get_files(".")

    with open("index.html", "w") as f:
        f.write(LAYOUT.format(data))

