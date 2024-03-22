import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from git import Repo
from dash.exceptions import PreventUpdate

# Extract commits over time
def extract_commit_dates(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())
        commit_dates = [commit.committed_datetime for commit in commits]
        return commit_dates
    except Exception as e:
        return {"error": str(e)}

# Display commits over times
def display_commit_graph(repo_path):
    commit_dates = extract_commit_dates(repo_path)
    if "error" in commit_dates:
        raise PreventUpdate
    df = pd.DataFrame(
        {
            "Commit Date": pd.to_datetime(commit_dates, utc=True),
            "Commit Count": 1,
        }
    )
    df["Commit Date"] = df["Commit Date"].dt.tz_convert(None)
    df["Commit Date"] = df["Commit Date"].dt.date

    df_group = df.groupby("Commit Date").count().reset_index()

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

    return dcc.Graph(figure=fig)
