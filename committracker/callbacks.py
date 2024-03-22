from dash import Output, Input, State, html, callback
from dash.exceptions import PreventUpdate
from .utils import clone_remote_repo  # Clone repository utility
from .plugin_loader import load_plugins  # Load plugins function
import dash_bootstrap_components as dbc  # Bootstrap components for Dash

# Plugin titles for UI display
PLUGIN_TITLES = {
    'git_statistics': 'Git Statistics',
    'commit_graph': 'Commit Graph',
    'branch_information': 'Branch Information',
}

# Callback for validating input fields
@callback(
    Output('url-error-message', 'children'),
    Output('plugin-error-message', 'children'),
    Input('load-repo-button', 'n_clicks'),
    State('repo-input', 'value'),
    State('plugin-selector', 'value'),
    prevent_initial_call=True
)
def validate_input(n_clicks, url, selected_plugins):
    url_error = ""
    plugin_error = ""
    if not url:
        url_error = "Please enter a repository URL."
    if not selected_plugins:
        plugin_error = "Please select at least one plugin."
    return url_error, plugin_error

# Registers callbacks for the app
def register_callbacks(app):
    @app.callback(
        Output('plugin-output-area', 'children'),
        [Input('load-repo-button', 'n_clicks')],
        [State('repo-input', 'value'), State('plugin-selector', 'value')]
    )
    def update_plugin_output(n_clicks, repo_url, selected_plugins):
        if n_clicks is None or n_clicks < 1 or not repo_url or not selected_plugins:
            raise PreventUpdate  # Stops callback from firing without valid input

        repo_path = clone_remote_repo(repo_url)  # Clones the Git repository
        if repo_path is None:
            return [html.Div("Failed to clone the repository.")]

        plugins = load_plugins()  # Loads the available plugins
        plugin_outputs = []
        for plugin_name in selected_plugins:
            plugin_function = plugins.get(plugin_name)
            if plugin_function:
                try:
                    plugin_output = plugin_function(repo_path)
                    card_title = PLUGIN_TITLES.get(plugin_name, plugin_name.replace('_', ' ').title())
                    card = dbc.Card(
                        [
                            dbc.CardHeader(card_title),
                            dbc.CardBody([plugin_output])
                        ],
                        className="mb-4"
                    )
                    plugin_outputs.append(card)
                except Exception as e:
                    plugin_outputs.append(html.Div(f"Error loading {plugin_name}: {e}"))

        return plugin_outputs
