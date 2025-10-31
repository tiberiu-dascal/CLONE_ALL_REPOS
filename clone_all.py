import os
import base64

# The script is expecting an environment variable called GITHUB_TOKEN to be present
# and its value to be set to your github token

encoded_env = os.getenv('ENCODED_GITHUB_TOKEN')
decode_bytes = base64.b64decode(encoded_env)
final_string = decode_bytes.decode("utf-8")
GITHUB_TOKEN = final_string.replace('\n', '')


if GITHUB_TOKEN is None:
    print("You GitHub token is not set!\n Please make sure to configure your environment variable GITHUB_API_TOKEN and the run the program again!")
    exit(1)

try:
    from git import Repo      # GitPython used to clone remote repo to local (GitPython module)
    from git import exc as exc
except:
    os.system("pip install GitPython --break-system-packages")
    from git import Repo
    from git import exc as exc

try:
    from github import Github, Auth # used to interact with GitHub API (PyGithub module)
except:
    os.system("pip install PyGithub --break-system-packages")
    from github import Github, Auth

BASE_DIR=f"{os.getenv('HOME')}/REPOS" # change this to match you preference

# login with access token
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# get the user
user = g.get_user()
my_repos = user.get_repos()
g.close()
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
        Repo.clone_from(f"git@github.com:{user.login}/{name}.git", BASE_DIR+"/"+name);
        print("\tStatus: ✅\n")
        success += 1
    except exc.CommandError as e:
        print(f"\tStatus: ⛔️: Repo #+- {name} -+# already exists and is not empty!\n")
        failed += 1
        continue

 # Display final statistics
print(f"Checked {failed+success} repos: SUCCESS:  {success}, FAILED: {failed}")

