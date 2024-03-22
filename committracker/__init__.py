import dash
import dash_bootstrap_components as dbc
from .callbacks import register_callbacks
from .layout import create_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout(app)
register_callbacks(app)
