import os
import json
import requests
from git import Repo

# You need to set a enviroment variable HOMEBREW_GITHUB_API_TOKEN 
# and set it equal to your github token
GIT_TOKEN = os.getenv('HOMEBREW_GITHUB_API_TOKEN')
GIT_USER = 'tibix' # change this to match your user
GIT_URL=f'https://api.github.com/users/{GIT_USER}/repos'
BASE_DIR='/Users/teebee/REPOS' # change this to match you preference

head = {'Authorization': 'token {}'.format(GIT_TOKEN)}

# Generate a list of all available repositories through json call to GitHUB API
json_url = requests.get(GIT_URL, headers=head)
items = json.loads(json_url.text)

# Initialize a dictionary that will store repo name and URL to clone the repo
repos = dict()

# Populate the repos dict
for item in items:
    repos[item['name']] = item['clone_url']

# Loop through dict and try to clone the repositories in a local folder
for name, repo in repos.items():
    print(f"Clonning repo {name} to {BASE_DIR}/{name} from {repo}")
    try:
        Repo.clone_from(repo, BASE_DIR+"/"+name);
    except:
        print(f"ERROR: Could not clone repo {name}")
