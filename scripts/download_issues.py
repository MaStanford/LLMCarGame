#!/usr/bin/env python3
"""
download_issues.py — Fetch all GitHub issues to a local JSON file.

Usage:
  python3 scripts/download_issues.py              # open issues only
  python3 scripts/download_issues.py --state all  # open + closed
  python3 scripts/download_issues.py -o my.json   # custom output file

Output: issues.json in the repo root (by default)
"""

import argparse
import json
import subprocess
import sys


REPO = "MaStanford/LLMCarGame"


def main():
    parser = argparse.ArgumentParser(description="Download GitHub issues to local JSON")
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"],
                        help="Issue state filter (default: open)")
    parser.add_argument("--output", "-o", default="issues.json",
                        help="Output file path (default: issues.json)")
    args = parser.parse_args()

    print(f"Fetching {args.state} issues from {REPO}...")

    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO,
             "--state", args.state, "--limit", "500",
             "--json", "number,title,body,state,labels,assignees,createdAt,updatedAt"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issues: {e.stderr}")
        sys.exit(1)

    issues = json.loads(result.stdout)
    issues.sort(key=lambda x: x["number"])

    with open(args.output, "w") as f:
        json.dump(issues, f, indent=2)

    print(f"Downloaded {len(issues)} issues to {args.output}")
    print()
    print("=== Issue Summary ===")
    for issue in issues:
        state = "OPEN" if issue["state"] == "OPEN" else "DONE"
        labels = ", ".join(l["name"] for l in issue.get("labels", []))
        label_str = f" [{labels}]" if labels else ""
        print(f"  #{issue['number']:>3}  {state:<4}  {issue['title']}{label_str}")


if __name__ == "__main__":
    main()
