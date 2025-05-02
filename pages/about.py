import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="About")

layout = dbc.Container([
    html.Div([
        html.H3(html.B("About the App"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),

    # Grey horizontal line
    html.Hr(style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"),
    
    # Main Content
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

                        ### Model Deep Dive

                        This section dives into each of the models used to generate the recommendations.

                        ##### 1. Elo Model

                        The Elo model is a simple but effective rating system originally developed to rank chess players. 
                        In this project, it has been adapted to estimate the relative strength of college football teams.
                        For example, Wisconsin's ELO ratings are shown below.
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/wisco_elo.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "max-width": "800px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),
                                
                        dcc.Markdown("""
                        Each team starts the season with an initial Elo rating based on their division:
                        - **FBS**: 1500  
                        - **FCS**: 1300  
                        - **Division II**: 1000  
                        - **Division III**: 800  

                        After each game, team Elo ratings are updated based on the game outcome, score margin, and 
                        whether a team played at home. The formula used to update ratings is shown below:
                        """),
                        
                        html.Div(
                            html.Img(
                                src="/assets/writeup/elo_equation.png",
                                style={"width": "100%", "height": "auto", "max-width": "600px"}
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                                            
                        dcc.Markdown("""
                        Explanation of Terms:
                        - elo_h = Elo rating of the home team (add the HFA when calculating the away team's rating)
                        - K = 100 (learning rate)
                        - DIVISOR = 800 (controls sensitivity to Elo differences)
                        - HFA = 100 (home field advantage adjustment)
                        - home_result and away_result are 1 for a win, 0 for a loss, and 0.5 for a tie

                        These parameters were chosen by minimizing the log loss in score predictions across historical games, 
                        using data dating back to 1930.
                                     
                        ##### 2. Win Probability Model (WP)
                        The win probability model estimates a team's chance of winning at any moment during the game, given the current game state.
                        To capture this, the model uses the following features:
                        - Current score differential  
                        - Pregame Elo rating difference between offense and defense  
                        - Game location (home, away, or neutral)  
                        - Percentage of game elapsed (excluding potential overtime)  
                        - Offense’s yards to goal  
                        - Number of timeouts remaining for both offense and defense  

                        These features are input into an XGBoost model, with hyperparameters optimized using Optuna.
                        The result is a well-calibrated model, as illustrated below:
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/wp_calibration.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "max-width": "500px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),


                        dcc.Markdown("""
                        Among all features, the current score differential and pregame Elo difference are the most influential in shaping the model’s predictions.
                        This is reflected in the feature importance plot below:
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/wp_feat_importance.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "max-width": "600px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),

                        dcc.Markdown("""
                        ##### 2. Field Goal Model
                        
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