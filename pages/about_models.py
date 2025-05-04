import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/about-models", name="About the Models")

layout = dbc.Container([
    html.Div([
        html.H3(html.B("About the Models"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),

    html.Hr(style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        dcc.Markdown("""
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
                        - Offense's yards to goal  
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
                        Among all features, the current score differential and pregame Elo difference are the most influential in shaping the model's predictions.
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
                        ##### 3. Field Goal Model (Heckman Two-Stage Approach)
                        This model uses a **Heckman selection framework** to account for selection bias—teams don't attempt field goals at random (*p = 0.041*), so modeling only attempted kicks would skew results.

                        **Stage 1: Attempt Probability**  
                        A **probit regression** estimates the likelihood of a field goal attempt based on:
                        - **Game context**: Score differential, time remaining, pressure situations  
                        - **Field position**: Yards to goal (strong negative predictor)  
                        - **Environment**: Wind speed, playing surface, elevation  

                        **Stage 2: Make Probability**  
                        A **linear regression**, corrected using the **inverse Mills ratio** from stage 1. Key predictors include:
                        - **Distance** to goal (strongest negative effect)  
                        - **Pressure** situations (slightly reduce accuracy)  
                        - **Wind speed** (noticeably reduces accuracy)  

                        **Calibration**: The model is well-calibrated overall, though slightly underestimates success in low-probability scenarios (<35%) due to sparse data.
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/fg_calibration.png",
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
                        **Key Insight**: Distance is the dominant factor in predicting field goal success. However, incorporating contextual variables like pressure, wind, and elevation improves overall model performance, especially in edge cases.
                        """),
                        html.Div(
                            html.Img(
                                src="/assets/writeup/fg_proba.png",
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

                        dcc.Markdown("""
                        ##### 4. Punt Return Yards Model (XGBoost with Optuna Tuning)

                        This model predicts the **expected return yardline** after a punt using **XGBoost**, with hyperparameters optimized via **Optuna**. The goal is to learn how field position and game context influence where the receiving team takes over after a punt.

                        **Feature Categories**:
                        - **Field position**: Where the punting team ends the play  
                        - **Game context**: Score differential, percent of game elapsed, home/away  
                        - **Environment**: Surface type (e.g. grass), wind speed, precipitation, temperature, elevation, indoors/outdoors  
                        - **Team strength**: Pre-game Elo ratings of both teams  

                        The model performs well in capturing non-linear relationships between **punt location** and **return location**.
                        """),
                        
                        html.Div(
                            html.Img(
                                src="/assets/writeup/punt_feat_importance.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "maxWidth": "500px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),

                        dcc.Markdown("""
                        **Key Insight**:  
                        The **end yardline of the punt by the kicking team** is by far the most important feature, dominating the model's decisions. However, adding context such as weather and team strength modestly improves predictions in edge cases.
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/punt_plot.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "maxWidth": "600px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),

                        dcc.Markdown("""
                        The model clearly learns the relationship between **punt depth** and **return yardline**, closely capturing real-world patterns. This helps inform downstream decisions about expected field position when choosing to punt.
                        """),

                        dcc.Markdown("""
                        ##### 5. Fourth Down Conversion Probability Model (XGBoost + Optuna)

                        This model estimates the probability of converting a **fourth down attempt**, trained using **XGBoost** with **Optuna** hyperparameter optimization. It helps assess when going for it on fourth down is a smart decision, factoring in field position, game context, and environmental variables.

                        **Feature Categories**:
                        - **Play context**: Yards to go, field position (yards to goal), game time elapsed  
                        - **Game situation**: Score differential, home vs. away, pregame Elo difference  
                        - **Environment**: Wind speed, precipitation, and temperature  

                        The model leverages non-linear relationships between these features to accurately estimate conversion chances in a variety of scenarios.
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/4th_down_feat_importance.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "maxWidth": "500px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),

                        dcc.Markdown("""
                        **Key Insight**:  
                        **Yards to go** and **field position** are the strongest drivers of conversion probability. However, contextual features like **score differential**, **Elo ratings**, and **weather** refine predictions in edge cases—especially in late-game or extreme weather situations.
                        """),

                        html.Div(
                            html.Img(
                                src="/assets/writeup/4th_down_calibration.png",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "maxWidth": "600px",
                                    "borderRadius": "8px",
                                    "boxShadow": "0px 0px 6px rgba(0, 0, 0, 0.15)"
                                }
                            ),
                            style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                        ),
                        html.Br(),

                        dcc.Markdown("""
                        The model is well-calibrated across the probability spectrum, providing reliable estimates that are suitable for integration into decision models (e.g., win probability maximization).
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