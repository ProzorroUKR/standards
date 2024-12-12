#! /usr/bin/python
from collections import defaultdict
import os
import fnmatch

LAYOUT = """---
layout: default
---
<body>
{}
</body>
"""

LANG_CODES = ("en", "uk", "ru", "ro")

IGNORE_PATTERNS = (
    "./index.html",
    "./_config.yml",
    "./mask_codes_example.json",
    ".DS_Store",
    "README.md",
    "CNAME",
    "*.py",
    "*.txt",
    ".*",
)


def find_versions(file_names):
    versions = defaultdict(list)
    for name, full_name in file_names:
        options = []
        name_parts = name.split(".")

        name = ".".join(name_parts[:-1])
        options.extend(name_parts[-1:])

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
    for f_name in sorted(os.listdir(path)):
        full_name = os.path.join(path, f_name)
        relative_path = os.path.relpath(full_name, ".")
        
        # Normalize paths to use forward slashes for consistent matching
        relative_path = relative_path.replace(os.sep, '/')
        normalized_path = './' + relative_path if not relative_path.startswith('./') else relative_path
        
        # Check both filename and path patterns
        should_ignore = any(
            (fnmatch.fnmatch(normalized_path, pattern) if pattern.startswith('./') 
             else fnmatch.fnmatch(f_name, pattern))
            for pattern in IGNORE_PATTERNS
        )
        
        if should_ignore:
            continue
            
        if os.path.isdir(full_name):
            line = get_files(full_name)
            if line:
                dirs.append("{} {}".format(f_name, line))
        else:
            files.append((f_name, full_name))

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


def format_html(html):
    indent_size = 0
    formatted_html = ''
    for tag in html.split('<'):
        if tag:
            stripped = '<' + tag.strip()
            if stripped.startswith('</'):
                indent_size -= 1
            formatted_html += '  ' * indent_size + stripped + '\n'
            if stripped.startswith('<') and not stripped.startswith('</') and not stripped.endswith('/>'):
                indent_size += 1
    return formatted_html


if __name__ == "__main__":
    data = format_html(get_files("."))
    with open("index.html", "w") as f:
        f.write(LAYOUT.format(data))
