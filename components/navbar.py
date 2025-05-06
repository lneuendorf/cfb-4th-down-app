import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    brand=html.B("CFB 4th Down", style={"fontSize": "28px"}),
    color="white",
    dark=False,
    children=[
        dbc.NavItem(dbc.NavLink("Teams", href="/team-tendencies")),
        dbc.NavItem(dbc.NavLink("Coachs", href="/coach-tendencies")),
        dbc.NavItem(dbc.NavLink("Plays", href="/game-decisions")),
        dbc.NavItem(dbc.NavLink("About", href="/")),
    ],
    sticky="top",
    style={
        "boxShadow": "0 1px 5px rgba(0,0,0,0.1)", 
    },
)

disclaimer_bar = dbc.Alert(
    "⚠️ Beta Release Disclaimer: Please note this is an early version and there may be data inconsistencies (yards to goal not matching play text). Use with caution.",
    color="secondary",
    style={
        "padding": "8px",
        "marginBottom": "0",
        "borderRadius": "0",
        "textAlign": "center",
        "fontSize": "14px"
    }
)

# Combine both components in a container
header = html.Div([
    navbar,
    disclaimer_bar
], style={"position": "sticky", "top": 0, "zIndex": 1000})