import requests, json

token = "secret_SoxtRjDO17G6KwJRIvdnvcAXBXBhVoNqOiF3IeFmiEG"

databaseId = "3e002c5ea2a64ab6aa8d7650363f1273"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def readDatabase(name, databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()

    with open(f'./db{name}.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

    with open(f'./db{name}.json', 'r', encoding='utf8') as f:
        json_data = json.load(f)

    return json_data