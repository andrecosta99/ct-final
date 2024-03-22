from collections import Counter
from git import Repo
from dash import html


# Extracts contributor data from a repository
def extract_contributors(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())
        contributors = Counter(commit.author.name for commit in commits)
        return contributors
    except Exception as e:
        return {'error': str(e)}


# Display contributors in a Dash component
def display_contributors(repo_path):
    contributors_data = extract_contributors(repo_path)
    if 'error' in contributors_data:
        return html.Div(f"Error: {contributors_data['error']}")

    contributors_list = html.Ul(
        [html.Li(f"{contributor}: {count}") for contributor, count in contributors_data.items()]
    )

    return html.Div([
        html.H5('Contributors'),
        contributors_list
    ], className="mt-4")
