import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/team-tendencies", name="Team Tendencies")

layout = dbc.Container([
    html.H2("Team Tendencies", className="mt-4"),
    html.P("Explore how different teams behave on 4th down."),
    # Placeholder content
    dcc.Graph(id="team-tendency-graph", figure={})
], fluid=True)