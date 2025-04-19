import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/coach-tendencies", name="Coach Tendencies")

layout = dbc.Container([
    html.H2("Coach Tendencies", className="mt-4"),
    html.P("Visualize and evaluate in-game 4th down decisions."),
    dcc.Graph(id="coach-tendency-graph", figure={}),
], fluid=True)