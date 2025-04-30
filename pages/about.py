import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/", name="About")

layout = dbc.Container([
    html.Div([
        html.H5(html.B("About"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),
    
    # Main content container
    dbc.Row([
        dbc.Col([
            dbc.Container(
                [
                    html.Div([
                        html.P("This page is currently under development and not yet complete.", 
                               className="lead text-center mb-4"),
                        html.P("We're working hard to bring you the best 4th down decision analysis.", 
                               className="text-center mb-5"),
                    ], style={'padding': '2rem'})
                ],
                className="bg-white p-4 text-center",
                style={
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "min-height": "400px"
                }
            )
        ], xs=12, className="mb-4")
    ])
], 
fluid=True,
style={
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
    "fontFamily": "Arial, sans-serif"
},
className="responsive-container"
)