#! /usr/bin/python
from collections import defaultdict
import os
import fnmatch

def load_template():
    template_path = os.path.join('docs', 'templates', 'index.template.html')
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")

LANG_CODES = ("en", "uk", "ru", "ro")

IGNORE_PATTERNS = (
    "./__pycache__/*",
    "./standards.egg-info/*",
    "./index.html",
    "./mask_codes_example.json",
    ".DS_Store",
    "README.md",
    "CNAME",
    "*.html",
    "*.js",
    "*.css",
    "*.py",
    "*.txt",
    ".*",
)


def find_versions(file_names):
    versions = defaultdict(list)
    for name, full_name in file_names:
        versions[name].append(
            (name, full_name)
        )
    return versions


def convert_to_list(strings):
    return "<ul><li>{}</li></ul>".format("</li><li>".join(strings))


def versions_to_html(args):
    response = "|".join(
        '<a href="{}" target="_blank">{}</a>'.format(full_name.replace('./', '../'), v_name)
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

    # Process directories first
    items = []
    # Add directories
    items.extend(dirs)
    
    # Then add files
    file_versions = find_versions(files)
    for f_name, versions in sorted(file_versions.items()):
        items.append(
            "{}".format(
                versions_to_html(versions)
            )
        )

    response = ""
    if items:
        response = convert_to_list(items)

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
    content = format_html(get_files("."))
    template = load_template()
    with open(os.path.join('docs', 'index.html'), "w") as f:
        f.write(template.format(content=content, root_path=""))
