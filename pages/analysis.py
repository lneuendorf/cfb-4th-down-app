import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/analysis", name="Analysis")

# Custom card style with hover effect
CARD_STYLE = {
    "borderRadius": "16px",
    "border": "none",
    "transition": "all 0.3s ease",
    "height": "100%",
    "backgroundColor": "white",
    "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
}


# Hover effect will be applied via custom CSS class
# Add this to your assets/ folder as a .css file
def create_model_card(image_path, title, description, link, badge_text=None):
    """Helper function to create consistent model cards"""

    # Add badge if provided
    badge = None
    if badge_text:
        badge = html.Span(
            badge_text,
            className="badge mb-2",
            style={
                "backgroundColor": "#2c3e50",
                "color": "white",
                "fontSize": "0.75rem",
                "padding": "0.35rem 0.75rem",
                "borderRadius": "20px",
                "marginBottom": "0.75rem",
                "display": "inline-block",
            },
        )

    return dbc.Card(
        [
            # Image Container with overlay effect
            html.Div(
                html.A(
                    html.Img(
                        src=image_path,
                        className="card-img-top",
                        style={
                            "objectFit": "cover",
                            "height": "180px",
                            "width": "100%",
                            "transition": "transform 0.3s ease",
                        },
                    ),
                    href=link,
                    target="_blank",
                    style={
                        "textDecoration": "none",
                        "overflow": "hidden",
                        "display": "block",
                    },
                ),
                style={"overflow": "hidden", "borderRadius": "16px 16px 0 0"},
                className="card-image-container",
            ),
            dbc.CardBody(
                [
                    html.A(
                        html.Div(
                            [
                                # Optional badge
                                badge,
                                # Title
                                html.H5(
                                    title,
                                    className="card-title",
                                    style={
                                        "fontWeight": "600",
                                        "marginBottom": "0.75rem",
                                        "fontSize": "1.1rem",
                                    },
                                ),
                                # Description
                                html.P(
                                    description,
                                    className="card-text small",
                                    style={
                                        "color": "#666",
                                        "lineHeight": "1.5",
                                        "marginBottom": "1rem",
                                    },
                                ),
                                # Read More Link
                                html.Div(
                                    [
                                        html.Span(
                                            "Read more ",
                                            style={
                                                "color": "#2c3e50",
                                                "fontWeight": "500",
                                                "fontSize": "0.9rem",
                                            },
                                        ),
                                        html.I(
                                            className="fas fa-arrow-right",
                                            style={
                                                "color": "#2c3e50",
                                                "fontSize": "0.8rem",
                                            },
                                        ),
                                    ],
                                ),
                            ]
                        ),
                        href=link,
                        target="_blank",
                        style={
                            "textDecoration": "none",
                            "color": "#000",
                            "transition": "color 0.2s",
                        },
                    ),
                ],
                style={"padding": "1.25rem"},
            ),
        ],
        style=CARD_STYLE,
        className="hover-card h-100",
    )


layout = dbc.Container(
    [
        # Header Section
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
        # Introduction
        html.Div(
            [
                html.P(
                    "This section hosts various analysis articles related to 4th down decisions, "
                    "team tendencies, and model insights.",
                    className="lead",
                    style={"fontSize": "1.1rem", "lineHeight": "1.6"},
                ),
            ],
            className="mb-5",
        ),
        # Featured Article Section (Overview)
        html.Div(
            [
                html.H4(
                    [html.I(className="fas fa-star me-2"), "Featured Overview"],
                    className="mb-3",
                    style={"color": "#333", "fontWeight": "600"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.A(
                                                    html.Img(
                                                        src="/assets/images/4th_down_trends.png",
                                                        className="img-fluid rounded-start",
                                                        style={
                                                            "objectFit": "cover",
                                                            "height": "100%",
                                                            "width": "100%",
                                                            "borderRadius": "16px 0 0 16px",
                                                        },
                                                    ),
                                                    href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                                    target="_blank",
                                                    style={
                                                        "textDecoration": "none",
                                                        "height": "100%",
                                                        "display": "block",
                                                    },
                                                ),
                                                md=4,
                                                style={"padding": 0},
                                            ),
                                            dbc.Col(
                                                dbc.CardBody(
                                                    [
                                                        html.A(
                                                            html.Div(
                                                                [
                                                                    html.Span(
                                                                        "Overview",
                                                                        className="badge mb-2",
                                                                        style={
                                                                            "backgroundColor": "#2c3e50",
                                                                            "color": "white",
                                                                            "fontSize": "0.75rem",
                                                                            "padding": "0.35rem 0.75rem",
                                                                            "borderRadius": "20px",
                                                                        },
                                                                    ),
                                                                    html.H3(
                                                                        "Building a College Football 4th Down Decision Engine",
                                                                        className="card-title h5",
                                                                        style={
                                                                            "fontWeight": "600",
                                                                            "marginBottom": "0.75rem",
                                                                        },
                                                                    ),
                                                                    html.P(
                                                                        "This article explains the methodology behind the decision engine, walking through how four separate models work together to calculate expected win probability for going for it, punting, or attempting a field goal. Using a real example from Iowa-Indiana, it demonstrates how the engine processes game context to make recommendations while also acknowledging important limitations—from oversimplified outcome modeling to the lack of uncertainty quantification that would help coaches understand risk alongside reward.",
                                                                        className="card-text",
                                                                        style={
                                                                            "color": "#555",
                                                                            "marginBottom": "1rem",
                                                                        },
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            html.I(
                                                                                className="fas fa-external-link-alt me-2",
                                                                                style={
                                                                                    "fontSize": "0.8rem"
                                                                                },
                                                                            ),
                                                                            "Read more",
                                                                        ],
                                                                        style={
                                                                            "color": "#2c3e50",
                                                                            "fontWeight": "500",
                                                                        },
                                                                    ),
                                                                ]
                                                            ),
                                                            href="https://lukeneuendorf.substack.com/p/building-a-college-football-4th-down",
                                                            target="_blank",
                                                            style={
                                                                "textDecoration": "none",
                                                                "color": "#000",
                                                                "transition": "color 0.2s",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                                md=8,
                                            ),
                                        ],
                                        className="g-0",
                                        style={"height": "100%"},
                                    ),
                                ],
                                style={
                                    **CARD_STYLE,
                                    "borderRadius": "16px",
                                    "overflow": "hidden",
                                },
                                className="hover-card",
                            ),
                            xs=12,
                        ),
                    ]
                ),
            ],
            className="mb-5",
        ),
        # Model Deep Dives Section
        html.Div(
            [
                html.H4(
                    [html.I(className="fas fa-chart-line me-2"), "Model Deep Dives"],
                    className="mb-3",
                    style={"color": "#333", "fontWeight": "600"},
                ),
                html.P(
                    "Detailed explanations of the individual models powering the decision engine",
                    className="text-muted mb-4",
                    style={
                        "fontSize": "0.95rem",
                        "padding-left": CONFIG["padding-left"],
                        "padding-right": CONFIG["padding-right"],
                    },
                ),
                dbc.Row(
                    [
                        # Article 2: Win Probability Model
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/wp_chart.png",
                                title="Win Probability Model",
                                description="Discover how the win probability model was developed, its features, and evaluation results. Learn what factors most influence game outcomes.",
                                link="https://lukeneuendorf.substack.com/p/win-probability-model",
                            ),
                            xs=12,
                            md=6,
                            lg=4,
                            className="mb-4",
                        ),
                        # Article 3: 4th Down Conversion Probability Model
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/feature_importance_4th_down_proba.png",
                                title="4th Down Conversion Probability",
                                description="Discover how the 4th down conversion probability model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/4th-down-conversion-probability-model",
                            ),
                            xs=12,
                            md=6,
                            lg=4,
                            className="mb-4",
                        ),
                        # Article 4: Field Goal Probability Model
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/fg_pressure_rating.png",
                                title="Field Goal Probability",
                                description="Discover how the field goal probability model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/field-goal-probability-model",
                            ),
                            xs=12,
                            md=6,
                            lg=4,
                            className="mb-4",
                        ),
                        # Article 5: Punt Return Yards Model
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/punt_model.png",
                                title="Punt Return Yards",
                                description="Discover how the punt return yards model was developed, its features, and evaluation results.",
                                link="https://lukeneuendorf.substack.com/p/punt-return-yards-model",
                            ),
                            xs=12,
                            md=6,
                            lg=4,
                            className="mb-4",
                        ),
                    ]
                ),
            ],
            className="mb-5",
        ),
        # Related Projects Section (New)
        html.Div(
            [
                html.H4(
                    [html.I(className="fas fa-project-diagram me-2"), "Related Projects"],
                    className="mb-3",
                    style={"color": "#333", "fontWeight": "600"},
                ),
                html.P(
                    "Experimental approaches and alternative methodologies explored during development",
                    className="text-muted mb-4",
                    style={
                        "fontSize": "0.95rem",
                        "padding-left": CONFIG["padding-left"],
                        "padding-right": CONFIG["padding-right"],
                    },
                ),
                dbc.Row(
                    [
                        # New Monte Carlo Simulator Article
                        dbc.Col(
                            create_model_card(
                                image_path="/assets/images/monte_carlo_sim.png",  # You'll need to add this image
                                title="Building a Monte Carlo College Football Game Simulator (and Why I Stopped)",
                                description="An exploration of Monte Carlo simulation for football games. Despite promising potential, the simulator faced significant computational challenges - running 1000 simulations took 16 minutes, and evaluating all 156,472 fourth down decisions would require ~1.7 years of compute time. Learn valuable lessons about computational limitations and optimization strategies.",
                                link="https://lukeneuendorf.substack.com/p/building-a-monte-carlo-college-football",
                                badge_text="Case Study",
                            ),
                            xs=12,
                            md=6,
                            lg=4,
                            className="mb-4",
                        ),
                    ]
                ),
            ],
            className="mb-5",
        ),
        # Coming Soon Section
        html.Div(
            [
                html.Hr(style={"borderTop": "1px solid #ddd", "margin": "2rem 0"}),
                html.Div(
                    [
                        html.I(
                            className="fas fa-newspaper me-2", style={"color": "#666"}
                        ),
                        html.Span(
                            "More general analysis articles coming soon...",
                            style={"color": "#666", "fontStyle": "italic"},
                        ),
                    ],
                    className="text-center py-4",
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "max-width": "1200px",
        "padding-left": CONFIG["padding-left"],
        "padding-right": CONFIG["padding-right"],
        "padding-bottom": "2rem",
        "margin": "0 auto",
    },
    className="responsive-container",
)
