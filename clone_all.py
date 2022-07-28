import os
from git import Repo      # GitPython used to clone remote repo to local (GitPython module)
from github import Github # used to interact with GitHub API (PyGithub module)
from git import exc as exc
# You need to set a enviroment variable HOMEBREW_GITHUB_API_TOKEN 
# and set it equal to your github token
GIT_TOKEN = os.getenv('HOMEBREW_GITHUB_API_TOKEN')
BASE_DIR='/Users/teebee/REPOS' # change this to match you preference

#login with access token
login  = Github(GIT_TOKEN)

#get the user
user  = login.get_user()

my_repos = user.get_repos()

# Initialize a dictionary that will store repo name and URL to clone the repo
repos = dict()

# Populate the repos dict
for repo in my_repos:
    repos[repo.name] = repo.clone_url

# Loop through dict and try to clone the repositories in a local folder
failed = 0
success = 0
for name, repo in repos.items():
    print(f"Cloning repo #+- {name} -+#\n\tFrom: {repo}\n\tTo: {BASE_DIR}/{name}")
    try:
        Repo.clone_from(repo, BASE_DIR+"/"+name);
        print("\tStatus: ✅\n")
        success += 1
    except exc.CommandError as e:
        print(f"\tStatus: ⛔️: Repo #+- {name} -+# already exists and is not empty!\n")
        failed += 1
        continue

# Display final statistics
print(f"Checked {failed+success} repos: SUCCESS:  {success}, FAILED: {failed}")