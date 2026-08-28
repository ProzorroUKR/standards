"""Rebuild uktzed.json from the УКТЗЕД tables published in the Customs Tariff law.

Source tables (printable version, one <table> per HS group, columns:
Код | Назва | Ставки мита, % | Додаткові ОВО):
  - https://zakon.rada.gov.ua/laws/show/2697а-20/print  (groups 1-49)
  - https://zakon.rada.gov.ua/laws/show/2697б-20/print  (groups 50-97)
"""

import argparse
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

SOURCE_URLS = [
    "https://zakon.rada.gov.ua/laws/show/2697а-20/print",
    "https://zakon.rada.gov.ua/laws/show/2697б-20/print",
]

DEFAULT_OUTPUT = "./classifiers/uktzed.json"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

# УКТЗЕД codes are grouped as "NNNN NN NN NN" (4 digits, then up to three
# groups of 2 digits).
CODE_RE = re.compile(r"^\d{4}(\s\d{2}){0,3}$")
BRACKET_CODE_RE = re.compile(r"^\[\d+\]$")
LEADING_DASHES_RE = re.compile(r"^((?:- )+)")


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=60)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def format_name(name: str) -> str:
    """Collapse "- - -" hierarchy markers into "---" as in the original data."""
    match = LEADING_DASHES_RE.match(name)
    if not match:
        return name
    dash_count = match.group(0).count("-")
    rest = name[match.end():]
    return "-" * dash_count + " " + rest


def extract_entries(html: str) -> list[tuple[str, str]]:
    """Return (code, name) pairs in document order for every code table found."""
    soup = BeautifulSoup(html, "html.parser")
    entries = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
        header_cells = [c.get_text(" ", strip=True) for c in rows[0].find_all(["td", "th"])]
        if not header_cells or header_cells[0] != "Код":
            continue

        for row in rows:
            cells = row.find_all(["td", "th"])
            texts = [c.get_text(" ", strip=True) for c in cells]
            if not texts:
                continue
            code = texts[0].strip()
            if not code or BRACKET_CODE_RE.match(code):
                continue
            if not CODE_RE.match(code):
                continue

            name = texts[1].strip() if len(texts) > 1 else ""
            if not name:
                print(f"warning: code {code!r} has no name, skipping", file=sys.stderr)
                continue

            entries.append((re.sub(r"\D", "", code), format_name(name)))
    return entries


def build_uktzed(urls: list[str] = SOURCE_URLS) -> dict[str, str]:
    result: dict[str, str] = {}
    for url in urls:
        html = fetch_html(url)
        for code, name in extract_entries(html):
            if code in result and result[code] != name:
                print(
                    f"warning: code {code} redefined: {result[code]!r} -> {name!r}",
                    file=sys.stderr,
                )
            result[code] = name
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="path to write uktzed.json to")
    args = parser.parse_args()

    data = build_uktzed()
    print(f"collected {len(data)} codes", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
