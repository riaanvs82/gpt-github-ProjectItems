import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_PROJECT_ID = os.getenv("GITHUB_PROJECT_ID")
GITHUB_REPO_ID = os.getenv("GITHUB_REPO_ID")
PROJECTI_TEMS = "ProjectItems.json"

if not all([GITHUB_TOKEN, GITHUB_PROJECT_ID, GITHUB_REPO_ID]):
    print("❌ Missing required environment variables.")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://api.github.com/graphql"

def create_project_item(title, description):
    query = """
    mutation($projectId:ID!, $title:String!, $body:String!, $repoId:ID!) {
      createProjectV2ItemByRepository(input: {
        projectId: $projectId,
        content: {
          repositoryId: $repoId,
          title: $title,
          body: $body
        }
      }) {
        item {
          id
        }
      }
    }
    """

    variables = {
        "projectId": GITHUB_PROJECT_ID,
        "title": title,
        "body": description,
        "repoId": GITHUB_REPO_ID
    }

    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables})
    if response.status_code != 200:
        print("❌ GraphQL error:", response.text)
    else:
        print(f"✅ Created: {title}")

def main():
    with open(PROJECTI_TEMS, "r", encoding="utf-8") as f:
        issues = json.load(f)

    for issue in issues:
        title = issue.get("title")
        description = issue.get("description", "")
        if title:
            create_project_item(title, description)

if __name__ == "__main__":
    main()
