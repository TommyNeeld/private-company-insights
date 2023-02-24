"""
dash app for specter
"""

# import dash_auth
from dash import Dash
import dash_bootstrap_components as dbc
from layout import get_layout
from callbacks import callbacks

app = Dash(__name__, title="specter-app", external_stylesheets=[dbc.themes.BOOTSTRAP])

# TODO: add authentication back
# auth = dash_auth.BasicAuth(app, settings.VALID_USERNAME_PASSWORD_PAIRS)

server = app.server

app.layout = get_layout(app)
callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
