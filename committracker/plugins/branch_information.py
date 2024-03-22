import logging
from git import Repo
from dash import html

# Extract branches info
def extract_branches_info(repo_path):
    try:
        repo = Repo(repo_path)
        branches_info = {
            branch.name: sum(1 for _ in repo.iter_commits(branch))
            for branch in repo.branches
        }
        return branches_info
    except Exception as e:
        logging.error(f"Error extracting branches information: {e}")
        return {"error": str(e)}

# Display branches info
def display_branch_information(repo_path):
    branches_info = extract_branches_info(repo_path)
    if "error" in branches_info:
        return html.Div(f"Error: {branches_info['error']}")

    branches_list = html.Ul(
        [html.Li(f"{branch}: {commits} commits") for branch, commits in branches_info.items()]
    )

    return html.Div([html.H5("Branches"), branches_list])
