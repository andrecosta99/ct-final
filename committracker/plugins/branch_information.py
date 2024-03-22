from dash import html
from .git_statistics import extract_branches_info  # Import the utility function to extract branch information

# Function to display branch information for a given repository path
def display_branch_information(repo_path):
    branches_info = extract_branches_info(repo_path)  # Extract branch info from the repository
    if "error" in branches_info:
        return html.Div(f"Error: {branches_info['error']}")  # Display error message if extraction fails

    # Create a list of branches with their commit counts
    branches_list = html.Ul([html.Li(f"{branch}: {commits} commits") for branch, commits in branches_info.items()])

    # Return the list within a div, titled "Branches"
    return html.Div([html.H5("Branches"), branches_list])
