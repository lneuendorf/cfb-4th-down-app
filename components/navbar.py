import dash_bootstrap_components as dbc
from dash import html

theme_toggle_desktop = dbc.Button(
    html.I(id="theme-toggle-icon-desktop", className="bi bi-sun-fill"),
    id="theme-toggle-desktop",
    n_clicks=0,
    className="theme-toggle-btn theme-toggle-btn-dark d-none d-lg-inline-flex ms-lg-3",
    color="link",
)

theme_toggle_mobile = dbc.Button(
    html.I(id="theme-toggle-icon-mobile", className="bi bi-sun-fill"),
    id="theme-toggle-mobile",
    n_clicks=0,
    className="theme-toggle-btn theme-toggle-btn-dark d-inline-flex d-lg-none",
    color="link",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.Div(
                [
                    dbc.NavbarBrand(
                        html.Span(
                            [
                                html.Img(
                                    src="/assets/logos/logo_light_mode.png",
                                    alt="CFB 4th Down",
                                    className="app-navbar-logo app-navbar-logo-light",
                                ),
                                html.Img(
                                    src="/assets/logos/logo_dark_mode.png",
                                    alt="CFB 4th Down",
                                    className="app-navbar-logo app-navbar-logo-dark",
                                ),
                            ],
                            className="app-navbar-brand-wrap",
                        ),
                        href="/",
                    ),
                    html.Div(
                        [
                            theme_toggle_mobile,
                            dbc.NavbarToggler(id="navbar-toggler"),
                        ],
                        className="d-flex d-lg-none align-items-center gap-2",
                    ),
                ],
                className="d-flex w-100 justify-content-between align-items-center",
            ),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink("Teams", href="/team-tendencies", active="exact")
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "Coaches", href="/coach-tendencies", active="exact"
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Plays", href="/game-decisions", active="exact")
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Analysis", href="/analysis", active="exact")
                        ),
                        dbc.NavItem(theme_toggle_desktop),
                    ],
                    className="ms-auto align-items-lg-center",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="white",
    dark=False,
    fixed="top",
    expand="lg",
    className="app-navbar",
    style={"boxShadow": "0 1px 5px rgba(0,0,0,0.1)"},
)

header = html.Div(
    [navbar],
    style={"position": "fixed", "top": 0, "left": 0, "right": 0, "zIndex": 1000},
)
