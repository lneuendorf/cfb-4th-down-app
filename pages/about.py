import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="About")

layout = dbc.Container(
    [
        # ======================
        # HERO
        # ======================
        html.Div(
            [
                html.H2(
                    html.B("College Football 4th-Down Decision Analytics"),
                    className="mt-4",
                    style={"color": "var(--text-color)"},
                ),
            ],
            style={"overflow": "hidden"},
        ),
        html.P(
            html.Em(
                "Did teams make the right call on fourth down? A data-driven look at decision-making through the lens of win probability."
            ),
            className="mb-4",
        ),
        html.Img(
            src="/assets/images/4th_down.jpg",
            style={"width": "100%", "height": "auto"},
            className="mb-4",
        ),
        html.P(
            [
                "This site evaluates every college football fourth-down decision through the lens of expected win probability. "
                "It reveals how often teams and coaches follow analytically optimal recommendations, and how much win probability "
                "is gained or lost when they do not."
            ]
        ),
        # ======================
        # MODEL OVERVIEW
        # ======================
        html.P(
            [
                html.B("How fourth-down recommendations are generated"),
                html.Br(),
                "For each fourth down, our machine learning decision engine evaluates the expected win probability "
                "of the three options: going for it, attempting a field goal, or punting. The recommendation is "
                "the option that maximizes expected win probability, considering both the likelihood and impact of each outcome.",
            ]
        ),
        html.P(
            [
                html.B("Example play:"),
                html.Br(),
                "Indiana vs Iowa, Week 5, 2025 – 4th & 1 at the Iowa 30, score 3–7, Q2 01:52, 80°F, wind 6 mph. "
                "The engine recommended 'Go For It', and Iowa ran Mark Gronowski for 2 yards to secure a first down, "
                "which aligned with the model's recommendation based on expected win probability.",
            ]
        ),
        html.P(
            [
                html.B("Key factors considered by the model:"),
                html.Br(),
                "The engine utilizes a range of contextual and statistical inputs to estimate outcomes and determine win probability.",
            ]
        ),
        html.Ul(
            [
                html.Li(
                    "Game state: score, time remaining, down, distance, field position"
                ),
                html.Li("Environmental conditions: weather, stadium elevation"),
                html.Li("Pregame betting line: point spread"),
                html.Li("Team strength metrics: Elo ratings and historical performance"),
            ]
        ),
        html.P(
            [
                "These inputs are processed through outcome models that estimate the probability of success for each option "
                "(e.g., 4th down conversion, field goal make, expected opponent field position after a punt). "
                "A win probability model then combines these outcomes to calculate the expected win probability for each decision. "
                "The option with the highest expected win probability is selected as the recommendation."
            ],
            className="mb-1",
        ),
        html.Img(
            src="/assets/images/architecture.png",
            style={
                "width": "100%",
                "max-width": "900px",
                "height": "auto",
                "display": "block",
                "margin": "0 auto",
                "box-sizing": "border-box",
                "padding-left": CONFIG["padding-left"],
                "padding-right": CONFIG["padding-right"],
            },
            className="mt-3 mb-4",
        ),
        html.P(
            [
                "You may notice that Iowa’s pregame Elo was higher than Indiana’s at the start of Week 5, 2025. "
                "This is because Elo is a running metric across seasons, and Iowa historically has been a stronger football program, "
                "giving them a higher baseline. After Indiana’s 20–15 win in this game, Indiana’s Elo jumped above Iowa’s, with values of 2784 vs 2747. "
                "Indiana went on to win the 2025–26 College Football season, finishing ranked #1 in the AP Top 25, while Iowa ended 9–4, ranked #17."
            ]
        ),
        # ======================
        # SITE OVERVIEW
        # ======================
        html.H3(
            html.B("What You Can Explore"),
            className="mt-4",
            style={"color": "var(--text-color)"},
        ),
        html.P(
            "The site is organized into several sections, accessible via the navigation bar:"
        ),
        html.Ol(
            [
                html.Li(
                    [
                        dcc.Link(
                            [
                                html.B("Teams"),
                                html.I(
                                    className="bi bi-link-45deg ms-1",
                                    style={"font-size": "0.9em"},
                                ),
                            ],
                            href="/team-tendencies",
                            style={"text-decoration": "none", "color": "inherit"},
                        ),
                        html.Br(),
                        "Team-level fourth-down tendencies across seasons, including how often teams follow model recommendations "
                        "and the cumulative win probability impact of their decisions.",
                    ]
                ),
                html.Br(),
                html.Li(
                    [
                        dcc.Link(
                            [
                                html.B("Coaches"),
                                html.I(
                                    className="bi bi-link-45deg ms-1",
                                    style={"font-size": "0.9em"},
                                ),
                            ],
                            href="/coach-tendencies",
                            style={"text-decoration": "none", "color": "inherit"},
                        ),
                        html.Br(),
                        "Coaching tendencies on fourth down, showing how individual coaches compare to peers and how "
                        "decision-making behavior evolves over time.",
                    ]
                ),
                html.Br(),
                html.Li(
                    [
                        dcc.Link(
                            [
                                html.B("Plays"),
                                html.I(
                                    className="bi bi-link-45deg ms-1",
                                    style={"font-size": "0.9em"},
                                ),
                            ],
                            href="/game-decisions",
                            style={"text-decoration": "none", "color": "inherit"},
                        ),
                        html.Br(),
                        html.B("Play-level detail for every fourth down decision:"),
                        html.Ul(
                            [
                                html.Li("Team and opponent Elo ratings"),
                                html.Li(
                                    "Full game context (score, quarter, time, distance, yards to goal)"
                                ),
                                html.Li("Expected win probability for each decision"),
                                html.Li(
                                    "Model recommendation vs. actual decision and play outcome"
                                ),
                            ]
                        ),
                        "This view can be used to identify the best and worst decisions by a team, or to sanity-check "
                        "whether a call aligned with the model recommendation.",
                    ]
                ),
                html.Br(),
                html.Li(
                    [
                        dcc.Link(
                            [
                                html.B("Analysis"),
                                html.I(
                                    className="bi bi-link-45deg ms-1",
                                    style={"font-size": "0.9em"},
                                ),
                            ],
                            href="/analysis",
                            style={"text-decoration": "none", "color": "inherit"},
                        ),
                        html.Br(),
                        "Longer-form writeups on the models powering the decision engine:",
                        html.Ul(
                            [
                                html.Li("Win probability model"),
                                html.Li("Fourth-down conversion probability model"),
                                html.Li("Field goal make probability model"),
                                html.Li("Punt yards-to-goal model"),
                            ]
                        ),
                        "This section also includes season-level analysis and trends toward aggressive or conservative behavior.",
                    ]
                ),
            ]
        ),
        # ======================
        # KEY METRICS
        # ======================
        html.H3(
            html.B("Key Metrics"),
            className="mt-4",
            style={"color": "var(--text-color)"},
        ),
        html.P(
            [
                "Across the ",
                dcc.Link(
                    html.B("Teams"),
                    href="/team-tendencies",
                    style={"color": "inherit", "text-decoration": "none"},
                ),
                " and ",
                dcc.Link(
                    html.B("Coaches"),
                    href="/coach-tendencies",
                    style={"color": "inherit", "text-decoration": "none"},
                ),
                " sections, several summary metrics are used:",
            ]
        ),
        html.Ul(
            [
                html.Li(
                    [
                        html.B("Go-For-It Rate When Recommended"),
                        html.Br(),
                        "The percentage of fourth downs where a team or coach goes for it when the model recommends doing so. "
                        "Higher values indicate greater alignment with analytically optimal decisions.",
                    ]
                ),
                html.Li(
                    [
                        html.B("Win Probability Lost Per Season"),
                        html.Br(),
                        "The total expected win probability forfeited when a team chooses a suboptimal option — effectively wins left on the table. "
                        "For example, a value of 25% corresponds to roughly a quarter of a win lost over the season due to fourth-down decisions.",
                    ]
                ),
                html.Br(),
            ]
        ),
        # ======================
        # DATA + CTA
        # ======================
        html.H3(
            html.B("Data"),
            className="mt-4",
            style={"color": "var(--text-color)"},
        ),
        html.P(
            [
                "All data used in this project is sourced from the ",
                html.A(
                    "CollegeFootballData",
                    href="https://collegefootballdata.com/",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
                " API using the ",
                html.A(
                    "cfbd-python",
                    href="https://github.com/CFBD/cfbd-python",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
                " Python package. Many thanks to the creators and maintainers of those resources.",
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
