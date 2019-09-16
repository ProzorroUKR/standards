"""
1) Export gmdn excel into utf-8 csv
2) Using this script convert csv into json
"""

import csv
import json
import itertools
from collections import OrderedDict
import unicodedata


def prepare(s):

    chars = []
    if isinstance(s, str):
        s = s.decode("utf-8")
    for ch in s:
        cat = unicodedata.category(ch)[0]
        if cat != "C":  # rm control characters
            chars.append(
                " " if unicodedata.category(ch)[0] == "Z" else ch  # replace whitespaces
            )
    s = "".join(chars).encode("utf-8")

    return s.strip(" \n\t")


if __name__ == "__main__":
    result = OrderedDict()
    with open('GMDN090919.csv', "r") as csvfile:
        spamreader = csv.reader(csvfile)
        for row in itertools.islice(spamreader, 1, None):
            uid, name_uk, description_uk, name_en, description_en, _ = row
            if uid:
                assert uid not in result
                result[uid] = OrderedDict(
                    [
                        ("name_uk", prepare(name_uk)),
                        ("description_uk", prepare(description_uk)),
                        ("name_en", prepare(name_en)),
                        ("description_en", prepare(description_en)),
                    ]
                )

    with open("gmdn.json", "w") as f:
        json.dump(result, f, indent=4, ensure_ascii=False, separators=(',', ': '))
