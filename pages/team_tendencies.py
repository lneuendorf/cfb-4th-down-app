import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config.config import CONFIG

dash.register_page(__name__, path="/team-tendencies", name="Team Tendencies")

df = pd.read_parquet("data/team_tendencies.parquet")

SAMPLE_SIZE_ON = False

layout = dbc.Container([
    html.Div([
        html.H5(html.B("Team Tendencies"), className="mt-4", style={'color': '#000'}),
        html.P("Explore how different teams behave on 4th down."),
    ], style={"overflow": "hidden"}), 
    
    dbc.Row([
        # Conference Dropdown
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Conference:", style={"height": "36px"}),
                    dcc.Dropdown(
                        id='conference-dropdown',
                        options=[{'label': conf, 'value': conf} for conf in 
                                 ['All'] + sorted(df['offense_conference'].dropna().unique())],
                        placeholder="Select Conference",
                        value='Big Ten',
                        style={"minWidth": "200px", "height": "36px"}
                    ),
                ],
                className="justify-content-xl-end justify-content-center"
            )
        ], xs=12, sm=12, md=12, lg=12, xl=4),

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
        ], xs=12, sm=12, md=12, lg=12, xl=4),
    ], className="mb-4 g-3 align-items-center"),

    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(
                    id="team-tendency-graph", 
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%"}
                ),
                className="bg-white p-3",
                style={
                    "border-radius": "16px", 
                    "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                    "height": "100%"
                }
            )
        ], xs=12, xl=6, className="mb-4"),
        dbc.Col([
            dbc.Container(
                dcc.Graph(id="wp-lost-graph", config={"displayModeBar": False}),
                className="bg-white p-3",
                style={"border-radius": "16px", 
                       "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                       "height": "100%"
                }
            )
        ], xs=12, xl=6, className="mb-4")
    ])
], 
fluid=True,
style={
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
},
className="responsive-container"
)

@dash.callback(
    Output("team-tendency-graph", "figure", allow_duplicate=True),
    Output("wp-lost-graph", "figure", allow_duplicate=True),
    Input("toggle-sample-size", "value"),
    State("team-tendency-graph", "figure"),
    State("wp-lost-graph", "figure"),
    prevent_initial_call=True
)
def toggle_sample_size(show_sample, fig1, fig2):
    # Update first figure
    fig1['data'][1]['visible'] = show_sample
    fig1['layout']['annotations'][0]['visible'] = show_sample
    
    # Update second figure
    fig2['data'][1]['visible'] = show_sample
    fig2['layout']['annotations'][0]['visible'] = show_sample

    # show the vertical grid lines
    fig1['layout']['xaxis']['showgrid'] = True
    fig2['layout']['xaxis']['showgrid'] = True

    global SAMPLE_SIZE_ON
    SAMPLE_SIZE_ON = show_sample
    
    return fig1, fig2

# Keep your original update_graphs callback (unchanged)
@dash.callback(
    Output("team-tendency-graph", "figure"),
    Output("wp-lost-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("conference-dropdown", "value")
)
def update_graphs(start_season, end_season, selected_conference):
    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]
    if selected_conference != "All":
        dff = dff[dff["offense_conference"] == selected_conference]

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
        hovertemplate="<b>%{y}</b>",
        name="",
        showlegend=False
    ))
    
    # Add invisible trace for the n= values on the left
    fig1.add_trace(go.Bar(
        x=[0.0001] * len(grouped_sorted1),
        y=grouped_sorted1["offense_team"],
        orientation="h",
        text=[f"n={n}" for n in grouped_sorted1["n_go_rec"]],
        textposition="outside",
        insidetextanchor="start",
        textfont=dict(color="white", size=8),
        hoverinfo="skip",
        marker=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
        cliponaxis=False
    ))

    # Calculate dynamic right margin based on max value
    max_x1 = grouped_sorted1["go_for_it_rate"].max()
    
    # Calculate bottom margin based on number of teams
    bottom_margin = 80
    BAR_HEIGHT = 20
    BAR_GAP = 10  
    x_range_multiplier = 1.15

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

    plot_height = len(grouped_sorted1) * (BAR_HEIGHT + BAR_GAP) + 150  # 150 for margins/title
    
    fig1.update_layout(
        title=dict(
            text=("Go-For-It Rate When Recommended<br>"
                  "<sub>Plays in final 30 seconds excluded. 'Optimal' defined as +1.5% WP over kicking</sub>"),
            xanchor='left',
            x=0
        ),
        xaxis_title="Percentage of times team went for it when recommended",
        yaxis=dict(
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted1["offense_team"].tolist(),
            showticklabels=False,
        ),
        xaxis=dict(
            tickformat=".0%",
            range=[0, max_x1 * x_range_multiplier]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=plot_height, 
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
    )
    
    # Add annotation for sample size
    fig1.add_annotation(
        x=0.5, y=1/len(grouped_sorted1) * -1.7,
        xref="paper", yref="paper",
        text="(n = number of plays where going for it was recommended)",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top"
    )

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
        hovertemplate="<b>%{y}</b>",
        name="",
        showlegend=False
    ))
    
    # Add invisible trace for the n= values on the left
    fig2.add_trace(go.Bar(
        x=[0.0001] * len(grouped_sorted2),
        y=grouped_sorted2["offense_team"],
        orientation="h",
        text=[f"n={n}" for n in grouped_sorted2["n_season"]],
        textposition="outside",
        insidetextanchor="start",
        textfont=dict(color="white", size=8),
        hoverinfo="skip",
        marker=dict(color="rgba(0,0,0,0)"),
        showlegend=False,
        cliponaxis=False
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

    plot_height2 = len(grouped_sorted2) * (BAR_HEIGHT + BAR_GAP) + 150
    
    fig2.update_layout(
        title=dict(
            text=("Average Win Probability Lost Per Season<br>"
                  "<sub>Due to not going for it when recommended</sub>"),
            xanchor='left',
            x=0
        ),
        xaxis_title="Avg WP Lost per Season (percentage points)",
        yaxis=dict(
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted2["offense_team"].tolist(),
            showticklabels=False,
        ),
        xaxis=dict(
            tickformat=".0%",
            range=[0, max_x2 * x_range_multiplier]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=plot_height2, 
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
    )

    fig2.add_annotation(
        x=0.5, y=1/len(grouped_sorted2) * -1.7,
        xref="paper", yref="paper",
        text="(n = number of seasons across selected years)",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top"
    )

    fig1, fig2 = toggle_sample_size(SAMPLE_SIZE_ON, fig1, fig2)
    
    return fig1, fig2