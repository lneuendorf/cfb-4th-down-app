import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    brand="4th Down Decisions",
    brand_href="/team-tendencies",
    color="primary",
    dark=False,
    children=[
        dbc.NavItem(dbc.NavLink("Team Tendencies", href="/team-tendencies")),
        dbc.NavItem(dbc.NavLink("Game Decisions", href="/game-decisions")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
    ],
    sticky="top",
)