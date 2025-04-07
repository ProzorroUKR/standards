import json
import requests

from datetime import datetime

KPK_RESOURCE_API = "https://api.openbudget.gov.ua/items"


def get_openbudget_dictionary():
    for dict_name in ("KPK", "TKPKMB"):
        resource_url = f"{KPK_RESOURCE_API}/{dict_name}"
        response = requests.get(resource_url)
        if response.status_code == 200:
            data = response.json()
            if dict_name == "KPK":
                export_kpk(dict_name, data)
            else:
                write_json_dict(dict_name, data)
        else:
            print(f"Response from resource {resource_url}: {response.status_code} - {response.text}")


def write_json_dict(dict_name, dict_data):
    result = {
        item["code"]: {k: v for k, v in item.items() if k != "code"}
        for item in dict_data
    }
    json_object = json.dumps(result, indent=2, ensure_ascii=False)
    with open(f'./classifiers/{dict_name.lower()}.json', 'w') as outfile:
        outfile.write(json_object)
        outfile.write("\n")  # empty line in the end of file for json validation


def export_kpk(dict_name, dict_data):
    kpk_years = {}
    for kpk_row in dict_data:
        if not kpk_row.get("datefrom"):
            print(kpk_row["code"])
        year_from = datetime.strptime(kpk_row.get("datefrom"), "%Y-%m-%d").year
        # By default, we take current year, if there wasn't `dateto` in dictionary that means that code is still using
        year_to = datetime.now().year
        if date_to := kpk_row.get("dateto"):
            year_to = datetime.strptime(date_to, "%Y-%m-%d").year
        dict_year = year_from
        while dict_year <= year_to:
            kpk_years.setdefault(dict_year, []).append(kpk_row)
            dict_year += 1

    for year in kpk_years.keys():
        write_json_dict(f"{dict_name}_{year}", kpk_years[year])


if __name__ == "__main__":
    get_openbudget_dictionary()
