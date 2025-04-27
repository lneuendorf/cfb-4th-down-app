import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config.config import CONFIG

dash.register_page(__name__, path="/coach-tendencies", name="Coach Tendencies")

df = pd.read_parquet("data/coach_tendencies.parquet")

# Get unique coaches for dropdown
all_coaches = sorted(df['coach_name'].unique())
# Preselected coaches
preselected_coaches = [
    'Nick Saban', 'Luke Fickell', 'Ryan Day', 'Lincoln Riley', 
    'Urban Meyer', 'Dan Lanning', 'Dabo Swinney', 'Brian Kelly', 'Kirby Smart'
]

SAMPLE_SIZE_ON = False
PLOT_HEIGHT = 400
MAX_SELECTED_COACHES = 10

layout = dbc.Container([
    html.Div([
        html.H5(html.B("Coach Tendencies"), className="mt-4", style={'color': '#000'}),
        html.P("Explore how different coaches behave on 4th down."),
    ], style={"overflow": "hidden"}), 
    
    dbc.Row([
        # Coach Selection Dropdown
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Coaches:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='coach-dropdown',
                        options=[{'label': coach, 'value': coach} for coach in all_coaches],
                        placeholder="Select Coaches...",
                        value=preselected_coaches,
                        multi=True,
                        style={"minWidth": "200px", "height": "36px"},
                        searchable=True
                    ),
                ],
                className="justify-content-xl-end justify-content-center"
            )
        ], xs=12, sm=12, md=12, lg=12, xl=6),

        # From Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("From:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='start-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                 sorted(df['season'].unique())],
                        value=df['season'].min(),
                        placeholder="Start",
                        style={"minWidth": "100px", "height": "36px"}
                    ),
                ],
                className="justify-content-end"
            )
        ], xs=6, sm=6, md=6, lg=6, xl=2),

        # To Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("To:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='end-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                 sorted(df['season'].unique())],
                        value=df['season'].max(),
                        placeholder="End",
                        style={"minWidth": "100px", "height": "36px"}
                    ),
                ],
                className="justify-content-start"
            )
        ], xs=6, sm=6, md=6, lg=6, xl=2),

        # Show Sample Size
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Label(
                        "Show Sample Size:", 
                        html_for="toggle-sample-size", 
                        className="my-auto"),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Switch(
                        id="toggle-sample-size",
                        label=None,
                        value=False,
                        className="my-auto"
                    ),
                    width="auto"
                )
            ], className="g-2 align-items-center justify-content-xl-start justify-content-center")
        ], xs=12, sm=12, md=12, lg=12, xl=2),
    ], className="mb-4 g-3 align-items-center"),

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
        ], xs=12, xl=6, className="mb-4"),
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
        ], xs=12, xl=6, className="mb-4")
    ]),
    
    # New time series plot
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
        ], xs=12, className="mb-4")
    ]),

    html.Div([
        html.P(
            "Note: Plays in final 30 seconds of the game are excluded.",
            style={"font-size": "12px", "color": "#555"}
        )
    ], className="text-center mt-2")
], 
fluid=True,
style={
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
},
className="responsive-container"
)

@dash.callback(
    Output("coach-tendency-graph", "figure", allow_duplicate=True),
    Output("coach-wp-lost-graph", "figure", allow_duplicate=True),
    Output("coach-trend-graph", "figure", allow_duplicate=True),
    Input("toggle-sample-size", "value"),
    State("coach-tendency-graph", "figure"),
    State("coach-wp-lost-graph", "figure"),
    State("coach-trend-graph", "figure"),
    prevent_initial_call=True
)
def toggle_sample_size(show_sample, fig1, fig2, fig3):
    global PLOT_HEIGHT
    
    # For bar charts
    if 'data' in fig1 and len(fig1['data']) > 1:
        fig1['data'][1]['visible'] = show_sample
    if 'annotations' in fig1 and len(fig1['annotations']) > 0:
        fig1['layout']['annotations'][0]['visible'] = show_sample
        
    if 'data' in fig2 and len(fig2['data']) > 1:
        fig2['data'][1]['visible'] = show_sample
    if 'annotations' in fig2 and len(fig2['annotations']) > 0:
        fig2['layout']['annotations'][0]['visible'] = show_sample
    
    fig1['layout']['xaxis']['showgrid'] = True
    fig2['layout']['xaxis']['showgrid'] = True
    
    fig1['layout']['height'] = PLOT_HEIGHT
    fig2['layout']['height'] = PLOT_HEIGHT
    
    global SAMPLE_SIZE_ON
    SAMPLE_SIZE_ON = show_sample
    
    return fig1, fig2, fig3

@dash.callback(
    Output("coach-dropdown", "value"),
    Input("coach-dropdown", "value"),
    prevent_initial_call=True
)
def limit_coach_selections(selected_coaches):
    if len(selected_coaches) > MAX_SELECTED_COACHES:
        return selected_coaches[:MAX_SELECTED_COACHES]
    return selected_coaches

@dash.callback(
    Output("coach-tendency-graph", "figure"),
    Output("coach-wp-lost-graph", "figure"),
    Output("coach-trend-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("coach-dropdown", "value"),
    Input('screen-width-store', 'data'),
    Input("toggle-sample-size", "value")
)
def update_graphs(start_season, end_season, selected_coaches, screen_width, show_sample):
    if not selected_coaches:
        selected_coaches = preselected_coaches
    
    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]
    dff = dff[dff["coach_name"].isin(selected_coaches)]

    if screen_width < 768:  
        axis_fontsize = 11
        axis_subtext_fontsize = 8
    else:
        axis_fontsize = 13
        axis_subtext_fontsize = 9

    # Aggregate data for bar charts
    grouped = (
        dff.groupby(["coach_name", "offense_team", "fill_color", "border_color"], as_index=False)
        .agg({"n_go": "sum", "n_go_rec": "sum", "net_wp_lost": "sum"})
    )
    grouped = (
        grouped.merge(
            dff.groupby(['coach_name', 'offense_team'])
            .agg(n_season=('season', 'count'))
            .reset_index(),
            on=['coach_name', 'offense_team'],
            how='left'
        )
    )
    grouped = grouped[grouped["n_go_rec"] > 0]
    grouped["go_for_it_rate"] = grouped["n_go"] / grouped["n_go_rec"]
    grouped["avg_wp_lost_per_season"] = grouped["net_wp_lost"] / grouped["n_season"]
    grouped["coach_label"] = grouped["coach_name"]

    ### PLOT 1: Go-For-It Rate
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        x=grouped_sorted1["go_for_it_rate"],
        y=grouped_sorted1["coach_label"],
        orientation="h",
        marker_color=grouped_sorted1["fill_color"],
        marker_line_color=grouped_sorted1["border_color"],
        marker_line_width=3,
        text=[f"{x:.1%}" for x in grouped_sorted1["go_for_it_rate"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="<b>%{y}</b>",
        name="",
        showlegend=False
    ))
    
    fig1.add_trace(go.Bar(
        x=[0.0001] * len(grouped_sorted1),
        y=grouped_sorted1["coach_label"],
        orientation="h",
        text=[f"n={n}" for n in grouped_sorted1["n_go_rec"]],
        textposition="outside",
        insidetextanchor="start",
        textfont=dict(color="white", size=8),
        hoverinfo="skip",
        marker=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
        cliponaxis=False,
        visible=show_sample
    ))

    max_x1 = grouped_sorted1["go_for_it_rate"].max()
    
    bottom_margin = 80
    min_height = 400
    BAR_HEIGHT = 20
    BAR_GAP = 10  
    x_range_multiplier = 1.15
    calculated_height = len(grouped_sorted1) * (BAR_HEIGHT + BAR_GAP) + 150
    global PLOT_HEIGHT
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
            categoryarray=grouped_sorted1["coach_label"].tolist(),
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
    
    fig1.add_annotation(
        x=0.5, y=1/len(grouped_sorted1) * -1.7,
        xref="paper", yref="paper",
        text=f"<span style='font-size:{axis_subtext_fontsize}px'>(n = number of plays where going for it was recommended)</span>",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top",
        visible=show_sample
    )

    ### PLOT 2: WP Lost
    grouped_sorted2 = grouped.sort_values("avg_wp_lost_per_season", ascending=True)
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=grouped_sorted2["avg_wp_lost_per_season"],
        y=grouped_sorted2["coach_label"],
        orientation="h",
        marker_color=grouped_sorted2["fill_color"],
        marker_line_color=grouped_sorted2["border_color"],
        marker_line_width=3,
        text=[f"{wp * 100:.1f}%" for wp in grouped_sorted2["avg_wp_lost_per_season"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="<b>%{y}</b>",
        name="",
        showlegend=False
    ))
    
    fig2.add_trace(go.Bar(
        x=[0.0001] * len(grouped_sorted2),
        y=grouped_sorted2["coach_label"],
        orientation="h",
        text=[f"n={n}" for n in grouped_sorted2["n_season"]],
        textposition="outside",
        insidetextanchor="start",
        textfont=dict(color="white", size=8),
        hoverinfo="skip",
        marker=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
        cliponaxis=False,
        visible=show_sample
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
            categoryarray=grouped_sorted2["coach_label"].tolist(),
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

    fig2.add_annotation(
        x=0.5, y=1/len(grouped_sorted2) * -1.7,
        xref="paper", yref="paper",
        text=f"<span style='font-size:{axis_subtext_fontsize}px'>(n = number of seasons across selected years)</span>",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top",
        visible=show_sample
    )

    ### PLOT 3: Trend Over Time
    # Prepare data for trend plot
    trend_data = dff.groupby(['coach_name', 'season', 'fill_color', 'border_color'], as_index=False).agg({
        'n_go': 'sum',
        'n_go_rec': 'sum'
    })
    trend_data = trend_data[trend_data['n_go_rec'] > 0]
    trend_data['go_for_it_rate'] = trend_data['n_go'] / trend_data['n_go_rec']
    
    fig3 = go.Figure()
    
    # Add a line for each coach
    for coach in selected_coaches:
        coach_data = trend_data[trend_data['coach_name'] == coach]
        if not coach_data.empty:
            color = coach_data.iloc[0]['fill_color']
            fig3.add_trace(go.Scatter(
                x=coach_data['season'],
                y=coach_data['go_for_it_rate'],
                mode='lines+markers',
                name=coach,
                line=dict(color=color, width=3),
                marker=dict(size=8),
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "Season: %{x}<br>" +
                             "Go Rate: %{y:.1%}<br>" +
                             "Plays: %{text}",
                text=[f"{n}" for n in coach_data['n_go_rec']]
            ))
    
    fig3.update_layout(
        title=dict(
            text="<span style='font-size:16px'><b>Go-For-It Rate Trend Over Time</b></span>",
            xanchor='left',
            x=0
        ),
        xaxis_title="Season",
        yaxis_title="Go-For-It Rate When Recommended",
        yaxis=dict(
            tickformat=".0%",
            range=[0, 1.1]
        ),
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        margin=dict(l=20, r=20, t=60, b=60),
        height=500,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig1, fig2, fig3