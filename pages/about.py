import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About")

layout = dbc.Container([
    html.H2("About", className="mt-4"),
    html.P("This app helps analyze 4th down decisions using data-driven insights."),
    html.P("Built by [Your Name].")
], fluid=True)
