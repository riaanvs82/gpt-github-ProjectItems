# GPT GitHub Project Items Assistant

A Python tool to automate GitHub Project management using OpenAI GPT.  
This project helps generate, suggest, and assist in completing GitHub Project Items based on project specifications, with AI-powered guidance.

---

## Features

- Generate GitHub Project Items from project specification files (Markdown).  
- Analyze and provide detailed suggestions or subtasks for open project items using GPT.  
- Save GPT outputs including code snippets, documentation drafts, and research notes.  
- Automatically organize outputs into folders per project item.  
- Supports labels/tags for project items to enhance organization.

---

## Prerequisites

- Specifications of your project saved in the `specifications.md` file.  
- A GPT prompt relevant to your project in the `prompt.txt` file.  
- Python 3.8 or higher  
- GitHub personal access token (PAT) with `repo` and `project` scopes  
- OpenAI API key  
- `.env` file configured with your tokens and project info (see below)

---

## Setup

1. Clone the repo:

   git clone https://github.com/yourusername/gpt-github-projectitems.git
   cd gpt-github-projectitems
   
2. Create a .env file in the root directory with the following:

   GITHUB_TOKEN=your_github_pat
   GITHUB_REPO=your_username/your_repository
   GITHUB_PROJECT_NUMBER=your_project_number
   OPENAI_API_KEY=your_openai_api_key

3. Install dependencies:

   pip install -r requirements.txt

---

## Usage

1. Generate issues from specifications:

    python generate_project_items_from_specs.py
 
2. Manually revise the newly created file - **issues.json** Adjust the specifications and prompt as needed.
 
3. Create the issues in your Github project

   python github_project_item_creator.py

4. Fetch next open issue and get GPT suggestions:

    python NextIssue.py
   
Outputs are saved under the issues/ directory of your project with subfolders for each issue.

---

## Project Structure
- specifications.md — Project specs file used to generate issues
- prompt.txt - Custom Prompt Template
- generate_project_items_from_specs.py — Script to create PjojectItems from specs
- gpt_fetch_next_issue.py — Script to fetch next open Github ProjectItem and generate GPT suggestions
- .env — Environment variables for API keys and config (not committed)
- ProjectItems/ — Output directory with GPT-generated suggestions and files

---

## Prompt
    prompt.txt — Custom Prompt Template

This file contains the template prompt used by the GPT model to generate issues from your specifications.md file.
The contents should be written in natural language with instructions to the AI on how to break down your project.
The prompt must include the placeholder {spec_text} where your project specification will be inserted dynamically.
You can adjust the wording in prompt.txt to control the tone, level of detail, or type of issues GPT generates.

---

## Notes
- Ensure your .env is never committed by adding it to .gitignore.
- Use GitLab project numeric ID or URL-encoded namespace/project path for GITLAB_PROJECT_ID.
- Update the prommpt.txt file as needed.
- Adjust the GPT model and temperature in scripts as needed.\
- This tool assumes issues are manageable and relatively small (1 day or less).
- The GPT output format supports multiple file outputs per issue, e.g., code, docs.

--- 
## License
MIT License © riaanvs
