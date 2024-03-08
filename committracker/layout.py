import dash_bootstrap_components as dbc
from dash import dcc, html


def create_layout(app):
    # Navbar
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="https://images.emojiterra.com/twitter/v13.1/512px/1f4c8.png",
                                height="30px",
                                style={"marginLeft": "20px"},
                            )
                        ),
                        dbc.Col(dbc.NavbarBrand("Commit Tracker", className="ml-2")),
                    ],
                    align="center",
                ),
                href="#",
            ),
        ],
        color="dark",
        dark=True,
    )

    content = dbc.Container(
        [
            dbc.Row(),
            dbc.Row(
                dbc.Col(
                    html.H5(
                        "Explore Git Repositories with Ease: In-Depth Analytics and Visual Insights",
                        className="text-center mb-4",
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(
                            "Enter a Git repository path or public URL",
                            className="align-self-center",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-repo",
                            type="text",
                            placeholder="Git repository local path or URL...",
                            style={"width": "100%", "border-radius": "5px"},
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        html.Button(
                            "Submit",
                            id="submit-val",
                            n_clicks=0,
                            className="btn btn-primary",
                            style={"border-radius": "5px"},
                        ),
                        width=3,
                        className="align-self-center",
                    ),
                ],
                align="center",
                className="my-2",
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[
                            dbc.Card(
                                [
                                    dbc.CardHeader("Commits Over Time"),
                                    dbc.CardBody(
                                        dcc.Graph(id="graph-commits-over-time")
                                    ),
                                ],
                                className="mb-4",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader("General Statistics"),
                                    dbc.CardBody(
                                        html.Div(
                                            id="stats-output", className="text-dark"
                                        )
                                    ),
                                ],
                                className="mb-4",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardHeader("Branches Statistics"),
                                    dbc.CardBody(
                                        html.Div(
                                            id="branches-info", className="text-dark"
                                        )
                                    ),
                                ],
                                className="mb-4",
                            ),
                        ],
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div("Commit Tracker 2024", className="text-center mt-4"),
                    width=12,
                )
            ),
        ],
        fluid=False,
        className="py-3 px-5",
    )
    layout = html.Div([navbar, content])
    return layout
