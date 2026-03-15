import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="Home", title="CFB 4th Down")


layout = dbc.Container(
    [
        # Hero - Full width, touching navbar
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            className="hero-background",
                            style={
                                "backgroundImage": 'url("/assets/images/4th_down.jpg")',
                                "backgroundSize": "cover",
                                "backgroundPosition": "center 30%",
                                "position": "absolute",
                                "top": 0,
                                "left": 0,
                                "right": 0,
                                "bottom": 0,
                                "zIndex": 1,
                            },
                        ),
                        html.Div(
                            className="hero-overlay",
                            style={
                                "position": "absolute",
                                "top": 0,
                                "left": 0,
                                "right": 0,
                                "bottom": 0,
                                "backgroundColor": "rgba(0, 0, 0, 0.5)",  # Dark overlay for text contrast
                                "zIndex": 2,
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "College Football 4th-Down Analytics",
                                    className="about-hero-kicker",
                                    style={
                                        "fontSize": "clamp(0.9rem, 3vw, 1.2rem)",  # Responsive font
                                        "fontWeight": "700",
                                        "letterSpacing": "2px",
                                        "textTransform": "uppercase",
                                        "marginBottom": "clamp(0.5rem, 2vw, 1rem)",  # Responsive margin
                                        "position": "relative",
                                        "zIndex": 3,
                                    },
                                ),
                                html.H1(
                                    "A data-driven look at fourth-down decisions in college football.",
                                    className="about-hero-title",
                                    style={
                                        "fontSize": "clamp(1.8rem, 8vw, 3.5rem)",  # Responsive font (smaller on mobile)
                                        "fontWeight": "700",
                                        "lineHeight": "1.2",
                                        "marginBottom": "clamp(0.75rem, 2.5vw, 1.5rem)",  # Responsive margin
                                        "maxWidth": "800px",
                                        "position": "relative",
                                        "zIndex": 3,
                                    },
                                ),
                            ],
                            className="about-hero-content",
                            style={
                                "position": "relative",
                                "zIndex": 3,
                                "padding": "clamp(1.5rem, 4vw, 2.5rem)",
                                "maxWidth": "1100px",
                                "margin": "0 auto",
                                "width": "100%",
                                "boxSizing": "border-box",
                                "minHeight": "100%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "textAlign": "center",
                            },
                        ),
                    ],
                    className="about-hero-viewport",
                    style={
                        "position": "relative",
                        "width": "100vw",
                        "marginLeft": "calc(-50vw + 50%)",
                        "marginRight": "calc(-50vw + 50%)",
                        "overflow": "hidden",
                    },
                )
            ]
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
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/logos/team.png",
                                                    alt="Teams",
                                                    className="about-feature-icon",
                                                ),
                                                html.H3(
                                                    "Teams",
                                                    className="about-feature-title",
                                                    style={"fontWeight": "700"},
                                                ),
                                            ],
                                            className="about-feature-title-row",
                                        ),
                                        html.P(
                                            "Compare how often teams follow the model's recommendation and how much win probability they gain or lose from fourth-down decisions.",
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
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/logos/coach.png",
                                                    alt="Coaches",
                                                    className="about-feature-icon",
                                                ),
                                                html.H3(
                                                    "Coaches",
                                                    className="about-feature-title",
                                                    style={"fontWeight": "700"},
                                                ),
                                            ],
                                            className="about-feature-title-row",
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
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/logos/play.png",
                                                    alt="Plays",
                                                    className="about-feature-icon",
                                                ),
                                                html.H3(
                                                    "Plays",
                                                    className="about-feature-title",
                                                    style={"fontWeight": "700"},
                                                ),
                                            ],
                                            className="about-feature-title-row",
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
                        html.Div(
                            [
                                html.Span(
                                    "Key Metrics", className="about-section-kicker"
                                ),
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
                                                "The total expected win probability lost when teams choose not to go for it on fourth down when the model recommends going.",
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
                    className="about-section-band-inner",
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
                                "College football play-by-play data used in this project was sourced from the ",
                                html.A(
                                    "CollegeFootballData",
                                    href="https://collegefootballdata.com/",
                                    target="_blank",
                                    style={
                                        "textDecoration": "underline",
                                        "fontStyle": "italic",
                                    },
                                ),
                                " API using the ",
                                html.A(
                                    "cfbd-python",
                                    href="https://github.com/CFBD/cfbd-python",
                                    target="_blank",
                                    style={
                                        "textDecoration": "underline",
                                        "fontStyle": "italic",
                                    },
                                ),
                                " Python package. Models and analysis were developed independently. See ",
                                html.A(
                                    "Analysis",
                                    href="/analysis",
                                    target="_blank",
                                    style={
                                        "textDecoration": "underline",
                                        "fontStyle": "italic",
                                    },
                                ),
                                " tab for more details.",
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
        "paddingLeft": CONFIG["padding-left"],
        "paddingRight": CONFIG["padding-right"],
        "paddingTop": "0",
        "paddingBottom": "0rem",
    },
    className="responsive-container about-page",
)
