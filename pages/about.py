import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import CONFIG

dash.register_page(__name__, path="/about", name="About")

layout = dbc.Container([
    html.Div([
        html.H5(html.B("About the App"), className="mt-4", style={'color': '#000'}),
    ], style={"overflow": "hidden"}),
    
    # Main content container
    dbc.Row([
        dbc.Col([
            dbc.Container(
                [
                    html.P("This app helps analyze 4th down decisions using data-driven insights.", 
                           className="mb-3"),
                    html.P("Built by [Your Name].", className="mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.H6("Data Sources", className="mt-2 mb-2", style={'color': '#000'}),
                            html.Ul([
                                html.Li("CFB Data from [Source Name]"),
                                html.Li("Win Probability Models from [Source Name]"),
                            ], style={'padding-left': '20px', 'margin-bottom': '20px'})
                        ], width=6),
                        
                        dbc.Col([
                            html.H6("Methodology", className="mt-2 mb-2", style={'color': '#000'}),
                            html.Ul([
                                html.Li("4th down recommendations based on +1.5% WP threshold"),
                                html.Li("Plays in final 30 seconds excluded"),
                            ], style={'padding-left': '20px', 'margin-bottom': '20px'})
                        ], width=6)
                    ]),
                    
                    html.H6("Contact", className="mt-2 mb-2", style={'color': '#000'}),
                    html.P("For questions or feedback, please email: your@email.com")
                ],
                className="bg-white p-4",
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
