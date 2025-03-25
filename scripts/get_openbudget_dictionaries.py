import json
import requests

KPK_RESOURCE_API = "https://api.openbudget.gov.ua/items"


def get_kpk_dictionary():
    for dict_name in ("KPK", "TKPKMB"):
        resource_url = f"{KPK_RESOURCE_API}/{dict_name}"
        response = requests.get(resource_url)
        if response.status_code == 200:
            data = response.json()
            json_object = json.dumps(data, indent=2, ensure_ascii=False)
            with open(f'./classifiers/{dict_name.lower()}.json', 'w') as outfile:
                outfile.write(json_object)
        else:
            print(f"Response from resource {resource_url}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    get_kpk_dictionary()
