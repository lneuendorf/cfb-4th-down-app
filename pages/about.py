import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="About")

layout = dbc.Container([
    html.Div([
        html.H3(html.B("About"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),

    # Grey horizontal line
    html.Hr(style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"),
], 
fluid=True,
style={
    "max-width": "1000px",
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
    "padding-bottom": "1rem",
},
className="responsive-container"
)