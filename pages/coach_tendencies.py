import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from config.config import CONFIG

dash.register_page(__name__, path="/coach-tendencies", name="Coach Tendencies")

df = pd.read_parquet("data/coach_tendencies.parquet")

# Get unique coaches for dropdowns
all_coaches = sorted(df['coach_name'].unique())
default_coaches = ['Lincoln Riley', 'Ryan Day', 'Nick Saban', 'Kirby Smart', 'Dabo Swinney', 'Deion Sanders', 'Jim Harbaugh', 'Lane Kiffin', 'Mike Leach']
MAX_SELECTED_COACHES = 10

layout = dbc.Container([
    html.Div([
        html.H5(html.B("Coach Tendencies"), className="mt-4", style={'color': '#000'}),
        html.P("Explore how different coaches behave on 4th down. Plays in final 30 seconds of the game are excluded."),
    ], style={"overflow": "hidden"}), 
    
    dbc.Row([
        # Coach Multi-Select Dropdown
        dbc.Col([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(
                        "Coaches:",  
                        style={
                            "height": "100%", 
                            "width": "90px",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                            "padding": "0.375rem 0.75rem"  # Match Bootstrap's default padding
                        }
                    ),
                    dcc.Dropdown(
                        id='coach-dropdown',
                        options=[{'label': coach, 'value': coach} for coach in all_coaches],
                        placeholder="Select Coaches...",
                        value=default_coaches,
                        multi=True,
                        style={
                            "minWidth": "180px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "border-left": "none",
                            "fontSize": "13px",
                        }
                    ),
                ], 
                style={"alignItems": "flex-start"}, 
                className="flex-nowrap g-0"  # g-0 removes gutters between elements
                )
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=8, className="mb-1"),

        # From Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("From:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='start-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                sorted(df['season'].unique())],
                        value=2013,
                        placeholder="Start",
                        style={
                            "minWidth": "100px", 
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px",
                        }
                    ),
                ],
                className="justify-content-end",
                style={"flexWrap": "nowrap"}
            ),
        ],xs=6, sm=6, md=6, lg=6, xl=2),

        # To Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("To:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='end-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                 sorted(df['season'].unique())],
                        value=2024,
                        placeholder="End",
                        style={
                            "minWidth": "100px",
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px",
                        }
                    ),
                ],
                className="justify-content-start",
                style={"flexWrap": "nowrap"}
            )
        ], xs=6, sm=6, md=6, lg=6, xl=2),
    ], className="mb-4 g-3 align-items-top"),

    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="coach-tendency-graph", 
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "min-height": "400px"}
                ),
                className="bg-white",
                style={
                    "padding-left": "20px",
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%",
                    "min-height": "400px"
                }
            )
        ], xs=12, xl=6, className="mb-4 px-1 pb-1 pt-1"),
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="coach-wp-lost-graph", 
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "min-height": "400px"}
                ),
                className="bg-white",
                style={
                    "padding-left": "20px",
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%",
                    "min-height": "400px"
                }
            )
        ], xs=12, xl=6, className="mb-4 px-1 pb-1 pt-1")
    ]),
    
    # Coach selection dropdown row for trend plot
    html.Div([
        html.H5(html.B("Coach Tendencies Over Time"), className="mt-4", style={'color': '#000'}),
        html.P("Explore the rate at which coaches go for it on 4th down when recommended over the years."),
    ], style={"overflow": "hidden"}),
    
    dbc.Row([
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText(
                        "Coach:", 
                        style={
                            "height": "100%",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                            "height": "36px",
                        }
                    ),
                    dcc.Dropdown(
                        id='trend-coach-dropdown',
                        options=[{'label': coach, 'value': coach} for coach in all_coaches],
                        placeholder="Select Coach...",
                        value='Lincoln Riley',
                        style={
                            "minWidth": "200px", 
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px",
                            "white-space": "nowrap",
                        }
                    ),
                ],
                className="justify-content-center",
                style={"flexWrap": "nowrap"}
            )
        ], xs=12, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="coach-trend-graph",
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "min-height": "400px"}
                ),
                className="bg-white",
                style={
                    "padding-left": "20px",
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%",
                    "min-height": "400px"
                }
            )
        ], xs=12, className="mb-4 px-1 pb-1 pt-1")
    ]),
], 
fluid=True,
style={
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
},
className="responsive-container"
)

@dash.callback(
    Output("coach-tendency-graph", "figure"),
    Output("coach-wp-lost-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("coach-dropdown", "value"),
    Input('screen-width-store', 'data')
)
def update_graphs(start_season, end_season, selected_coaches, screen_width):
    if not selected_coaches:
        return go.Figure(), go.Figure()
    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]
    
    # Filter by selected coaches
    dff = dff[dff["coach_name"].isin(selected_coaches)].sort_values("season")

    if screen_width < 768:  
        axis_fontsize = 11
        axis_subtext_fontsize = 8
    else:
        axis_fontsize = 13
        axis_subtext_fontsize = 9

    # Aggregate data for bar charts
    grouped = (
        dff.groupby(["coach_name"], as_index=False)
        .agg({"n_go": "sum", "n_go_rec": "sum", "net_wp_lost": "sum", "fill_color": "last", "border_color": "last"})
    )
    grouped = (
        grouped.merge(
            dff.groupby(['coach_name'])
            .agg(n_season=('season', 'count'))
            .reset_index(),
            on='coach_name',
            how='left'
        )
    )
    grouped = grouped[grouped["n_go_rec"] > 0]
    grouped["go_for_it_rate"] = grouped["n_go"] / grouped["n_go_rec"]
    grouped["avg_wp_lost_per_season"] = grouped["net_wp_lost"] / grouped["n_season"]

    ### PLOT 1: Go-For-It Rate - Sort from highest to lowest
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=grouped_sorted1["go_for_it_rate"],
        y=grouped_sorted1["coach_name"],
        orientation="h",
        marker_color=grouped_sorted1["fill_color"],
        marker_line_color=grouped_sorted1["border_color"],
        marker_line_width=3,
        text=[f"{x:.1%}" for x in grouped_sorted1["go_for_it_rate"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="%{customdata[0]} play(s)",
        name="",
        showlegend=False,
        customdata=grouped_sorted1[["n_go_rec"]].values
    ))

    max_x1 = grouped_sorted1["go_for_it_rate"].max()
    
    # Calculate dynamic height based on number of coaches
    BAR_HEIGHT = 20
    BAR_GAP = 10  
    bottom_margin = 80
    min_height = 400
    x_range_multiplier = 1.15
    
    num_coaches = len(grouped_sorted1)
    calculated_height = num_coaches * (BAR_HEIGHT + BAR_GAP) + 150
    PLOT_HEIGHT = max(calculated_height, min_height)
    
    fig1.update_layout(
        title=dict(
            text=(
                "<span style='font-size:16px'><b>Go-For-It Rate When Recommended</b></span><br>"
                "<span style='font-size:16px'><sub>'Recommended' when going for it is +1.5% WP over kicking</sub></span>"
            ),
            xanchor='left',
            x=0,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Percent of time coach went for it when recommended</span>",
        yaxis=dict(
            fixedrange=True,
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted1["coach_name"].tolist(),
            showticklabels=True,
        ),
        xaxis=dict(
            fixedrange=True,
            tickformat=".0%",
            range=[0, max_x1 * x_range_multiplier]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=PLOT_HEIGHT, 
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
        autosize=True,
        dragmode=False,
    )

    ### PLOT 2: WP Lost - Sort from highest to lowest (most WP lost to least)
    grouped_sorted2 = grouped.sort_values("avg_wp_lost_per_season", ascending=True)
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=grouped_sorted2["avg_wp_lost_per_season"],
        y=grouped_sorted2["coach_name"],
        orientation="h",
        marker_color=grouped_sorted2["fill_color"],
        marker_line_color=grouped_sorted2["border_color"],
        marker_line_width=3,
        text=[f"{wp * 100:.1f}%" for wp in grouped_sorted2["avg_wp_lost_per_season"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="%{customdata[0]} season(s)",
        name="",
        showlegend=False,
        customdata=grouped_sorted2[["n_season"]].values
    ))

    max_x2 = grouped_sorted2["avg_wp_lost_per_season"].max()
    
    fig2.update_layout(
        title=dict(
            text=(
                "<span style='font-size:16px'><b>Win Probability Lost Per Season</b></span><br>"
                "<span style='font-size:16px'><sub>Due to not going for it on 4th down when recommended</sub></span>"
            ),
            xanchor='left',
            x=0
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Avg WP Lost per Season (percentage points)</span>",
        yaxis=dict(
            fixedrange=True,
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted2["coach_name"].tolist(),
            showticklabels=True,
        ),
        xaxis=dict(
            fixedrange=True,
            tickformat=".0%",
            range=[0, max_x2 * x_range_multiplier]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=PLOT_HEIGHT, 
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
        dragmode=False,
    )

    return fig1, fig2

@dash.callback(
    Output("coach-trend-graph", "figure"),
    Input("trend-coach-dropdown", "value"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input('screen-width-store', 'data')
)
def update_trend_graph(selected_coach, start_season, end_season, screen_width):
    if selected_coach is None:
        return go.Figure()
    
    # Get coach data
    coach_df = df[df['coach_name'] == selected_coach]
    
    coach_data = coach_df.groupby('season').agg(
        n_go=('n_go', 'sum'),
        n_go_rec=('n_go_rec', 'sum'),
        fill_color=('fill_color', 'first'),
        border_color=('border_color', 'first')
    ).reset_index()
    
    coach_data['go_rate'] = coach_data['n_go'] / coach_data['n_go_rec']
    
    if screen_width < 768:  
        axis_fontsize = 11
        title_fontsize = 14
    else:
        axis_fontsize = 13
        title_fontsize = 16
    
    # Get coach colors
    fill_color = coach_data['fill_color'].iloc[0]
    border_color = coach_data['border_color'].iloc[0]
    
    fig = go.Figure()
    
    # Add line trace
    fig.add_trace(go.Scatter(
        x=coach_data['season'],
        y=coach_data['go_rate'],
        mode='lines+markers',
        line=dict(color=fill_color, width=3),
        marker=dict(color=border_color, size=10, line=dict(width=2, color='black')),
        hoverinfo='text',
        hovertemplate='<b>Season %{x}</b><br>Go Rate: %{y:.1%}<br>Plays: %{customdata}<extra></extra>',
        name='',
        customdata=coach_data['n_go_rec']
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<span style='font-size:{title_fontsize}px'><b>{selected_coach} Go-For-It Rate Over Time</b></span>",
            x=0.5,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Season</span>",
        yaxis_title=f"<span style='font-size:{axis_fontsize}px'>Go-For-It Rate When Recommended</span>",
        yaxis=dict(
            tickformat=".0%",
            range=[0, min(1.1, max(coach_data['go_rate']) * 1.1)]
        ),
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        margin=dict(l=20, r=60, t=80, b=60),
        height=400,
        template="plotly_white",
        showlegend=False,
        hovermode="x unified",
        dragmode=False,
    )
    
    return fig