import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from dash.dash_table import DataTable
from config.config import CONFIG

dash.register_page(__name__, path="/game-decisions", name="Game Decisions")

# Load the data
df = pd.read_parquet("data/game_decisions.parquet")

# Get unique conferences and years for dropdowns
all_conferences = sorted(df['Offense Conference'].dropna().unique())
all_years = sorted(df['Season'].unique(), reverse=True)

layout = dbc.Container([
    html.Div([
        html.H5(html.B("Game Decisions"), className="mt-4", style={'color': '#000'}),
        html.P("Explore and evaluate in-game 4th down decisions."),
    ], style={"overflow": "hidden"}),
    html.P("Column Descriptions:"),
    html.Ul([
        html.Li([
            html.I("ELO:"),
            " Pregame team Elo rating, representing estimated team strength."
        ]),
        html.Li([
            html.I("YTG (Yards to Goal):"),
            " Distance from the line of scrimmage to the end zone."
        ]),
    ]),
    
    dbc.Container([
        # First row with Conference and Season dropdowns
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    # Conference Dropdown - make width responsive
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Conference:",
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "fontSize": "14px",
                                        "whiteSpace": "nowrap",
                                    }
                                ),
                                dcc.Dropdown(
                                    id='conference-dropdown',
                                    options=[{'label': conf, 'value': conf} for conf in all_conferences],
                                    value='Big Ten',
                                    placeholder="Select Conference",
                                    style={
                                        "minWidth": "150px",  # Reduced min width
                                        "width": "100%",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    }
                                ),
                            ],
                            className="me-2",
                            style={"flexWrap": "nowrap"}
                        ),
                        width="auto",
                        className="pe-1"
                    ),
                    
                    # Season Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Season:", 
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "whiteSpace": "nowrap",
                                        "fontSize": "14px"
                                    }
                                ),
                                dcc.Dropdown(
                                    id='year-dropdown',
                                    options=[{'label': str(year), 'value': year} for year in all_years],
                                    value=df['Season'].max(),
                                    placeholder="Select Season",
                                    style={
                                        "minWidth": "100px",
                                        "width": "100%",  # Make it fill available space
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    }
                                ),
                            ],
                            style={"flexWrap": "nowrap"},
                        ),
                        width="auto",
                        className="ps-1"
                    ),
                ], 
                justify="center",
                className="g-1"  # Reduce gap further
                ),
                className="mb-2"
            )
        ),
        
        # Second row with the other dropdowns
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    # Offense Team Dropdown - make more compact
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Offense:",
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "whiteSpace": "nowrap",
                                        "padding": "0 8px",
                                        "fontSize": "14px"
                                    }
                                ),
                                dcc.Dropdown(
                                    id='offense-team-dropdown',
                                    placeholder="Team",
                                    style={
                                        "minWidth": "150px",
                                        "width": "100%",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                    multi=False,
                                    value='Wisconsin',
                                ),
                            ],
                            className="me-1",  # Reduced margin
                            style={"flexWrap": "nowrap"}
                        ),
                        width="auto",
                        className="pe-1"
                    ),
                    
                    # Week Dropdown - make more compact
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Week:", 
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "padding": "0 8px",
                                        "whiteSpace": "nowrap",
                                        "fontSize": "14px"
                                    }
                                ),
                                dcc.Dropdown(
                                    id='week-dropdown',
                                    placeholder="Week",
                                    style={
                                        "minWidth": "70px",  # Reduced
                                        "width": "100%",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                    multi=False
                                ),
                            ],
                            className="me-1",
                            style={"flexWrap": "nowrap"},
                        ),
                        width="auto",
                        className="px-1"
                    ),
                    
                    # Recommendation Dropdown - make more compact
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Recommendation:",
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "whiteSpace": "nowrap",
                                        "padding": "0 6px",
                                        "fontSize": "14px"
                                    },
                                ),
                                dcc.Dropdown(
                                    id='recommendation-dropdown',
                                    placeholder="Select",
                                    style={
                                        "minWidth": "100px",  # Reduced
                                        "width": "100%",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                ),
                            ],
                            className="me-1",
                            style={"flexWrap": "nowrap"}
                        ),
                        width="auto",
                        className="pe-1"
                    ),
                    
                    # Decision Dropdown - make more compact
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Decision:",
                                    style={
                                        "height": "36px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                        "padding": "0 6px",
                                        "whiteSpace": "nowrap",
                                        "fontSize": "14px"
                                    }
                                ),
                                dcc.Dropdown(
                                    id='decision-dropdown',
                                    placeholder="Select",
                                    style={
                                        "minWidth": "100px",  # Reduced
                                        "width": "100%",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                    multi=False
                                ),
                            ],
                            style={"flexWrap": "nowrap"},
                        ),
                        width="auto",
                        className="ps-1"
                    ),
                ], 
                justify="center",
                className="g-1"  # Minimal gap
                ),
                className="mb-4"
            )
        )
    ], fluid=True, className="px-0"),
    
    dbc.Row([
        dbc.Col([
            dbc.Container([
                DataTable(
                    id='decision-table',
                    columns=[
                        {"name": ["", "Week"], "id": "Week", "type": "numeric"},
                        {"name": ["Offense", "Team"], "id": "Offense Team", "presentation": "markdown"},
                        {"name": ["Offense", "ELO"], "id": "Pregame Offense Elo", "type": "numeric"},
                        {"name": ["Offense", "Score"], "id": "Offense Score", "type": "numeric"},
                        {"name": ["Defense", "Team"], "id": "Defense Team", "presentation": "markdown"},
                        {"name": ["Defense", "ELO"], "id": "Pregame Defense Elo", "type": "numeric"},
                        {"name": ["Defense", "Score"], "id": "Defense Score", "type": "numeric"},
                        {"name": ["Game State", "Time"], "id": "Time"},
                        {"name": ["Game State", "Down & Dist"], "id": "Down & Distance"},
                        {"name": ["Game State", "YTG"], "id": "Yards to Goal", "type": "numeric"},
                        # New Win Probability columns
                        {"name": ["Expected Win Prob", "Go"], "id": "Win Probability Go", "type": "numeric", "format": {"specifier": ".2%"}},
                        {"name": ["Expected Win Prob", "Field Goal"], "id": "Win Probability Field Goal", "type": "numeric", "format": {"specifier": ".2%"}},
                        {"name": ["Expected Win Prob", "Punt"], "id": "Win Probability Punt", "type": "numeric", "format": {"specifier": ".2%"}},
                        # Play Outcome columns
                        {"name": ["Play Outcome", "Recommendation"], "id": "Recommendation"},
                        {"name": ["Play Outcome", "Decision"], "id": "Decision"},
                        {"name": ["Play Outcome", "Play Desc"], "id": "Desc"},
                    ],
                    page_size=20,
                    page_action='native',
                    sort_action='native',
                    filter_action='none',  # Disable the built-in filtering
                    merge_duplicate_headers=True,
                    style_table={
                        'overflowX': 'auto',
                        'height': '100%',
                        'minHeight': '400px',
                        'fontFamily': 'Arial, sans-serif',
                        'width': '100%',
                        'minWidth': 'none',
                    },
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'border': 'none',
                        'fontFamily': 'Arial, sans-serif',
                        'textAlign': 'center'
                    },
                    style_header_conditional=[
                        {
                            'if': {'header_index': 0},
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'borderBottom': '2px solid black'
                        },
                    ],
                    style_cell={
                        'textAlign': 'center',
                        'padding': '8px 10px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'border': 'none',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px',
                        'lineHeight': '1.3',
                        'minWidth': '80px',
                        'maxWidth': '300px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Desc'},
                            'minWidth': '200px',
                            'textAlign': 'left'
                        },
                        {
                            'if': {'column_id': 'Recommendation'},
                            'minWidth': '150px'
                        },
                        {
                            'if': {'column_id': 'Offense Team'},
                            'minWidth': '150px',
                            'textAlign': 'left'
                        },
                        {
                            'if': {'column_id': 'Defense Team'},
                            'minWidth': '150px',
                            'textAlign': 'left'
                        },
                        {
                            'if': {'column_id': 'Decision'},
                            'minWidth': '100px'
                        },
                        {
                            'if': {'column_id': ['Week', 'Pregame Offense Elo', 'Offense Score', 
                                            'Pregame Defense Elo', 'Defense Score', 'Yards to Goal']},
                            'textAlign': 'center'
                        },
                        # Add vertical borders between major sections
                        {
                            'if': {'column_id': 'Week'},
                            'borderRight': '2px solid #dee2e6'
                        },
                        {
                            'if': {'column_id': 'Offense Score'},
                            'borderRight': '2px solid #dee2e6'
                        },
                        {
                            'if': {'column_id': 'Defense Score'},
                            'borderRight': '2px solid #dee2e6'
                        },
                        {
                            'if': {'column_id': 'Yards to Goal'},
                            'borderRight': '2px solid #dee2e6'
                        },
                        {
                            'if': {'column_id': 'Win Probability Punt'},
                            'borderRight': '2px solid #dee2e6'
                        }
                    ],
                    style_data={
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px',
                        'lineHeight': '1.3'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    markdown_options={"html": True}
                )
            ],
            fluid=True, 
            className="p-0", 
            style={
                "borderRadius": "3px",
                "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
                "padding": "0px",
                "backgroundColor": "white",
                "overflow": "hidden",
                "width": "100%",
                "margin": "0 auto"
            })
        ], xs=12, className="mb-4 px-1 pb-1 pt-1", style={"overflow": "hidden"}),
    ])
], 
fluid=True,
style={
    "paddingLeft": CONFIG['padding-left'],
    "paddingRight": CONFIG['padding-right'],
    "fontFamily": "Arial, sans-serif",
    "width": "100%",
    "maxWidth": "none",
    "@media (max-width: 480px)": {
        "paddingLeft": "8px",
        "paddingRight": "8px"
    }
},
className="responsive-container"
)

@dash.callback(
    Output('offense-team-dropdown', 'options'),
    Output('week-dropdown', 'options'),
    Output('recommendation-dropdown', 'options'),
    Output('decision-dropdown', 'options'),
    Input('conference-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_dropdown_options(selected_conference, selected_year):
    dff = df[df['Season'] == selected_year]
    dff = dff[dff['Offense Conference'] == selected_conference]
    
    offense_teams = [{'label': team, 'value': team} for team in sorted(dff['Offense Team'].unique())]
    weeks = [{'label': week, 'value': week} for week in sorted(dff['Week'].unique())]
    
    # Only show these three options in recommendation dropdown
    recommendations = [
        {'label': 'Field Goal', 'value': 'Field Goal'},
        {'label': 'Go', 'value': 'Go'},
        {'label': 'Punt', 'value': 'Punt'}
    ]
    
    decisions = [{'label': dec, 'value': dec} for dec in sorted(dff['Decision'].unique())]
    
    return offense_teams, weeks, recommendations, decisions

@dash.callback(
    Output('decision-table', 'data'),
    Input('conference-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('offense-team-dropdown', 'value'),
    Input('week-dropdown', 'value'),
    Input('recommendation-dropdown', 'value'),
    Input('decision-dropdown', 'value')
)
def update_table(selected_conference, selected_year, selected_team, selected_week, selected_recommendation, selected_decision):
    dff = df[df['Season'] == selected_year]
    dff = dff[dff['Offense Conference'] == selected_conference]
    
    # Apply filters
    if selected_team:
        dff = dff[dff['Offense Team'] == selected_team]
    if selected_week:
        dff = dff[dff['Week'] == selected_week]
    if selected_recommendation:
        # Special handling for each recommendation type
        if selected_recommendation == 'Go':
            dff = dff[dff['Recommendation'].str.contains(r'\bGo\b', case=False, regex=True)]
        elif selected_recommendation == 'Field Goal':
            dff = dff[dff['Recommendation'].str.contains('Field Goal', case=False)]
        elif selected_recommendation == 'Punt':
            dff = dff[dff['Recommendation'].str.contains('Punt', case=False)]
    if selected_decision:
        dff = dff[dff['Decision'] == selected_decision]
    
    # Convert team names to markdown with logos
    dff['Offense Team'] = dff.apply(
        lambda x: f"<img src='{x['Offense Logo']}' style='height:30px; margin-right:5px;'> {x['Offense Team']}", 
        axis=1
    )
    dff['Defense Team'] = dff.apply(
        lambda x: f"<img src='{x['Defense Logo']}' style='height:30px; margin-right:5px;'> {x['Defense Team']}", 
        axis=1
    )

    return dff.to_dict('records')