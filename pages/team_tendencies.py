import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config.config import CONFIG

dash.register_page(__name__, path="/team-tendencies", name="Team Tendencies")

df = pd.read_parquet("data/team_tendencies.parquet")

PLOT_HEIGHT = 400

layout = dbc.Container([
    html.Div([
        html.H5(html.B("Team Tendencies"), className="mt-4", style={'color': '#000'}),
        html.P("Explore how different teams behave on 4th down. Plays in final 30 seconds of the game are excluded."),
    ], style={"overflow": "hidden"}), 
    
    dbc.Row([
        # Conference Dropdown
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText(
                        "Conference:",
                        style={
                            "height": "36px",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                        }
                    ),
                    dcc.Dropdown(
                        id='conference-dropdown',
                        options=[{'label': conf, 'value': conf} for conf in 
                                 ['All'] + sorted(df['offense_conference'].dropna().unique())],
                        placeholder="Select Conference",
                        value='Big Ten',
                        style={
                            "minWidth": "200px",
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px"
                        }
                    ),
                ],
                # add right padding
                className="justify-content-xl-end justify-content-center px-xl-3"
            )
        ], xs=12, sm=12, md=12, lg=12, xl=6),

        # From Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText(
                        "From:",
                        style={
                            "height": "36px",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                        }
                    ),
                    dcc.Dropdown(
                        id='start-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                 sorted(df['season'].unique())],
                        value=df['season'].min(),
                        placeholder="Start",
                        style={
                            "minWidth": "100px",
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px"
                        }
                    ),
                ],
                className="justify-content-end"
            )
        ], xs=6, sm=6, md=6, lg=6, xl=2),

        # To Season
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText(
                        "To:", 
                        style={
                            "height": "36px",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                        }
                    ),
                    dcc.Dropdown(
                        id='end-season',
                        options=[{'label': str(s), 'value': s} for s in 
                                 sorted(df['season'].unique())],
                        value=df['season'].max(),
                        placeholder="End",
                        style={
                            "minWidth": "100px",
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px"
                        }
                    ),
                ],
                className="justify-content-start"
            )
        ], xs=6, sm=6, md=6, lg=6, xl=2),
    ], className="mb-4 g-3 align-items-center"),

    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="team-tendency-graph", 
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "min-height": "400px"}  # Add min-height
                ),
                className="bg-white",
                style={
                    "padding-left": "20px",
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%",
                    "min-height": "400px"  # Add min-height to container
                }
            )
        ], xs=12, xl=6, className="mb-4 px-1 pb-1 pt-1"),
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="wp-lost-graph", 
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "min-height": "400px"}  # Add min-height
                ),
                className="bg-white",
                style={
                    "padding-left": "20px",
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%",
                    "min-height": "400px"  # Add min-height to container
                }
            )
        ], xs=12, xl=6, className="mb-4 px-1 pb-1 pt-1")
    ]),
    # Team selection dropdown row (add this new row)
    html.Div([
        html.H5(html.B("Team Tendencies Over Time"), className="mt-4", style={'color': '#000'}),
        html.P("Explore the rate at which teams go for it on 4th down when recommended over the years."),
    ], style={"overflow": "hidden"}),
    
    dbc.Row([
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText(
                        "Team:", 
                        style={
                            "height": "36px",
                            "border-top-right-radius": "0",
                            "border-bottom-right-radius": "0",
                        }
                    ),
                    dcc.Dropdown(
                        id='team-dropdown',
                        options=[{'label': team, 'value': team} for team in 
                                 sorted(df['offense_team'].unique())],
                        placeholder="Select Team",
                        value='LSU',
                        style={
                            "minWidth": "200px",
                            "height": "36px",
                            "border-top-left-radius": "0",
                            "border-bottom-left-radius": "0",
                            "fontSize": "13px"
                        }
                    ),
                ],
                className="justify-content-center"
            )
        ], xs=12, className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="team-trend-graph", 
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

# Keep your original update_graphs callback (unchanged)
@dash.callback(
    Output("team-tendency-graph", "figure"),
    Output("wp-lost-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("conference-dropdown", "value"),
    Input('screen-width-store', 'data')
)
def update_graphs(start_season, end_season, selected_conference, screen_width):
    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]
    if selected_conference != "All":
        dff = dff[dff["offense_conference"] == selected_conference]

    if screen_width < 768:  
        axis_fontsize = 11
        axis_subtext_fontsize = 8
    else:
        axis_fontsize = 13
        axis_subtext_fontsize = 9

    grouped = (
        dff.groupby(["offense_team", "fill_color", "border_color", "offense_logos"], as_index=False)
        .agg({"n_go": "sum", "n_go_rec": "sum", "net_wp_lost": "sum"})
    )
    grouped = (
        grouped.merge(
            (dff.groupby(['offense_team'])
            .agg(n_season=('season', 'count'))
            .reset_index()),
            on='offense_team',
            how='left'
        )
    )
    grouped = grouped[grouped["n_go_rec"] > 0]
    grouped["go_for_it_rate"] = grouped["n_go"] / grouped["n_go_rec"]
    grouped["avg_wp_lost_per_season"] = grouped["net_wp_lost"] / grouped["n_season"]

    ### PLOT 1
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)
    fig1 = go.Figure()
    
    # Add main bar trace with the metric on the right
    fig1.add_trace(go.Bar(
        x=grouped_sorted1["go_for_it_rate"],
        y=grouped_sorted1["offense_team"],
        orientation="h",
        marker_color=grouped_sorted1["fill_color"],
        marker_line_color=grouped_sorted1["border_color"],
        marker_line_width=3,
        text=[f"{x:.1%}" for x in grouped_sorted1["go_for_it_rate"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> (%{customdata[0]} play(s))",
        name="",
        showlegend=False,
        customdata=grouped_sorted1[["n_go_rec"]].values
    ))

    # Calculate dynamic right margin based on max value
    max_x1 = grouped_sorted1["go_for_it_rate"].max()
    
    # Calculate bottom margin based on number of teams
    bottom_margin = 80
    min_height = 400
    BAR_HEIGHT = 20
    BAR_GAP = 10  
    x_range_multiplier = 1.15
    calculated_height = len(grouped_sorted1) * (BAR_HEIGHT + BAR_GAP) + 150
    global PLOT_HEIGHT
    PLOT_HEIGHT = max(calculated_height, min_height)

    for _, row in grouped_sorted1.iterrows():
        fig1.add_layout_image(dict(
            source=row["offense_logos"],
            x=row["go_for_it_rate"] + (max_x1 * 0.02),
            y=row["offense_team"],
            xref="x",
            yref="y",
            sizex=1,
            sizey=0.8,
            xanchor="left",
            yanchor="middle",
            layer="above"
        ))
    
    fig1.update_layout(
        title=dict(
            text=(
                "<span style='font-size:16px'><b>Go-For-It Rate When Recommended</b></span><br>"
                "<span style='font-size:16px'><sub>'Recommended' when going for it is +1.5% WP over kicking</sub></span>"
            ),
            xanchor='left',
            x=0,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Percent of time team went for it when recommended</span>",
        yaxis=dict(
            fixedrange=True,  # Prevents zoom/pan on x-axis
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted1["offense_team"].tolist(),
            showticklabels=False,
        ),
        xaxis=dict(
            fixedrange=True,  # Prevents zoom/pan on x-axis
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
    
    # Add annotation for sample size
    # fig1.add_annotation(
    #     x=0.5, y=1/len(grouped_sorted1) * -2,
    #     xref="paper", yref="paper",
    #     text=f"<span style='font-size:{axis_subtext_fontsize}px'>(n = number of plays where going for it was recommended)</span>",
    #     showarrow=False,
    #     font=dict(size=9),
    #     xanchor="center",
    #     yanchor="middle",
    # )

    ### PLOT 2
    grouped_sorted2 = grouped.sort_values("avg_wp_lost_per_season", ascending=True)
    fig2 = go.Figure()
    
    # Add main bar trace with the metric on the right
    fig2.add_trace(go.Bar(
        x=grouped_sorted2["avg_wp_lost_per_season"],
        y=grouped_sorted2["offense_team"],
        orientation="h",
        marker_color=grouped_sorted2["fill_color"],
        marker_line_color=grouped_sorted2["border_color"],
        marker_line_width=3,
        text=[f"{wp * 100:.1f}%" for wp in grouped_sorted2["avg_wp_lost_per_season"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> (%{customdata[0]} season(s))",
        name="",
        showlegend=False,
        customdata=grouped_sorted2[["n_season"]].values
    ))

    max_x2 = grouped_sorted2["avg_wp_lost_per_season"].max()

    for _, row in grouped_sorted2.iterrows():
        fig2.add_layout_image(dict(
            source=row["offense_logos"],
            x=row["avg_wp_lost_per_season"] + (max_x2 * 0.02),
            y=row["offense_team"],
            xref="x",
            yref="y",
            sizex=1,
            sizey=0.8, 
            xanchor="left",
            yanchor="middle",
            layer="above"
        ))

    
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
            fixedrange=True,  # Prevents zoom/pan on x-axis
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted2["offense_team"].tolist(),
            showticklabels=False,
        ),
        xaxis=dict(
            fixedrange=True,  # Prevents zoom/pan on x-axis
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

    # fig2.add_annotation(
    #     x=0.5, y=1/len(grouped_sorted1) * -2,
    #     xref="paper", yref="paper",
    #     text=f"<span style='font-size:{axis_subtext_fontsize}px'>(n = number of seasons across selected years)</span>",
    #     showarrow=False,
    #     font=dict(size=9),
    #     xanchor="center",
    #     yanchor="middle",
    # )
    
    return fig1, fig2

@dash.callback(
    Output("team-trend-graph", "figure"),
    Input("team-dropdown", "value"),
    Input('screen-width-store', 'data')
)
def update_trend_graph(selected_team, screen_width):
    if selected_team is None:
        return go.Figure()
    
    # Get team data
    team_df = df[df['offense_team'] == selected_team]
    team_data = team_df.groupby('season').agg(
        n_go=('n_go', 'sum'),
        n_go_rec=('n_go_rec', 'sum'),
        fill_color=('fill_color', 'first'),
        border_color=('border_color', 'first'),
        offense_logos=('offense_logos', 'first')
    ).reset_index()
    
    team_data['go_rate'] = team_data['n_go'] / team_data['n_go_rec']
    
    if screen_width < 768:  
        axis_fontsize = 11
        title_fontsize = 14
        logo_size = 0.8
    else:
        axis_fontsize = 13
        title_fontsize = 16
        logo_size = 1
    
    # Get team colors and logo
    fill_color = team_data['fill_color'].iloc[0]
    border_color = team_data['border_color'].iloc[0]
    logo = team_data['offense_logos'].iloc[0]
    
    fig = go.Figure()
    
    # Add line trace
    fig.add_trace(go.Scatter(
        x=team_data['season'],
        y=team_data['go_rate'],
        mode='lines+markers',
        line=dict(color=fill_color, width=3),
        marker=dict(color=border_color, size=10, line=dict(width=2, color='black')),
        hoverinfo='text',
        hovertemplate='<b>Season %{x}</b><br>Go Rate: %{y:.1%}<extra></extra>',
        name=''
    ))
    
    # Add team logo
    fig.add_layout_image(dict(
        source=logo,
        x=1,
        y=1,
        xref="paper",
        yref="paper",
        xanchor="right",
        yanchor="top",
        sizex=logo_size,
        sizey=logo_size,
        layer="below",
        opacity=0.5,
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<span style='font-size:{title_fontsize}px'><b>{selected_team} Go-For-It Rate Over Time</b></span>",
            x=0.5,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Season</span>",
        yaxis_title=f"<span style='font-size:{axis_fontsize}px'>Go-For-It Rate When Recommended</span>",
        yaxis=dict(
            tickformat=".0%",
            range=[0, min(1.1, max(team_data['go_rate']) * 1.1)]
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