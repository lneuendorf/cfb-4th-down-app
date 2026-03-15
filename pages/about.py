import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="Home", title="CFB 4th Down")


layout = dbc.Container(
    [
        # Hero
        html.Section(
            [
                html.Div(
                    [
                        html.Img(
                            src="/assets/images/4th_down.jpg",
                            alt="Fourth down play",
                            className="about-hero-image",
                        ),
                        html.Div(className="about-hero-scrim"),
                        html.Div(
                            [
                                html.Div(
                                    "College Football 4th-Down Analytics",
                                    className="about-hero-kicker",
                                ),
                                html.H1(
                                    "See when teams and coaches made the right fourth-down call.",
                                    className="about-hero-title",
                                ),
                                html.P(
                                    "A data-driven look at fourth-down decision-making through the lens of expected win probability.",
                                    className="about-hero-subtitle",
                                ),
                            ],
                            className="about-hero-content",
                        ),
                    ],
                    className="about-hero about-hero-simple",
                )
            ],
            className="about-section about-section-hero",
        ),
        # What you can explore
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Overview", className="about-section-kicker"),
                        html.H2(
                            "What you can explore",
                            className="about-section-title",
                        ),
                        html.P(
                            "Use the site to compare decision-making across teams, coaches, and individual plays.",
                            className="about-section-copy",
                        ),
                    ],
                    className="about-section-heading",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Link(
                                html.Div(
                                    [
                                        html.Div("01", className="about-feature-number"),
                                        html.H3(
                                            "Teams",
                                            className="about-feature-title",
                                            style={"fontWeight": "700"},
                                        ),
                                        html.P(
                                            "Compare how often teams follow the model’s recommendation and how much win probability they gain or lose from fourth-down decisions.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-feature-card clickable-card",
                                ),
                                href="/team-tendencies",
                                style={"textDecoration": "none", "color": "inherit"},
                            ),
                            md=4,
                            className="mb-3 mb-md-0",
                        ),
                        dbc.Col(
                            dcc.Link(
                                html.Div(
                                    [
                                        html.Div("02", className="about-feature-number"),
                                        html.H3(
                                            "Coaches",
                                            className="about-feature-title",
                                            style={"fontWeight": "700"},
                                        ),
                                        html.P(
                                            "See which coaches are more aggressive or conservative, and how their decision-making changes over time.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-feature-card clickable-card",
                                ),
                                href="/coach-tendencies",
                                style={"textDecoration": "none", "color": "inherit"},
                            ),
                            md=4,
                            className="mb-3 mb-md-0",
                        ),
                        dbc.Col(
                            dcc.Link(
                                html.Div(
                                    [
                                        html.Div("03", className="about-feature-number"),
                                        html.H3(
                                            "Plays",
                                            className="about-feature-title",
                                            style={"fontWeight": "700"},
                                        ),
                                        html.P(
                                            "Inspect individual fourth-down decisions with full game context, model recommendations, and expected win probability by option.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-feature-card clickable-card",
                                ),
                                href="/game-decisions",
                                style={"textDecoration": "none", "color": "inherit"},
                            ),
                            md=4,
                            className="mb-3 mb-md-0",
                        ),
                    ],
                    className="g-3",
                ),
            ],
            className="about-section about-section-features",
        ),
        # Key metrics
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Key Metrics", className="about-section-kicker"),
                        html.H2(
                            "How to read the main metrics",
                        ),
                        html.P(
                            "These are the two main summary metrics used throughout the Teams and Coaches pages.",
                        ),
                    ],
                    className="about-section-heading",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.H3(
                                        "Go-For-It Rate When Recommended",
                                        className="about-metric-title",
                                        style={"fontWeight": "700"},
                                    ),
                                    html.P(
                                        "The percentage of model-recommended go situations where the team or coach actually went for it.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-metric-card",
                            ),
                            md=6,
                            className="mb-3 mb-md-0",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H3(
                                        "Win Probability Lost Per Season",
                                        className="about-metric-title",
                                        style={"fontWeight": "700"},
                                    ),
                                    html.P(
                                        "The total expected win probability given up by choosing a lower-value option on fourth down.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-metric-card",
                            ),
                            md=6,
                            className="mb-3 mb-md-0",
                        ),
                    ],
                    className="g-3",
                ),
            ],
            className="about-section about-section-metrics",
        ),
        # Data attribution
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Data", className="about-section-kicker"),
                        html.H2(
                            "Source and attribution",
                        ),
                        html.P(
                            [
                                "All data used in this project is sourced from the ",
                                html.A(
                                    "CollegeFootballData",
                                    href="https://collegefootballdata.com/",
                                    target="_blank",
                                    style={"textDecoration": "none"},
                                ),
                                " API using the ",
                                html.A(
                                    "cfbd-python",
                                    href="https://github.com/CFBD/cfbd-python",
                                    target="_blank",
                                    style={"textDecoration": "none"},
                                ),
                                " Python package.",
                            ],
                            className="mb-0",
                        ),
                    ],
                    className="about-section-heading",
                ),
            ],
            className="about-section about-section-data",
        ),
    ],
    fluid=True,
    style={
        "maxWidth": "1100px",
        "paddingLeft": CONFIG["padding-left"],
        "paddingRight": CONFIG["padding-right"],
        "paddingBottom": "2rem",
    },
    className="responsive-container about-page",
)
