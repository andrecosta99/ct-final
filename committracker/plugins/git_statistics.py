from git import Repo
from collections import Counter
from dash import html
import logging
import dash_bootstrap_components as dbc



def extract_git_stats(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        contributors = Counter(commit.author.name for commit in commits)
        commit_dates = [commit.committed_datetime for commit in commits]
        commit_types = Counter(
            categorize_commit_type(commit.message) for commit in commits
        )

        total_lines_added = 0
        total_lines_deleted = 0
        for commit in commits:
            stats = commit.stats.total
            total_lines_added += stats['insertions']
            total_lines_deleted += stats['deletions']

        average_lines_per_commit = (
            (total_lines_added + total_lines_deleted) / len(commits)
            if commits else 0
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

def categorize_commit_type(commit_message):
    lower_msg = commit_message.lower()
    if "fix" in lower_msg or "bug" in lower_msg:
        return "Bug Fix"
    elif "feature" in lower_msg or "add" in lower_msg:
        return "Feature"
    elif "doc" in lower_msg or "readme" in lower_msg:
        return "Documentation"
    else:
        return "Other"

def extract_branches_info(repo_path):
    try:
        repo = Repo(repo_path)
        branches_info = {}
        for branch in repo.branches:
            branch_name = branch.name
            commits_count = sum(1 for _ in repo.iter_commits(branch))
            branches_info[branch_name] = commits_count
        return branches_info
    except Exception as e:
        logging.error(f"Error extracting branches information: {e}")
        return {"error": str(e)}

def display_git_statistics(repo_path):
    stats = extract_git_stats(repo_path)
    if "error" in stats:
        return html.Div(f"Error: {stats['error']}")


    return html.Div(
        dbc.Card(
            dbc.CardBody([
                html.H4("Git Statistics", className="card-title"),
                html.P(f"Total Commits: {stats['total_commits']}"),
                html.P(f"Average Lines per Commit: {stats['average_lines_per_commit']}"),
                html.Div([
                    html.H5("Contributors", className="card-subtitle"),
                    html.Ul([html.Li(f"{contributor}: {count}") for contributor, count in stats['contributors'].items()])
                ]),
                html.Div([
                    html.H5("Commit Types", className="card-subtitle"),
                    html.Ul([html.Li(f"{ctype}: {count}") for ctype, count in stats['commit_types'].items()])
                ])
            ]),
            className="mb-4"
        ),
        className="mt-4"
    )
