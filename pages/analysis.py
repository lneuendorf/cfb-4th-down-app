import dash
from dash import html
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(
    __name__, path="/analysis", name="Analysis", title="Analysis | CFB 4th Down"
)

CARD_STYLE = {
    "height": "100%",
}


def create_section_header(kicker, title, description):
    return html.Div(
        [
            html.Div(kicker, className="tendencies-section-kicker"),
            html.H2(title, className="analysis-section-title"),
            html.P(description, className="analysis-section-copy"),
        ],
        className="analysis-section-header",
    )


def create_model_card(
    image_path,
    title,
    description,
    link,
    badge_text=None,
    card_class_name="",
    card_number=None,
    image_class_name="",
):
    media = None
    if image_path:
        media = html.A(
            html.Div(
                html.Img(
                    src=image_path,
                    className=f"analysis-card-image {image_class_name}".strip(),
                ),
                className="analysis-card-image-wrap",
            ),
            href=link,
            target="_blank",
            className="analysis-card-media-link",
        )

    return dbc.Card(
        [
            media,
            dbc.CardBody(
                [
                    html.Div(card_number, className="analysis-card-number")
                    if card_number
                    else None,
                    html.H3(title, className="analysis-card-title"),
                    html.P(description, className="analysis-card-description"),
                    html.A(
                        "Continue →",
                        href=link,
                        target="_blank",
                        className="analysis-card-cta",
                    ),
                ],
                className="analysis-card-body",
            ),
        ],
        style=CARD_STYLE,
        className=f"analysis-card h-100 {card_class_name}".strip(),
    )


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Analysis", className="analysis-page-title"),
                html.P(
                    "Model notes, experiments, and methodology behind the fourth-down engine.",
                    className="analysis-page-intro",
                ),
            ],
            className="analysis-page-header mt-2",
        ),
        html.Section(
            [
                create_section_header(
                    "Start Here",
                    "Decision Engine",
                    "Understand how the full recommendation system fits together.",
                ),
                dbc.Card(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/images/4th_down_trends_white.png",
                                                    className="analysis-feature-image analysis-feature-image-light",
                                                ),
                                                html.Img(
                                                    src="/assets/images/4th_down_trends.png",
                                                    className="analysis-feature-image analysis-feature-image-dark",
                                                ),
                                            ]
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
                                    lg=4,
                                    className="analysis-feature-media",
                                ),
                                dbc.Col(
                                    dbc.CardBody(
                                        [
                                            html.H3(
                                                "Building a College Football 4th Down Decision Engine",
                                                className="analysis-feature-title",
                                            ),
                                            html.P(
                                                "A walkthrough of how the four-model engine evaluates go, punt, and field-goal decisions.",
                                                className="analysis-feature-copy",
                                            ),
                                            html.A(
                                                "Read more →",
                                                href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                                target="_blank",
                                                className="analysis-feature-link",
                                            ),
                                        ],
                                        className="analysis-feature-body",
                                    ),
                                    lg=8,
                                ),
                            ],
                            className="g-0 h-100",
                        )
                    ],
                    style=CARD_STYLE,
                    className="analysis-feature-card analysis-feature-card-primary",
                ),
            ],
            className="analysis-section",
        ),
        html.Div(className="tendencies-section-divider"),
        html.Section(
            [
                create_section_header(
                    "Core Models",
                    "Four Model Breakdowns",
                    "The components behind go, field-goal, punt, and game-state estimates.",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            create_model_card(
                                image_path=None,
                                title="Win Probability Model",
                                description="How the win probability model turns game context into estimated chances of winning.",
                                link="https://lukeneuendorf.substack.com/p/win-probability-model",
                                card_number="01",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path=None,
                                title="4th Down Conversion Probability",
                                description="How the fourth-down conversion model estimates the probability of converting and the factors that influence success.",
                                link="https://lukeneuendorf.substack.com/p/4th-down-conversion-probability-model",
                                card_number="02",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path=None,
                                title="Field Goal Probability",
                                description="How the field-goal model estimates make probability from kick distance, game context, and conditions.",
                                link="https://lukeneuendorf.substack.com/p/field-goal-probability-model",
                                card_number="03",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            create_model_card(
                                image_path=None,
                                title="Punt Return Yards",
                                description="How the punt model estimates field-position outcomes after kicks and returns.",
                                link="https://lukeneuendorf.substack.com/p/punt-return-yards-model",
                                card_number="04",
                            ),
                            xs=12,
                            md=6,
                            xl=3,
                            className="mb-3",
                        ),
                    ]
                ),
            ],
            className="analysis-section",
        ),
        html.Div(className="tendencies-section-divider"),
        html.Section(
            [
                create_section_header(
                    "Experiments",
                    "Related Project",
                    "Alternative approaches and side work explored during development.",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/monte_carlo_sim.png",
                                title="Building a Monte Carlo College Football Game Simulator (and Why I Stopped)",
                                description="A postmortem on a simulation-first approach and why the compute cost made it impractical.",
                                link="https://lukeneuendorf.substack.com/p/building-a-monte-carlo-college-football",
                                card_class_name="analysis-card-compact",
                                image_class_name="analysis-card-image-invert-light",
                            ),
                            xs=12,
                            lg=5,
                            xl=4,
                            className="mb-3",
                        ),
                    ]
                ),
            ],
            className="analysis-section",
        ),
        html.Div(className="tendencies-section-divider"),
        html.Section(
            [
                html.Div(
                    [
                        html.I(className="fas fa-newspaper"),
                        html.Span("More analysis articles coming soon."),
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
