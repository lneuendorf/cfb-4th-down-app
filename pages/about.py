import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="About")


def nav_link(label, href):
    return dcc.Link(
        [
            html.B(label),
            html.I(className="bi bi-link-45deg ms-1", style={"fontSize": "0.9em"}),
        ],
        href=href,
        style={"textDecoration": "none", "color": "inherit"},
    )


layout = dbc.Container(
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
                        html.H1(
                            "College Football 4th-Down Decision Analytics",
                            className="about-hero-title",
                        ),
                        html.P(
                            html.Em(
                                "Did teams make the right call on fourth down? A data-driven look at decision-making through the lens of win probability."
                            ),
                            className="about-hero-subtitle",
                        ),
                    ],
                    className="about-hero-content",
                ),
            ],
            className="about-hero",
        ),
        html.Div(
            [
                html.P(
                    "This site evaluates every college football fourth-down decision through the lens of expected win probability. "
                    "It reveals how often teams and coaches follow analytically optimal recommendations, and how much win probability "
                    "is gained or lost when they do not.",
                    className="mb-0",
                )
            ],
            className="about-intro-panel",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Model Overview", className="about-section-kicker"),
                        html.H2(
                            "How the recommendation engine works",
                            className="about-section-title",
                        ),
                    ],
                    className="about-section-heading",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            "For each fourth down, our machine learning decision engine evaluates the expected win probability of three options:",
                                            className="mb-2",
                                        ),
                                        html.Ol(
                                            [
                                                html.Li("Going for it"),
                                                html.Li("Attempting a field goal"),
                                                html.Li("Punting"),
                                            ],
                                            className="mb-2",
                                        ),
                                        html.P(
                                            "The recommendation is the option that maximizes expected win probability, considering both the likelihood (convert/don't convert, make/miss field goal) and impact of each outcome on win probability.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-story-card about-story-card-primary",
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Key factors considered by the model:",
                                            className="about-card-title",
                                            style={"fontWeight": "bold"},
                                        ),
                                        html.P(
                                            "The engine utilizes a range of contextual and statistical inputs to estimate outcomes and determine win probability.",
                                            className="mb-3",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "Game state: score, time remaining, down, distance, field position"
                                                ),
                                                html.Li(
                                                    "Environmental conditions: weather, stadium elevation"
                                                ),
                                                html.Li(
                                                    "Pregame betting line: point spread"
                                                ),
                                                html.Li(
                                                    "Team strength metrics: Elo ratings and historical performance"
                                                ),
                                            ],
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-story-card about-story-card-outline",
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Example play:",
                                            className="about-card-title",
                                            style={"fontWeight": "bold"},
                                        ),
                                        html.P(
                                            "Indiana vs Iowa, Week 5, 2025 – 4th & 1 at the Iowa 30, score 3–7, Q2 01:52, 80°F, wind 6 mph. "
                                            "The engine recommended 'Go For It', and Iowa ran Mark Gronowski for 2 yards to secure a first down, "
                                            "which aligned with the model's recommendation based on expected win probability.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="about-story-card about-story-card-accent",
                                ),
                            ],
                            lg=5,
                            className="mb-4 mb-lg-0",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            "Model architecture (with example play):",
                                            className="about-card-title",
                                            style={"fontWeight": "bold"},
                                        ),
                                        html.P(
                                            "These inputs are processed through outcome models that estimate the probability of success for each option "
                                            "(e.g., 4th down conversion, field goal make, expected opponent field position after a punt). "
                                            "A win probability model then combines these outcomes to calculate the expected win probability for each decision. "
                                            "The option with the highest expected win probability is selected as the recommendation.",
                                            className="about-diagram-copy",
                                        ),
                                        html.Img(
                                            src="/assets/images/architecture.png",
                                            alt="Model architecture diagram",
                                            className="about-architecture-image",
                                        ),
                                        html.P(
                                            "You may notice that Iowa’s pregame Elo was higher than Indiana’s at the start of Week 5, 2025. "
                                            "This is because Elo is a running metric across seasons, and Iowa historically has been a stronger football program, "
                                            "giving them a higher baseline. After Indiana’s 20–15 win in this game, Indiana’s Elo jumped above Iowa’s, with values of 2784 vs 2747. "
                                            "Indiana went on to win the 2025–26 College Football season, finishing ranked #1 in the AP Top 25, while Iowa ended 9–4, ranked #17.",
                                            className="about-diagram-note mb-0",
                                        ),
                                    ],
                                    className="about-diagram-panel",
                                )
                            ],
                            lg=7,
                        ),
                    ],
                    className="g-4",
                ),
            ],
            className="about-section about-section-story",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Site Overview", className="about-section-kicker"),
                        html.H2(
                            "What You Can Explore",
                            className="about-section-title",
                        ),
                        html.P(
                            "The site is organized into several sections, accessible via the navigation bar:",
                            className="about-section-copy",
                        ),
                    ],
                    className="about-section-heading",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div("01", className="about-feature-number"),
                                    html.H3(
                                        nav_link("Teams", "/team-tendencies"),
                                        className="about-feature-title",
                                    ),
                                    html.P(
                                        "Team-level fourth-down tendencies across seasons, including how often teams follow model recommendations "
                                        "and the cumulative win probability impact of their decisions.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-feature-card about-feature-card-team",
                            ),
                            md=6,
                            className="mb-3",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div("02", className="about-feature-number"),
                                    html.H3(
                                        nav_link("Coaches", "/coach-tendencies"),
                                        className="about-feature-title",
                                    ),
                                    html.P(
                                        "Coaching tendencies on fourth down, showing how individual coaches compare to peers and how "
                                        "decision-making behavior evolves over time.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-feature-card about-feature-card-coach",
                            ),
                            md=6,
                            className="mb-3",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div("03", className="about-feature-number"),
                                    html.H3(
                                        nav_link("Plays", "/game-decisions"),
                                        className="about-feature-title",
                                    ),
                                    html.P(
                                        html.B(
                                            "Play-level detail for every fourth down decision:"
                                        ),
                                        className="mb-2",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Team and opponent Elo ratings"),
                                            html.Li(
                                                "Full game context (score, quarter, time, distance, yards to goal)"
                                            ),
                                            html.Li(
                                                "Expected win probability for each decision"
                                            ),
                                            html.Li(
                                                "Model recommendation vs. actual decision and play outcome"
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    html.P(
                                        "This view can be used to identify the best and worst decisions by a team, or to sanity-check "
                                        "whether a call aligned with the model recommendation.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-feature-card about-feature-card-plays",
                            ),
                            lg=7,
                            className="mb-3",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div("04", className="about-feature-number"),
                                    html.H3(
                                        nav_link("Analysis", "/analysis"),
                                        className="about-feature-title",
                                    ),
                                    html.P(
                                        "Longer-form writeups on the models powering the decision engine:",
                                        className="mb-2",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Win probability model"),
                                            html.Li(
                                                "Fourth-down conversion probability model"
                                            ),
                                            html.Li("Field goal make probability model"),
                                            html.Li("Punt yards-to-goal model"),
                                        ],
                                        className="mb-3",
                                    ),
                                    html.P(
                                        "This section also includes season-level analysis and trends toward aggressive or conservative behavior.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-feature-card about-feature-card-analysis",
                            ),
                            lg=5,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),
            ],
            className="about-section about-section-features",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Reference Guide", className="about-section-kicker"),
                        html.H2("Key Metrics", className="about-section-title"),
                        html.P(
                            [
                                "Across the ",
                                dcc.Link(
                                    html.B("Teams"),
                                    href="/team-tendencies",
                                    style={
                                        "color": "inherit",
                                        "textDecoration": "none",
                                    },
                                ),
                                " and ",
                                dcc.Link(
                                    html.B("Coaches"),
                                    href="/coach-tendencies",
                                    style={
                                        "color": "inherit",
                                        "textDecoration": "none",
                                    },
                                ),
                                " sections, several summary metrics are used:",
                            ],
                            className="about-section-copy",
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
                                        style={"fontWeight": "bold"},
                                    ),
                                    html.P(
                                        "The percentage of fourth downs where a team or coach goes for it when the model recommends doing so. "
                                        "Higher values indicate greater alignment with analytically optimal decisions.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-metric-card about-metric-card-light",
                            ),
                            md=6,
                            className="mb-3",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H3(
                                        "Win Probability Lost Per Season",
                                        className="about-metric-title",
                                        style={"fontWeight": "bold"},
                                    ),
                                    html.P(
                                        "The total expected win probability forfeited when a team chooses a suboptimal option — effectively wins left on the table. "
                                        "For example, a value of 25% corresponds to roughly a quarter of a win lost over the season due to fourth-down decisions.",
                                        className="mb-0",
                                    ),
                                ],
                                className="about-metric-card about-metric-card-light",
                            ),
                            md=6,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),
            ],
            className="about-section about-section-metrics",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Data", className="about-section-kicker"),
                        html.H2(
                            "Source and attribution",
                            className="about-section-title",
                        ),
                    ],
                    className="about-section-heading",
                ),
                html.Div(
                    [
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
                                " Python package. Many thanks to the creators and maintainers of those resources.",
                            ],
                            className="mb-0",
                        )
                    ],
                    className="about-data-banner",
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
