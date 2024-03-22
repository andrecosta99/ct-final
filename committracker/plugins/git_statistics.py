from git import Repo
from collections import Counter
from dash import html
import logging
import dash_bootstrap_components as dbc

# Analyze Git statistics from a repository's commit history
def extract_git_stats(repo_path):
    try:
        repo = Repo(repo_path)  # Load the repository
        commits = list(repo.iter_commits())  # List of all commits

        # Count contributions by author
        contributors = Counter(commit.author.name for commit in commits)
        # Collect commit dates
        commit_dates = [commit.committed_datetime for commit in commits]
        # Categorize commits by message content
        commit_types = Counter(categorize_commit_type(commit.message) for commit in commits)

        # Calculate total lines added and deleted
        total_lines_added = sum(commit.stats.total['insertions'] for commit in commits)
        total_lines_deleted = sum(commit.stats.total['deletions'] for commit in commits)

        # Compute average lines changed per commit
        average_lines_per_commit = (
            (total_lines_added + total_lines_deleted) / len(commits) if commits else 0
        )

        return {
            "total_commits": len(commits),
            "contributors": contributors,
            "commit_dates": commit_dates,
            "commit_types": commit_types,
            "average_lines_per_commit": average_lines_per_commit,
        }
    except Exception as e:
        return {"error": str(e)}

# Categorize commits into types based on the commit message
def categorize_commit_type(commit_message):
    if "fix" in commit_message.lower() or "bug" in commit_message.lower():
        return "Bug Fix"
    elif "feature" in commit_message.lower() or "add" in commit_message.lower():
        return "Feature"
    elif "doc" in commit_message.lower() or "readme" in commit_message.lower():
        return "Documentation"
    return "Other"

# Extract information about branches in a repository
def extract_branches_info(repo_path):
    try:
        repo = Repo(repo_path)  # Load the repository
        branches_info = {branch.name: sum(1 for _ in repo.iter_commits(branch)) for branch in repo.branches}
        return branches_info
    except Exception as e:
        logging.error(f"Error extracting branches information: {e}")
        return {"error": str(e)}

# Display Git statistics in a Dash component
def display_git_statistics(repo_path):
    stats = extract_git_stats(repo_path)  # Extract Git stats
    if "error" in stats:
        return html.Div(f"Error: {stats['error']}")  # Display error if any

    # Stats presentation
    return html.Div([
        html.H5("General Statistics"),
        html.P(f"Total Commits: {stats['total_commits']}"),
        html.P(f"Average Lines per Commit: {stats['average_lines_per_commit']}"),
        html.Div([
            html.H5("Contributors"),
            html.Ul([html.Li(f"{contributor}: {count}") for contributor, count in stats['contributors'].items()])
        ]),
        html.Div([
            html.H5("Commit Types"),
            html.Ul([html.Li(f"{ctype}: {count}") for ctype, count in stats['commit_types'].items()])
        ])
    ], className="mt-4")
