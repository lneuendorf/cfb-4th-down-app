import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/analysis", name="Analysis")

layout = dbc.Container([
    html.Div([
        html.H3(html.B("Analysis"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),

    # Grey horizontal line
    html.Hr(style={"borderTop": "2px solid grey", "margin": "1rem 0"}, className="mb-4"),

    html.Div([
        html.P(
            "This section will host various analysis articles related to 4th down decisions, "
            "team tendencies, and model insights. Stay tuned for in-depth write-ups and visualizations "
            "that explore different facets of college football strategy.",
            style={"fontSize": "18px", "lineHeight": "1.6"}
        ),
    ], className="mb-5"),
    
    # Card Grid
    # dbc.Row([
    #     # Article 1: About the App
    #     dbc.Col([
    #         dbc.Card(
    #             [
    #                 dcc.Link(
    #                     html.Img(
    #                         src="/assets/writeup/4th_down.jpg",
    #                         className="card-img-top",
    #                         style={
    #                             "height": "250px", 
    #                             "objectFit": "cover",
    #                             "cursor": "pointer",
    #                             "borderRadius": "16px 16px 0 0"
    #                         }
    #                     ),
    #                     href="/about-app",
    #                     style={"textDecoration": "none"}
    #                 ),
    #                 dbc.CardBody([
    #                     dcc.Link(
    #                         html.H4("About the App", className="card-title"),
    #                         href="/about-app",
    #                         style={"textDecoration": "none", "color": "inherit"}
    #                     ),
    #                     html.P(
    #                         "Learn about 4th down decisions in college football and how this app helps analyze team strategies.",
    #                         className="card-text"
    #                     ),
    #                 ]),
    #             ],
    #             className="shadow-sm h-100",
    #             style={
    #                 "borderRadius": "16px",
    #                 "border": "none",
    #                 "transition": "transform 0.2s",
    #                 ":hover": {
    #                     "transform": "scale(1.02)",
    #                     "boxShadow": "0 5px 15px rgba(0,0,0,0.1)"
    #                 }
    #             }
    #         )
    #     ], xs=12, md=6, className="mb-4"),
        
    #     # Article 2: About the Models
    #     dbc.Col([
    #         dbc.Card(
    #             [
    #                 dcc.Link(
    #                     html.Img(
    #                         src="/assets/writeup/wisco_elo.png",
    #                         className="card-img-top",
    #                         style={
    #                             "height": "250px", 
    #                             "objectFit": "cover",
    #                             "cursor": "pointer",
    #                             "borderRadius": "16px 16px 0 0"
    #                         }
    #                     ),
    #                     href="/about-models",
    #                     style={"textDecoration": "none"}
    #                 ),
    #                 dbc.CardBody([
    #                     dcc.Link(
    #                         html.H4("About the Models", className="card-title"),
    #                         href="/about-models",
    #                         style={"textDecoration": "none", "color": "inherit"}
    #                     ),
    #                     html.P(
    #                         "Dive into the technical details of the five models powering the recommendations.",
    #                         className="card-text"
    #                     ),
    #                 ]),
    #             ],
    #             className="shadow-sm h-100",
    #             style={
    #                 "borderRadius": "16px",
    #                 "border": "none",
    #                 "transition": "transform 0.2s",
    #                 ":hover": {
    #                     "transform": "scale(1.02)",
    #                     "boxShadow": "0 5px 15px rgba(0,0,0,0.1)"
    #                 }
    #             }
    #         )
    #     ], xs=12, md=6, className="mb-4"),
    # ]),
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