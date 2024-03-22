import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html
from dash.exceptions import PreventUpdate

from .plugin_loader import load_plugins  # Function to load available plugins
from .utils import clone_remote_repo  # Function to clone a Git repository

# Mapping of plugin identifiers to their display titles
PLUGIN_TITLES = {
    "git_statistics": "Git Statistics",
    "commit_graph": "Commit Graph",
    "branch_information": "Branch Information",
    "commit_type": "Commit Type",
    "contributors": "Project Contributers",
}

# Decorator to specify callback for input validation
@callback(
    Output("url-error-message", "children"),
    Output("plugin-error-message", "children"),
    Input("load-repo-button", "n_clicks"),
    State("repo-input", "value"),
    State("plugin-selector", "value"),
    prevent_initial_call=True,
)
# Function to validate the input fields
def validate_input(n_clicks, url, selected_plugins):
    url_error = ""
    plugin_error = ""
    # Check if the repository URL is entered
    if not url:
        url_error = "Please enter a repository URL."
    # Check if at least one plugin is selected
    if not selected_plugins:
        plugin_error = "Please select at least one plugin."
    # Return error messages
    return url_error, plugin_error

# Function to register callbacks in the app
def register_callbacks(app):
    # Decorator to specify callback for updating plugin output
    @app.callback(
        Output("plugin-output-area", "children"),
        [Input("load-repo-button", "n_clicks")],
        [State("repo-input", "value"), State("plugin-selector", "value")],
    )
    # Function to update the plugin output based on user interactions
    def update_plugin_output(n_clicks, repo_url, selected_plugins):
        # Prevent update if inputs are not valid
        if n_clicks is None or n_clicks < 1 or not repo_url or not selected_plugins:
            raise PreventUpdate

        # Display a loading message while data is being loaded
        loading_message = html.Div(
            "Data Updated",
            style={"textAlign": "center", "marginTop": "14px", "marginBottom": "20px"},
        )

        # Clone the Git repository
        repo_path = clone_remote_repo(repo_url)
        # Show error if repository cloning fails
        if repo_path is None:
            return [html.Div("Failed to clone the repository.")]

        # Load all available plugins
        plugins = load_plugins()
        # Begin with the loading message
        plugin_outputs = [loading_message]
        # Iterate over selected plugins and generate their outputs
        for plugin_name in selected_plugins:
            plugin_function = plugins.get(plugin_name)
            if plugin_function:
                try:
                    # Generate plugin output
                    plugin_output = plugin_function(repo_path)
                    # Get the title for the plugin
                    card_title = PLUGIN_TITLES.get(
                        plugin_name, plugin_name.replace("_", " ").title()
                    )
                    # Create a card to display the plugin output
                    card = dbc.Card(
                        [dbc.CardHeader(card_title), dbc.CardBody([plugin_output])],
                        className="mb-4",
                    )
                    # Append the card to the outputs
                    plugin_outputs.append(card)
                except Exception as e:
                    # Append error message if plugin loading fails
                    plugin_outputs.append(html.Div(f"Error loading {plugin_name}: {e}"))
        # Return all plugin outputs
        return plugin_outputs
