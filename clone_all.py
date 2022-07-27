import json
import re
import requests
from git import Repo

GIT_TOKEN = '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'
GIT_USER = 'tibix'
GIT_URL=f'https://api.github.com/users/{GIT_USER}/repos'
BASE_DIR='/Users/teebee/REPOS'

# print(GIT_URL)
head = {'Authorization': 'token {}'.format(GIT_TOKEN)}

json_url = requests.get(GIT_URL, headers=head)
items = json.loads(json_url.text)

repos = dict()

# print(items)
for item in items:
    repos[item['name']] = item['clone_url']

for name, repo in repos.items():
    print(f"Clonning repo {name} to {BASE_DIR}/{name} from {repo}")
    try:
        Repo.clone_from(repo, BASE_DIR+"/"+name);
    except:
        print(f"ERROR: Could not clone repo {name}")

# print(repos)