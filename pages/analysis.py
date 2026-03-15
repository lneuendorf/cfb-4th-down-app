import dash
from dash import html
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(
    __name__, path="/analysis", name="Analysis", title="Analysis | CFB 4th Down"
)

CARD_STYLE = {
    "borderRadius": "22px",
    "border": "none",
    "transition": "all 0.25s ease",
    "height": "100%",
    "backgroundColor": "var(--surface-bg)",
    "boxShadow": "0 10px 28px var(--shadow-color)",
}


def create_section_header(kicker, title, description):
    return html.Div(
        [
            html.Span(kicker, className="analysis-section-kicker"),
            html.H2(title, className="analysis-section-title"),
            html.P(description, className="analysis-section-copy"),
        ],
        className="analysis-section-header",
    )


def create_model_card(image_path, title, description, link, badge_text=None):
    badge = None
    if badge_text:
        badge = html.Span(badge_text, className="analysis-badge")

    return dbc.Card(
        [
            html.A(
                html.Div(
                    html.Img(
                        src=image_path,
                        className="analysis-card-image",
                    ),
                    className="analysis-card-image-wrap",
                ),
                href=link,
                target="_blank",
                className="analysis-card-media-link",
            ),
            dbc.CardBody(
                [
                    badge,
                    html.H3(title, className="analysis-card-title"),
                    html.P(description, className="analysis-card-description"),
                    html.A(
                        [
                            html.Span("Read more", className="analysis-card-cta-text"),
                            html.I(className="fas fa-arrow-right"),
                        ],
                        href=link,
                        target="_blank",
                        className="analysis-card-cta",
                    ),
                ],
                className="analysis-card-body",
            ),
        ],
        style=CARD_STYLE,
        className="analysis-card hover-card h-100",
    )


layout = dbc.Container(
    [
        html.Section(
            [
                html.Div(
                    [
                        html.Span("Analysis Library", className="analysis-hero-kicker"),
                        html.H1("Analysis", className="analysis-hero-title"),
                        html.P(
                            "This section hosts various analysis articles related to 4th down decisions, team tendencies, and model insights.",
                            className="analysis-hero-subtitle",
                        ),
                    ],
                    className="analysis-hero-copy",
                ),
            ],
            className="analysis-hero",
        ),
        html.Section(
            [
                create_section_header(
                    "Start Here",
                    "Featured Overview",
                    "Begin with the full decision-engine walkthrough before diving into the model-specific articles.",
                ),
                dbc.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        html.Img(
                                            src="/assets/images/4th_down_trends.png",
                                            className="analysis-feature-image",
                                        ),
                                        href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                        target="_blank",
                                        className="analysis-feature-image-link",
                                        style={
                                            "display": "block",
                                            "width": "100%",
                                            "height": "100%",
                                        },
                                    ),
                                    lg=5,
                                    className="analysis-feature-media",
                                ),
                                dbc.Col(
                                    dbc.CardBody(
                                        [
                                            html.Span(
                                                "Overview",
                                                className="analysis-badge",
                                            ),
                                            html.H3(
                                                "Building a College Football 4th Down Decision Engine",
                                                className="analysis-feature-title",
                                            ),
                                            html.P(
                                                "This article explains the methodology behind the decision engine, where four models combine to estimate expected win probability for going for it, punting, or attempting a field goal, while highlighting key modeling limitations.",
                                                className="analysis-feature-copy",
                                            ),
                                            html.A(
                                                [
                                                    html.I(
                                                        className="fas fa-external-link-alt"
                                                    ),
                                                    html.Span("Read more"),
                                                ],
                                                href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                                target="_blank",
                                                className="analysis-feature-link",
                                            ),
                                        ],
                                        className="analysis-feature-body",
                                    ),
                                    lg=7,
                                ),
                            ],
                            className="g-0 h-100",
                        )
                    ],
                    style=CARD_STYLE,
                    className="analysis-feature-card hover-card",
                ),
            ],
            className="analysis-section",
        ),
        html.Section(
            [
                create_section_header(
                    "Core Models",
                    "Model Deep Dives",
                    "Detailed explanations of the individual models powering the decision engine.",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/wp_chart.png",
                                title="Win Probability Model",
                                description="Discover how the win probability model was developed, its features, and evaluation results. Learn what factors most influence game outcomes.",
                                link="https://lukeneuendorf.substack.com/p/win-probability-model",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-4",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/feature_importance_4th_down_proba.png",
                                title="4th Down Conversion Probability",
                                description="Discover how the 4th down conversion probability model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/4th-down-conversion-probability-model",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-4",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/fg_pressure_rating.png",
                                title="Field Goal Probability",
                                description="Discover how the field goal probability model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/field-goal-probability-model",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-4",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/punt_model.png",
                                title="Punt Return Yards",
                                description="Discover how the punt return yards model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/punt-return-yards-model",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-4",
                        ),
                    ]
                ),
            ],
            className="analysis-section",
        ),
        html.Section(
            [
                create_section_header(
                    "Experiments",
                    "Related Projects",
                    "Experimental approaches and alternative methodologies explored during development.",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/monte_carlo_sim.png",
                                title="Building a Monte Carlo College Football Game Simulator (and Why I Stopped)",
                                description="An exploration of Monte Carlo simulation for football games. Despite promising potential, the simulator faced significant computational challenges - running 1000 simulations took 16 minutes, and evaluating all 156,472 fourth down decisions would require ~1.7 years of compute time. Learn valuable lessons about computational limitations and optimization strategies.",
                                link="https://lukeneuendorf.substack.com/p/building-a-monte-carlo-college-football",
                                badge_text="Case Study",
                            ),
                            xs=12,
                            lg=6,
                            xl=5,
                            className="mb-4",
                        ),
                    ]
                ),
            ],
            className="analysis-section",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.I(className="fas fa-newspaper"),
                        html.Span("More general analysis articles coming soon..."),
                    ],
                    className="analysis-coming-soon",
                )
            ],
            className="analysis-section analysis-section-last",
        ),
    ],
    fluid=True,
    style={
        "maxWidth": "1200px",
        "paddingLeft": CONFIG["padding-left"],
        "paddingRight": CONFIG["padding-right"],
        "paddingBottom": "2rem",
        "margin": "0 auto",
    },
    className="responsive-container analysis-page",
)
