import argparse
import base64
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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


parser = argparse.ArgumentParser(description="Clone all GitHub repos for the authenticated user.")
parser.add_argument("--dest", default=f"{os.getenv('HOME')}/REPOS", help="Destination directory (default: ~/REPOS)")
parser.add_argument("--update", action="store_true", help="Pull latest changes for repos that already exist locally")
parser.add_argument("--workers", type=int, default=10, help="Number of parallel workers (default: 10)")
args = parser.parse_args()

BASE_DIR = args.dest
os.makedirs(BASE_DIR, exist_ok=True)

# login with access token
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# get the user and repos
user = g.get_user()
my_repos = list(user.get_repos())
g.close()


def clone_repo(repo):
    name = repo.name
    dest = BASE_DIR + "/" + name
    clone_url = f"https://{GITHUB_TOKEN}@github.com/{user.login}/{name}.git"

    if os.path.exists(dest):
        if args.update:
            try:
                local_repo = Repo(dest)
                origin = local_repo.remotes.origin
                origin.pull()
                print(f"[UPDATED] {name}")
                return "updated"
            except Exception as e:
                print(f"[FAILED]  {name} — pull error: {e}")
                return "failed"
        else:
            print(f"[SKIPPED] {name} — already exists")
            return "failed"

    try:
        Repo.clone_from(clone_url, dest)
        print(f"[CLONED]  {name}")
        return "success"
    except exc.CommandError as e:
        print(f"[FAILED]  {name} — {e}")
        return "failed"


print(f"Found {len(my_repos)} repos. Starting with {args.workers} workers...\n")

counts = {"success": 0, "updated": 0, "failed": 0}

with ThreadPoolExecutor(max_workers=args.workers) as executor:
    futures = [executor.submit(clone_repo, repo) for repo in my_repos]
    for future in as_completed(futures):
        result = future.result()
        counts[result] += 1

print(f"\nDone — {len(my_repos)} repos: CLONED: {counts['success']}, UPDATED: {counts['updated']}, FAILED: {counts['failed']}")
