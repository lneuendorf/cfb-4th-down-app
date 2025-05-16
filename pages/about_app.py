import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/about-app", name="About the App")

layout = dbc.Container([
    html.Div([
        html.H3(html.B("About the App"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),

    # Add this note div
    html.Div(
        dbc.Alert(
            "Note: This documentation is currently a work in progress.",
            color="warning",
            style={
                "margin": "1rem 0",
                "borderLeft": "5px solid #ffc107",
                "backgroundColor": "#fff8e1",
                "color": "#856404"
            }
        ),
        className="mb-3"
    ),

    html.Hr(style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        dcc.Markdown("""
                        ### What is a 4th down decision?

                        In American football, each team has four attempts—called downs—to advance the ball 10 yards. 
                        If they fail to do so after four downs, they must turn the ball over to the opposing team. 
                        On 4th down, teams typically choose between three options:

                        - Punt the ball to the opposing team
                        - Attempt a field goal
                        - Try to convert the 4th down into a first down

                        Over the years, analysts have studied these decisions in depth, and much of the research shows 
                        that teams—especially in the NFL—tend to be too conservative. By punting or attempting field goals 
                        when they should go for it, teams often lose valuable win probability. While this topic has been 
                        well-explored in the NFL, there is far less public research focused on college football (CFB).

                        This app provides a way to visualize how CFB teams and coaches make 4th down decisions, and how 
                        those choices align with what a set of models recommend. It's important to note that the models are not perfect, 
                        and the underlying data has its limitations—but this tool offers insight into who is making the most (and least) data-aligned decisions.

                        ### How does the process work at a high level?

                        To generate a recommendation, five different models are used. 
                        The foundation is an Elo model—originally developed for ranking chess players—which estimates each team's overall strength. 
                        This Elo rating serves as an input feature in the other four models:

                        - A win probability model based on the current game state
                        - A 4th down conversion probability model
                        - A field goal success probability model
                        - A punt landing spot prediction model

                        For each possible decision—go for it, kick a field goal, or punt—the models estimate the expected win probability 
                        based on the game state after that choice is selected. The choice with the highest expected win probability is the recommended decision.
                        """),
                    ], style={"padding": "0rem", "margin": "0rem"})
                ]),
                className="shadow-sm",
                style={
                    "borderRadius": "16px",
                    "border": "none"
                }
            )
        ], xs=12)
    ])
], 
fluid=True,
style={
    "max-width": "1000px",
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
    "padding-bottom": "1rem",
},
className="responsive-container"
)