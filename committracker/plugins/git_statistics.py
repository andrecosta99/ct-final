import logging
from git import Repo
from dash import html


# Analyze Git statistics from a repository's commit history
def extract_git_stats(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        # Collect commit dates
        commit_dates = [commit.committed_datetime for commit in commits]

        # Calculate total lines added and deleted
        total_lines_added = sum(commit.stats.total['insertions'] for commit in commits)
        total_lines_deleted = sum(commit.stats.total['deletions'] for commit in commits)

        # Compute average lines changed per commit
        average_lines_per_commit = ((total_lines_added + total_lines_deleted) / len(commits)) if commits else 0

        return {
            'total_commits': len(commits),
            'commit_dates': commit_dates,
            'average_lines_per_commit': average_lines_per_commit,
        }

    except Exception as e:
        logging.error(f'Error extracting git statistics: {e}')
        return {'error': str(e)}


# Display Git statistics in a Dash component
def display_git_statistics(repo_path):
    stats = extract_git_stats(repo_path)
    if 'error' in stats:
        return html.Div(f"Error: {stats['error']}")

    return html.Div([
        html.H5('General Statistics'),
        html.Ul([
            html.Li(f"Total Commits: {stats['total_commits']}"),
            html.Li(f"Average Lines per Commit: {stats['average_lines_per_commit']:.2f}")
        ]),
    ], className="mt-4")
