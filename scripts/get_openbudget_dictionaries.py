import json
import time
from copy import deepcopy

import requests

from datetime import datetime

KPK_RESOURCE_API = "https://api.openbudget.gov.ua/items"


def get_openbudget_dictionary():
    for dict_name in ("KPK", "TKPKMB"):
        headers = {"User-Agent": "Mozilla/5.0"}  # GitHub actions bot user-agent is being blocked by API
        resource_url = f"{KPK_RESOURCE_API}/{dict_name}"
        for attempt in range(3):
            try:
                response = requests.get(resource_url, headers=headers, timeout=10.0)
                response.raise_for_status()
                break
            except requests.HTTPError as e:
                print(f"HTTP error during downloading {dict_name}: {e.response.status_code}")
                break
            except requests.RequestException as e:
                print(f"Network issue (attempt {attempt + 1}/3): {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Another exception: {e}")
                break
        if response.status_code == 200:
            data = response.json()
            if dict_name == "KPK":
                export_kpk(dict_name, data)
            else:
                write_json_dict(dict_name, data, split_by_code=True)
        else:
            print(f"Response from resource {resource_url}: {response.status_code} - {response.text}")


def write_json_dict(dict_name, dict_data, split_by_code=False):
    sorted_dict_data = sorted(dict_data, key=lambda x: x["code"])
    if split_by_code:
        result = {
            item["code"]: {k: v for k, v in item.items() if k != "code"}
            for item in sorted_dict_data
        }
    else:
        result = sorted_dict_data
    json_object = json.dumps(result, indent=2, ensure_ascii=False)
    with open(f'./classifiers/{dict_name.lower()}.json', 'w') as outfile:
        outfile.write(json_object)
        outfile.write("\n")  # empty line in the end of file for json validation


def export_kpk(dict_name, dict_data):
    kpk_years = {}
    kpk_general = []
    for kpk_row in dict_data:
        year_from = datetime.strptime(kpk_row.get("datefrom"), "%Y-%m-%d").year
        # By default, we take current year, if there wasn't `dateto` in dictionary that means that code is still using
        year_to = datetime.now().year
        if year_from > year_to:
            year_to = year_from  # in case there will be codes the for next year
        if date_to := kpk_row.get("dateto"):
            year_to = datetime.strptime(date_to, "%Y-%m-%d").year
        dict_year = year_from
        kpk_code_years = []  # array for collecting years for particular code
        while dict_year <= year_to:
            kpk_years.setdefault(dict_year, []).append(kpk_row)
            kpk_code_years.append(dict_year)
            dict_year += 1
        kpk_code_data = deepcopy(kpk_row)
        kpk_code_data["years"] = kpk_code_years
        kpk_general.append(kpk_code_data)

    for year in kpk_years.keys():
        write_json_dict(f"{dict_name}_{year}", kpk_years[year])
    write_json_dict(dict_name, kpk_general)


if __name__ == "__main__":
    get_openbudget_dictionary()
