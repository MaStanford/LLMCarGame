import os
import re
import sys
import json
import time
import subprocess
import shutil

# Configuration
REPO_OWNER = "MaStanford"
REPO_NAME = "LLMCarGame"
GEMINI_MD_PATH = "GEMINI.md"

def get_existing_issues_gh_cli():
    """Fetches all open issues using GitHub CLI."""
    try:
        cmd = ["gh", "issue", "list", "--state", "all", "--limit", "1000", "--json", "title"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout)
        return {issue['title'] for issue in issues}
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issues via gh CLI: {e}")
        return set()
    except Exception as e:
        print(f"Error: {e}")
        return set()

def parse_markdown_tasks(file_path):
    """Parses checkbox tasks and their indented descriptions."""
    tasks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    current_section = None
    current_task = None
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Header detection
        if line.startswith("#"):
            current_section = line.lstrip("#").strip()
            current_task = None 
            continue
            
        # 2. New Task detection: - [ ] Title (MUST be at root of list, i.e. no leading space or very little)
        # We look for lines starting exactly with "- [ ]" or " - [ ]"
        task_match = re.match(r'^- \[ \] (.+)', line)
        if task_match:
            title_text = task_match.group(1).strip()
            # Clean title
            clean_title = title_text.replace("**", "").replace("__", "").replace(":", "")
            
            current_task = {
                "title": clean_title,
                "body_lines": [],
                "section": current_section
            }
            tasks.append(current_task)
            continue
            
        # 3. Body capture
        if current_task:
            # If the line is an empty line or indented, it belongs to the current task
            if stripped == "" or line.startswith(" ") or line.startswith("\t"):
                 current_task["body_lines"].append(line)
            else:
                 # It's a non-indented line that isn't a new task, end task context
                 current_task = None
                
    # Post-process tasks
    final_tasks = []
    for t in tasks:
        # Only sync tasks from "Open Tasks" section
        if t["section"] == "Open Tasks":
            body = "".join(t["body_lines"]).strip()
            # Add section footer
            footer = f"\n\n**Section:** {t['section']}"
            t["body"] = body + footer
            final_tasks.append(t)
            
    return final_tasks

def create_issue(task):
    """Creates an issue via gh CLI."""
    print(f"Creating issue: {task['title']}...")
    try:
        cmd = ["gh", "issue", "create", 
               "--title", task['title'],
               "--body", task['body'],
               "--label", "task"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Success: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue: {e.stderr}")
        return False

def main():
    if not shutil.which("gh"):
        print("Error: 'gh' CLI tool not found.")
        sys.exit(1)
        
    print(f"Reading {GEMINI_MD_PATH}...")
    tasks = parse_markdown_tasks(GEMINI_MD_PATH)
    print(f"Found {len(tasks)} main tasks in 'Open Tasks' section.")
    
    if not tasks:
        print("No tasks found to sync.")
        return

    existing_titles = get_existing_issues_gh_cli()
    print(f"Found {len(existing_titles)} existing issues on GitHub.")
    
    count = 0
    for task in tasks:
        if task['title'] in existing_titles:
            print(f"Skipping existing: {task['title']}")
            continue
        
        if create_issue(task):
            count += 1
            time.sleep(1)
            
    print(f"Done. Created {count} issues.")

if __name__ == "__main__":
    main()
