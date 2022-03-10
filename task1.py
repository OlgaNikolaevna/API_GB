import requests
import json

username = 'OlgaNikolaevna'
url = 'https://api.github.com'
r = requests.get(f'{url}/users/{username}/repos')

if r.ok:
    with open('git_repo_list.json', 'w') as f:
        json.dump(r.json(), f)
    print("OK. git_repo_list.json created")
else:
    print("Error " + r)
