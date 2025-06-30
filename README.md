# GPT GitLab Project Issues

A Python tool to automate GitLab issue management using OpenAI GPT.  
This project helps generate, suggest, and assist in completing GitLab issues based on project specifications, with AI-powered guidance.

---

## Features

- Generate GitLab issues from project specification files (Markdown).  
- Analyze and provide detailed suggestions or subtasks for open issues using GPT.  
- Save GPT outputs including code snippets, documentation drafts, and research notes.  
- Automatically organize outputs into folders per issue.  


---

## Prerequisites

- Specificatioons of your project saved in the specifications.md file.
- A GPT prompt relevant to your project in the prompt.txt file.
- Python 3.8 or higher  
- GitLab personal access token with API scope  
- OpenAI API key  
- `.env` file configured with your tokens and project info (see below)

---

## Setup

1. Clone the repo:

   git clone https://github.com/yourusername/gpt-gitlab-projectissues.git
   cd gpt-gitlab-projectissues

2. Create a .env file in the root directory with the following:

    GITLAB_TOKEN=your_gitlab_token
    GITLAB_PROJECT_ID=your_project_id_or_namespace%2Fproject_name
    OPENAI_API_KEY=your_openai_api_key

3. Install dependencies:

    pip install -r requirements.txt

## Usage

1. Generate issues from specifications:

    python gpt_generate_issues_from_specs.py
 
2. Manually revise the newly created file - **issues.json** Adjust the specifications and prompt as needed.
 
3. Create the issues in your GitLab project

    python gitlab_issue_creator.py

4. Fetch next open issue and get GPT suggestions:

    python NextIssue.py
Outputs are saved under the issues/ directory of your project with subfolders for each issue.

## Project Structure
- specifications.md — Project specs file used to generate issues
- prompt.txt - Custom Prompt Template
- gpt_generate_issues_from_specs.py — Script to create issues from specs
- gpt_fetch_next_issue.py — Script to fetch next open GitLab issue and generate GPT suggestions
- .env — Environment variables for API keys and config (not committed)
- issues/ — Output directory with GPT-generated suggestions and files

## Prompt
    prompt.txt — Custom Prompt Template

This file contains the template prompt used by the GPT model to generate issues from your specifications.md file.
The contents should be written in natural language with instructions to the AI on how to break down your project.
The prompt must include the placeholder {spec_text} where your project specification will be inserted dynamically.
You can adjust the wording in prompt.txt to control the tone, level of detail, or type of issues GPT generates.

## Notes
- Ensure your .env is never committed by adding it to .gitignore.
- Use GitLab project numeric ID or URL-encoded namespace/project path for GITLAB_PROJECT_ID.
- Update the prommpt.txt file as needed.
- Adjust the GPT model and temperature in scripts as needed.\
- This tool assumes issues are manageable and relatively small (1 day or less).
- The GPT output format supports multiple file outputs per issue, e.g., code, docs.

## License
MIT License © riaanvs