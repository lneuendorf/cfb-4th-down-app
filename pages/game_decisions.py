import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from dash.dash_table import DataTable
from config.config import CONFIG

dash.register_page(__name__, path="/game-decisions", name="Game Decisions")

# Load the data
df = pd.read_parquet("data/plays_tendencies.parquet")

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
            html.U("ELO:"),
            " Pregame team Elo rating, representing estimated team strength."
        ]),
        html.Li([
            html.U("YTG (Yards to Goal):"),
            " Distance from the line of scrimmage to the end zone."
        ]),
    ]),
    
    dbc.Container([
        # First row with Conference and Season dropdowns
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    # Conference Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Conference:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='conference-dropdown',
                                    options=[{'label': conf, 'value': conf} for conf in all_conferences],
                                    value='Big Ten',
                                    placeholder="Select Conference",
                                    style={"minWidth": "200px", "height": "36px"}
                                ),
                            ],
                            className="me-2"  # Add right margin to separate from next group
                        ),
                        width="auto",
                        className="pe-1"  # Add right padding
                    ),
                    
                    # Season Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Season:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='year-dropdown',
                                    options=[{'label': str(year), 'value': year} for year in all_years],
                                    value=2024,
                                    placeholder="Select Season",
                                    style={"minWidth": "100px", "height": "36px"}
                                ),
                            ]
                        ),
                        width="auto",
                        className="ps-1"  # Add left padding
                    ),
                ], 
                justify="center",
                className="g-2"  # Reduced gap between items
                ),
                className="mb-4"
            )
        ),
        
        # Second row with the other dropdowns
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    # Offense Team Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Offense Team:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='offense-team-dropdown',
                                    placeholder="Select Offense Team",
                                    style={"minWidth": "200px", "height": "36px"},
                                    multi=False
                                ),
                            ],
                            className="me-2"  # Add right margin to separate from next group
                        ),
                        width="auto",
                        className="pe-1"  # Add right padding
                    ),
                    
                    # Week Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Week:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='week-dropdown',
                                    placeholder="Select Week",
                                    style={"minWidth": "100px", "height": "36px"},
                                    multi=False
                                ),
                            ],
                            className="me-2"  # Add right margin to separate from next group
                        ),
                        width="auto",
                        className="px-1"  # Add horizontal padding
                    ),
                    
                    # Recommendation Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Recommendation:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='recommendation-dropdown',
                                    placeholder="Select Recommendation",
                                    style={"minWidth": "150px", "height": "36px"},
                                    multi=False,
                                    optionHeight=100,
                                ),
                            ],
                            className="me-2"  # Add right margin to separate from next group
                        ),
                        width="auto",
                        className="px-1"  # Add horizontal padding
                    ),
                    
                    # Decision Dropdown
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Decision:", style={"height": "36px"}),
                                dcc.Dropdown(
                                    id='decision-dropdown',
                                    placeholder="Select Decision",
                                    style={"minWidth": "150px", "height": "36px"},
                                    multi=False
                                ),
                            ]
                        ),
                        width="auto",
                        className="ps-1"  # Add left padding
                    ),
                ], 
                justify="center",
                className="g-2"  # Reduced gap between items
                ),
                className="mb-4"
            )
        )
    ], fluid=True),
    
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
                        {"name": ["Play Outcome", "Recommendation"], "id": "Recommendation"},
                        {"name": ["Play Outcome", "Decision"], "id": "Decision"},
                        {"name": ["Play Outcome", "Play Desc"], "id": "Desc"},
                    ],
                    page_size=10,
                    page_action='native',
                    sort_action='native',
                    filter_action='none',  # Disable the built-in filtering
                    merge_duplicate_headers=True,
                    style_table={
                        'overflowX': 'auto',
                        'height': '100%',
                        'minHeight': '400px',
                        'fontFamily': 'Arial, sans-serif',
                        'width': '100%'
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
                            'borderBottom': '1px solid #dee2e6'
                        }
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
                    # Removed tooltip_data and tooltip_duration to disable hover interactivity
                    markdown_options={"html": True}
                )
            ], fluid=True, className="p-0"),
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
    recommendations = [{'label': rec, 'value': rec} for rec in sorted(dff['Recommendation'].unique())]
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
        dff = dff[dff['Recommendation'] == selected_recommendation]
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