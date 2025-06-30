import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "riaanvs82"
REPO_NAME = "gpt-gitlab-issue-assistant"
PROJECT_TITLE = "BalanceBot"  # Exactly as it appears on GitHub

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://api.github.com/graphql"

def get_repo_id():
    query = """
    query($owner:String!, $name:String!) {
      repository(owner: $owner, name: $name) {
        id
      }
    }
    """
    variables = {"owner": USERNAME, "name": REPO_NAME}
    res = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables})
    data = res.json()
    
    if "errors" in data:
        print("❌ GitHub API returned an error:")
        for error in data["errors"]:
            print(f"  - {error['message']}")
        print("\nCheck that USERNAME and REPO_NAME are correct.")
        exit(1)

    return data["data"]["repository"]["id"]


def get_project_id():
    query = """
    query($repoId: ID!) {
      node(id: $repoId) {
        ... on Repository {
          projectsV2(first: 20) {
            nodes {
              id
              title
            }
          }
        }
      }
    }
    """
    variables = {"repoId": repo_id}
    res = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables})
    data = res.json()

    if "errors" in data:
        print("❌ GitHub API returned an error:")
        for error in data["errors"]:
            print(f"  - {error['message']}")
        print("Check that the repo_id is correct and that you have access.")
        exit(1)

    projects = data["data"]["node"]["projectsV2"]["nodes"]

    if not projects:
        print("❌ No projects found in this repository.")
        print("➡️  Ensure you created a GitHub Project (Beta, 'Projects (V2)') in your repository.")
        exit(1)

    for p in projects:
        if p and p.get("title") == PROJECT_TITLE:
            return p["id"]

    print(f"❌ Project titled '{PROJECT_TITLE}' not found in repository.")
    print("Available project titles:")
    for p in projects:
        if p:
            print(f"  - {p.get('title', '(no title)')}")
    exit(1)


if __name__ == "__main__":
    repo_id = get_repo_id()
    project_id = get_project_id()

    print(f"GITHUB_REPO_ID={repo_id}")
    print(f"GITHUB_PROJECT_ID={project_id}")