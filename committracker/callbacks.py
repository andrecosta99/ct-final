from dash import Output, Input, State, html, callback_context
from dash.exceptions import PreventUpdate
from .utils import clone_remote_repo
from .plugin_loader import load_plugins
import dash_bootstrap_components as dbc

PLUGIN_TITLES = {
    'git_statistics': 'Git Statistics',
    'commit_graph': 'Commit Graph',
    'branch_information': 'Branch Information',

}

def register_callbacks(app):
    @app.callback(
        Output('plugin-output-area', 'children'),
        [Input('load-repo-button', 'n_clicks')],
        [State('repo-input', 'value'), State('plugin-selector', 'value')]
    )
    def update_plugin_output(n_clicks, repo_url, selected_plugins):
        if n_clicks is None or n_clicks < 1 or not repo_url or not selected_plugins:
            raise PreventUpdate

        repo_path = clone_remote_repo(repo_url)
        if repo_path is None:
            return [html.Div("Failed to clone the repository.")]

        plugins = load_plugins()
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
