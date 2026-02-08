#!/usr/bin/env python3
"""
upload_issues.py — Create GitHub issues from a local JSON file.

Reads new_issues.json (or a file passed via --input) and creates each issue
on GitHub, skipping any whose title already exists.

Usage:
  python3 scripts/upload_issues.py                    # reads new_issues.json
  python3 scripts/upload_issues.py --input my.json    # reads my.json
  python3 scripts/upload_issues.py --dry-run           # preview without creating

Input format (new_issues.json):
[
  {
    "title": "Short issue title",
    "body": "Detailed description with markdown...",
    "labels": ["bug", "enhancement"]
  }
]
"""

import argparse
import json
import subprocess
import sys
import time


REPO = "MaStanford/LLMCarGame"


def get_existing_issue_titles():
    """Fetch all existing issue titles from GitHub for dedup."""
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO, "--state", "all",
             "--limit", "1000", "--json", "title"],
            capture_output=True, text=True, check=True
        )
        issues = json.loads(result.stdout)
        return {issue["title"] for issue in issues}
    except subprocess.CalledProcessError as e:
        print(f"Error fetching existing issues: {e.stderr}")
        sys.exit(1)


def create_issue(title, body, labels):
    """Create a single GitHub issue via gh CLI."""
    cmd = ["gh", "issue", "create", "--repo", REPO,
           "--title", title, "--body", body]
    for label in labels:
        cmd.extend(["--label", label])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"  Created: {url}")
        return True
    else:
        print(f"  FAILED: {result.stderr.strip()}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload issues to GitHub from JSON")
    parser.add_argument("--input", "-i", default="new_issues.json",
                        help="Input JSON file (default: new_issues.json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would be created without creating")
    args = parser.parse_args()

    # Load input file
    try:
        with open(args.input, "r") as f:
            new_issues = json.load(f)
    except FileNotFoundError:
        print(f"Error: {args.input} not found.")
        print()
        print('Create it with this format:')
        print("""[
  {
    "title": "Issue title",
    "body": "Description of the issue...",
    "labels": ["bug"]
  }
]""")
        sys.exit(1)

    print(f"Found {len(new_issues)} issues in {args.input}")

    # Fetch existing titles for dedup
    if not args.dry_run:
        print("Fetching existing issues for dedup...")
    existing_titles = get_existing_issue_titles() if not args.dry_run else set()
    if not args.dry_run:
        print(f"Found {len(existing_titles)} existing issues on GitHub")
    print()

    created = 0
    skipped = 0

    for issue in new_issues:
        title = issue["title"]
        body = issue.get("body", "")
        labels = issue.get("labels", [])

        if title in existing_titles:
            print(f"SKIP (exists): {title}")
            skipped += 1
            continue

        if args.dry_run:
            print(f"DRY-RUN: Would create: {title}")
            if labels:
                print(f"         Labels: {', '.join(labels)}")
            print()
            continue

        print(f"Creating: {title}")
        if create_issue(title, body, labels):
            created += 1
        time.sleep(1)  # rate limit courtesy

    print()
    if args.dry_run:
        print(f"Dry run complete. {len(new_issues)} issues would be created (minus any existing).")
    else:
        print(f"Done. Created: {created}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
