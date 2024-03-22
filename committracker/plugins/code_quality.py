import subprocess
from git import Repo
from dash import html
import os

def run_code_quality_analysis(repo_path):
    """
    Run code quality analysis using Flake8 on a given Git repository.

    Args:
        repo_path (str): Path to the Git repository.

    Returns:
        str: The output from the Flake8 analysis.
    """
    try:
        # Ensure the repository exists
        if not os.path.isdir(repo_path):
            raise Exception("Repository directory not found.")

        # Initialize the Git repository object
        repo = Repo(repo_path)
        if repo.bare:
            raise Exception("The Git repository is empty.")

        # Run Flake8 command
        result = subprocess.run(['flake8', repo_path], capture_output=True, text=True)

        # Return Flake8 output
        return result.stdout if result.stdout else "No issues found by Flake8."
    except Exception as e:
        return f'Error: {e}'

def display_code_quality(repo_path):
    """
    Display the Flake8 code quality analysis results for a Git repository in a Dash component.

    Args:
        repo_path (str): Path to the Git repository.

    Returns:
        dash.html.Div: A Dash component containing the Flake8 analysis report.
    """
    quality_report = run_code_quality_analysis(repo_path)
    return html.Div([
        html.H5('Code Quality Analysis (Flake8)'),
        html.Pre(quality_report, style={'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'})
    ])
