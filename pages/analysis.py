import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/analysis", name="Analysis")

layout = dbc.Container(
    [
        html.Div(
            [
                html.H3(html.B("Analysis"), className="mt-4", style={"color": "#000"}),
            ],
            style={"overflow": "hidden"},
        ),
        # Grey horizontal line
        html.Hr(
            style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"
        ),
        html.Div(
            [
                html.P(
                    "This section hosts various analysis articles related to 4th down decisions, "
                    "team tendencies, and model insights. Stay tuned for in-depth write-ups and visualizations "
                    "that explore different facets of college football strategy."
                ),
            ],
            className="mb-5",
        ),
        # Card Grid
        dbc.Row(
            [
                # Article 1: 4th Down Decision Engine Overview
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.A(
                                    html.Img(
                                        src="/assets/images/4th_down_trends.png",
                                        className="card-img-top img-fluid",
                                        style={
                                            "objectFit": "cover",
                                            "cursor": "pointer",
                                            "borderRadius": "16px 16px 0 0",
                                        },
                                    ),
                                    href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                    target="_blank",  # opens in new tab
                                    style={"textDecoration": "none"},
                                ),
                                dbc.CardBody(
                                    [
                                        html.A(
                                            html.H4(
                                                "Building a College Football 4th Down Decision Engine",
                                                className="card-title",
                                            ),
                                            href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                            target="_blank",
                                            style={
                                                "textDecoration": "none",
                                                "color": "inherit",
                                            },
                                        ),
                                        html.P(
                                            "Learn about the motivation, data sources, and modeling techniques behind the 4th down decision engine.",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                            style={
                                "borderRadius": "16px",
                                "border": "none",
                                "transition": "transform 0.2s",
                                ":hover": {
                                    "transform": "scale(1.02)",
                                    "boxShadow": "0 5px 15px rgba(0,0,0,0.1)",
                                },
                            },
                        )
                    ],
                    xs=12,
                    md=6,
                    className="mb-4",
                ),
                # Article 2: Win Probability Model
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.A(
                                    html.Img(
                                        src="/assets/images/wp_chart.png",
                                        className="card-img-top img-fluid",
                                        style={
                                            "objectFit": "cover",
                                            "cursor": "pointer",
                                            "borderRadius": "16px 16px 0 0",
                                        },
                                    ),
                                    href="https://lukeneuendorf.substack.com/p/win-probability-model",
                                    target="_blank",  # opens in new tab
                                    style={"textDecoration": "none"},
                                ),
                                dbc.CardBody(
                                    [
                                        html.A(
                                            html.H4(
                                                "Win Probability Model",
                                                className="card-title",
                                            ),
                                            href="https://lukeneuendorf.substack.com/p/win-probability-model",
                                            target="_blank",
                                            style={
                                                "textDecoration": "none",
                                                "color": "inherit",
                                            },
                                        ),
                                        html.P(
                                            "Discover how the win probability model was developed, its features, and evaluation results.",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                            style={
                                "borderRadius": "16px",
                                "border": "none",
                                "transition": "transform 0.2s",
                                ":hover": {
                                    "transform": "scale(1.02)",
                                    "boxShadow": "0 5px 15px rgba(0,0,0,0.1)",
                                },
                            },
                        )
                    ],
                    xs=12,
                    md=6,
                    className="mb-4",
                ),
                # Article 3: 4th Down Conversion Probability Model
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.A(
                                    html.Img(
                                        src="/assets/images/feature_importance_4th_down_proba.png",
                                        className="card-img-top img-fluid",
                                        style={
                                            "objectFit": "cover",
                                            "cursor": "pointer",
                                            "borderRadius": "16px 16px 0 0",
                                        },
                                    ),
                                    href="https://lukeneuendorf.substack.com/p/4th-down-conversion-probability-model",
                                    target="_blank",  # opens in new tab
                                    style={"textDecoration": "none"},
                                ),
                                dbc.CardBody(
                                    [
                                        html.A(
                                            html.H4(
                                                "4th Down Conversion Probability Model",
                                                className="card-title",
                                            ),
                                            href="https://lukeneuendorf.substack.com/p/4th-down-conversion-probability-model",
                                            target="_blank",
                                            style={
                                                "textDecoration": "none",
                                                "color": "inherit",
                                            },
                                        ),
                                        html.P(
                                            "Discover how the 4th down conversion probability model was developed, its features, and evaluation results.",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                            style={
                                "borderRadius": "16px",
                                "border": "none",
                                "transition": "transform 0.2s",
                                ":hover": {
                                    "transform": "scale(1.02)",
                                    "boxShadow": "0 5px 15px rgba(0,0,0,0.1)",
                                },
                            },
                        )
                    ],
                    xs=12,
                    md=6,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "max-width": "1000px",
        "padding-left": CONFIG["padding-left"],
        "padding-right": CONFIG["padding-right"],
        "padding-bottom": "1rem",
    },
    className="responsive-container",
)
