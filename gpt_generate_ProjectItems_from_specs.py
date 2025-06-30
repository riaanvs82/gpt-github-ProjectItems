# === Script: generate_projectitems_from_specs.py ===
# Uses OpenAI's latest API to generate GitHub project item JSON from markdown spec file

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import re

# === LOAD .env ===
load_dotenv()

# === CONFIG ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SPEC_FILE = "specifications.md"
OUTPUT_FILE = "ProjectItems.json"

# === INITIALIZE OPENAI CLIENT ===
client = OpenAI(api_key=OPENAI_API_KEY)

# === READ SPECIFICATIONS ===
def read_specifications(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# === SIMPLE LABELS HEURISTIC ===
def assign_labels(issue):
    labels = []

    title = issue.get("title", "").lower()
    desc = issue.get("description", "").lower()

    # Technical vs non-technical
    tech_keywords = ["code", "arduino", "pixhawk", "motor", "controller", "integration", "gps", "test", "wire", "sensor"]
    doc_keywords = ["document", "readme", "docs", "write", "summary", "diagram"]
    research_keywords = ["research", "estimate", "investigate", "study", "analyze"]

    if any(k in title or k in desc for k in tech_keywords):
        labels.append("technical")
    if any(k in title or k in desc for k in doc_keywords):
        labels.append("documentation")
    if any(k in title or k in desc for k in research_keywords):
        labels.append("research")

    # Priority heuristic
    if "finalize" in title or "complete" in title:
        labels.append("high priority")

    return list(set(labels))  # unique labels

# === CALL OPENAI GPT ===
def generate_issues_from_spec(spec_text, prompt_file="prompt.txt"):
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{spec_text}", spec_text)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content

    # Remove ```json ... ``` if it somehow sneaks in
    content = re.sub(r"^```(?:json)?\s*|```$", "", content.strip(), flags=re.MULTILINE)

    try:
        issues = json.loads(content)
        return issues
    except json.JSONDecodeError:
        print("❌ GPT response could not be parsed as JSON:\n")
        print(content)
        return []

# === CONVERT raw issues to GitHub ProjectItems ===
def convert_to_project_items(raw_issues):
    project_items = []

    for i, issue in enumerate(raw_issues, 1):
        title = issue.get("title", f"Issue {i}")
        description = issue.get("description", "")

        # Compose body combining title + description for better detail
        body = f"### Issue Description\n\n{description}"

        labels = assign_labels(issue)

        project_item = {
            "title": title,
            "body": body,
            "labels": labels,
            # Optionally add more metadata fields here
        }
        project_items.append(project_item)

    return project_items

# === SAVE TO FILE ===
def save_project_items(items, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"✅ Project items saved to {output_path}")

# === MAIN ===
if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set in .env")
        exit(1)

    if not os.path.exists(SPEC_FILE):
        print(f"❌ Specification file '{SPEC_FILE}' not found.")
        exit(1)

    spec_text = read_specifications(SPEC_FILE)
    raw_issues = generate_issues_from_spec(spec_text)

    if raw_issues:
        project_items = convert_to_project_items(raw_issues)
        save_project_items(project_items, OUTPUT_FILE)
