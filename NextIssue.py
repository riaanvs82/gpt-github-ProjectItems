import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SPEC_FILE = "specifications.md"
OUTPUT_BASE = "C:\\Source\\BalanceBot\\issues"


if not all([GITLAB_TOKEN, GITLAB_PROJECT_ID, OPENAI_API_KEY]):
    print("Please set GITLAB_TOKEN, GITLAB_PROJECT_ID and OPENAI_API_KEY in your .env file")
    exit(1)

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

client = OpenAI(api_key=OPENAI_API_KEY)

def read_specifications():
    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        return f.read()

def fetch_next_open_issue():
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/issues"
    params = {
        "state": "opened",
        "order_by": "created_at",
        "sort": "asc",
        "per_page": 1  # Get only the first (oldest open issue)
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    issues = response.json()
    return issues[0] if issues else None

def get_gpt_output(spec_text, issue_title, issue_description):
    prompt = (
        f"You are an embedded systems assistant helping with an open GitLab issue.\n"
        f"Project specification:\n{spec_text}\n\n"
        f"The current issue is:\nTitle: {issue_title}\nDescription: {issue_description}\n\n"
        "Please provide:\n"
        "1. A list of suggestions or subtasks\n"
        "2. Helpful background or research links if needed\n"
        "3. If relevant, one or more files to be created (code, docs, configs, etc.)\n\n"
        "When providing files, use the following format exactly:\n"
        "Filename: <filename.ext>\n"
        "---\n"
        "<file content>\n\n"
        "You may include multiple file blocks.\n"
        "Respond only with this output — no extra explanations or markdown code fences.\n"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def save_outputs(issue_title, gpt_output):
    # Create a clean folder name
    safe_name = "".join(c for c in issue_title if c.isalnum() or c in " _-").rstrip()
    issue_dir = os.path.join(OUTPUT_BASE, safe_name)
    os.makedirs(issue_dir, exist_ok=True)

    # Always save full GPT response
    gpt_file = os.path.join(issue_dir, "chatgpt.txt")
    with open(gpt_file, "w", encoding="utf-8") as f:
        f.write(gpt_output)
    print(f"✅ Saved GPT response to: {gpt_file}")

    # Pattern: Filename: <file.ext>\n---\n<content>
    pattern = r"Filename:\s*(.+?)\s*[-]+\s*\n(.*?)(?=(?:\nFilename:|$))"
    matches = re.findall(pattern, gpt_output, flags=re.DOTALL)

    if not matches:
        print("⚠️ No structured files found in GPT output.")
        return

    for filename, content in matches:
        filename = filename.strip()
        file_path = os.path.join(issue_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Created file: {file_path}")

def main():
    spec_text = read_specifications()
    issue = fetch_next_open_issue()

    if not issue:
        print("No open issues found.")
        return

    title = issue['title']
    desc = issue.get('description', '') or ''
    print(f"🔍 Working on issue: {title}")

    gpt_output = get_gpt_output(spec_text, title, desc)
    save_outputs(title, gpt_output)


if __name__ == "__main__":
    main()
