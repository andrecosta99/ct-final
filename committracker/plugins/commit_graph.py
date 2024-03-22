import pandas as pd
import plotly.graph_objs as go
from dash import dcc

from .git_statistics import (
    extract_git_stats,  # Import the function to extract Git statistics
)


# Function to display a graph of commits over time for a given repository path
def display_commit_graph(repo_path):
    stats = extract_git_stats(repo_path)  # Extract Git statistics from the repository
    if "error" in stats:
        return dcc.Graph()  # Return an empty graph if there's an error in stats

    # Prepare data frame with commit dates
    df = pd.DataFrame(
        {
            "Commit Date": pd.to_datetime(
                [commit for commit in stats["commit_dates"]], utc=True
            ),
            "Commit Count": 1,
        }
    )
    df["Commit Date"] = df["Commit Date"].dt.tz_convert(
        None
    )  # Remove timezone information
    df["Commit Date"] = df["Commit Date"].dt.date  # Convert to date only

    # Group by date and count commits per day
    df_group = df.groupby("Commit Date").count().reset_index()

    # Create a Plotly graph object for displaying the data
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df_group["Commit Date"],
                y=df_group["Commit Count"],
                mode="lines+markers",
            )
        ]
    )
    fig.update_layout(title="", xaxis_title="Date", yaxis_title="Number of Commits")

    return dcc.Graph(figure=fig)  # Return the graph component with the commit data
