import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/game-decisions", name="Game Decisions")

layout = dbc.Container([
    html.H2("Game Decisions", className="mt-4"),
    html.P("Visualize and evaluate in-game 4th down decisions."),
    dcc.Graph(id="game-decision-graph", figure={})
], fluid=True)
