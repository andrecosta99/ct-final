from collections import Counter
from git import Repo
from dash import html


def extract_commit_types(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())
        commit_types = Counter(categorize_commit_type(commit.message) for commit in commits)
        return commit_types
    except Exception as e:
        return {"error": str(e)}

def categorize_commit_type(commit_message):
    commit_message = commit_message.lower()
    if "fix" in commit_message or "bug" in commit_message:
        return "Bug Fix"
    elif "feature" in commit_message or "add" in commit_message:
        return "Feature"
    elif "doc" in commit_message or "readme" in commit_message:
        return "Documentation"
    else:
        return "Other"

def display_commit_type(repo_path):
    commit_type = extract_commit_types(repo_path)
    if "error" in commit_type:
        return html.Div(f"Error: {commit_type['error']}")

    commit_types_list = html.Ul(
        [html.Li(f"{commit_type}: {count}") for commit_type, count in commit_type.items()]
    )

    return html.Div(
        [
            html.H5("Commits"),
            commit_types_list
        ],
        className="commit-types-container"
    )
