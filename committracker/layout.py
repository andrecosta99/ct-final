from dash import html, dcc
import dash_bootstrap_components as dbc
from .plugin_loader import load_plugins


PLUGIN_TITLES = {
    'git_statistics': 'Git Statistics',
    'branch_information': 'Branch Information',
    'commit_graph': 'Commit Graph',

}

def create_layout(app):
    plugins = load_plugins()
    plugin_options = [
        {'label': PLUGIN_TITLES.get(plugin, ' '.join(plugin.replace('_', ' ').title())), 'value': plugin}
        for plugin in plugins.keys()
    ]

    navbar = dbc.NavbarSimple(
        brand="Commit Tracker",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-4"
    )

    plugin_selector = dcc.Dropdown(
        id='plugin-selector',
        options=plugin_options,
        multi=True,
        placeholder='Select plugins...'
    )

    repo_input = dbc.Input(
        id='repo-input',
        type='text',
        placeholder='Enter repository URL or path...',
        className='me-2'
    )

    submit_button = dbc.Button(
        'Load Repository',
        id='load-repo-button',
        n_clicks=0,
        color="primary"
    )

    plugin_output_area = html.Div(id='plugin-output-area')

    layout = html.Div([
        navbar,
        dbc.Container(
            [
                dbc.Row([
                    dbc.Col(plugin_selector, md=8),
                    dbc.Col(submit_button, md=4)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(repo_input, md=12)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(plugin_output_area, md=12)
                ])
            ],
            fluid=True
        )
    ])

    return layout
