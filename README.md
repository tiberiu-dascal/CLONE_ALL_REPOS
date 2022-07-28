# CLONE_ALL_REPOS is a tool that will allow users to clone all their current repositories available on github
## Requirements
- Github TOKEN
- User name
- Location

## Flow
1. First generate a list of all available repositories using curl: curl -i -H "Authorization: token $token" https://api.github.com/user/repos
2. (Optional) Save the previous call to a .json file
3. Parse the .json and grab all clone_urls
4. Iterate through all repos and clone them locally

