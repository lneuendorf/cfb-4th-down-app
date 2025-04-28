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
    # add box shadow
    style={
        "boxShadow": "0 1px 5px rgba(0,0,0,0.1)", 
        # "marginBottom": "20px",  # Ensure spacing from content
    },
)