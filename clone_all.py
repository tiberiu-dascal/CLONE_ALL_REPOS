import base64
import os
import subprocess
import sys

# The script is expecting an environment variable called ENCODED_GITHUB_TOKEN to be present
# and its value to be set to your base64-encoded github token

encoded_env = os.getenv("ENCODED_GITHUB_TOKEN")
if encoded_env is None:
    print(
        "Your GitHub token is not set!\n"
        "Please make sure to configure your environment variable ENCODED_GITHUB_TOKEN and then run the program again!"
    )
    sys.exit(1)

GITHUB_TOKEN = base64.b64decode(encoded_env).decode("utf-8").strip()


def install_package(package):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package, "--break-system-packages"],
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"Failed to install {package}:\n{result.stderr.decode()}")
        sys.exit(1)


try:
    from git import Repo
    from git import exc as exc
except ImportError:
    install_package("GitPython")
    from git import Repo
    from git import exc as exc

try:
    from github import Auth, Github
except ImportError:
    install_package("PyGithub")
    from github import Auth, Github


BASE_DIR = f"{os.getenv('HOME')}/REPOS"  # change this to match your preference
os.makedirs(BASE_DIR, exist_ok=True)

# login with access token
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# get the user and repos
user = g.get_user()
my_repos = user.get_repos()

# Loop through repos and try to clone them locally
failed = 0
success = 0
for repo in my_repos:
    name = repo.name
    print(f"Cloning repo #+- {name} -+#\n\tFrom: {repo.clone_url}\n\tTo: {BASE_DIR}/{name}")
    try:
        clone_url = f"https://{GITHUB_TOKEN}@github.com/{user.login}/{name}.git"
        Repo.clone_from(clone_url, BASE_DIR + "/" + name)
        print("\tStatus: ✅\n")
        success += 1
    except exc.CommandError:
        print(f"\tStatus: ⛔️: Repo #+- {name} -+# already exists and is not empty!\n")
        failed += 1

g.close()

# Display final statistics
print(f"Checked {failed + success} repos: SUCCESS: {success}, FAILED: {failed}")
