import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from config.config import CONFIG

dash.register_page(__name__, path="/coach-tendencies", name="Coach Tendencies")

df = pd.read_parquet("data/coach_tendencies.parquet")

# Get unique coaches for dropdowns
all_coaches = sorted(df["coach_name"].unique())
default_coaches = [
    "Lincoln Riley",
    "Marcus Freeman",
    "Ryan Day",
    "Nick Saban",
    "Kirby Smart",
    "Dabo Swinney",
    "Deion Sanders",
    "Jim Harbaugh",
    "Lane Kiffin",
    "Mike Leach",
]
MAX_SELECTED_COACHES = 10

layout = dbc.Container(
    [
        html.Div(
            [
                html.H5(
                    html.B("Coach Tendencies"), className="mt-4", style={"color": "#000"}
                ),
                html.P("Explore how different coaches behave on 4th down."),
            ],
            style={"overflow": "hidden"},
        ),
        dbc.Row(
            [
                # Coach Multi-Select Dropdown
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText(
                                            "Coaches:",
                                            style={
                                                "height": "100%",
                                                "width": "90px",
                                                "border-top-right-radius": "0",
                                                "border-bottom-right-radius": "0",
                                                "padding": "0.375rem 0.75rem",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="coach-dropdown",
                                            options=[
                                                {"label": coach, "value": coach}
                                                for coach in all_coaches
                                            ],
                                            placeholder="Select Coaches...",
                                            value=default_coaches,
                                            multi=True,
                                            style={
                                                "minWidth": "180px",
                                                "border-top-left-radius": "0",
                                                "border-bottom-left-radius": "0",
                                                "border-left": "none",
                                                "fontSize": "13px",
                                            },
                                        ),
                                    ],
                                    style={"alignItems": "flex-start"},
                                    className="flex-nowrap g-0",
                                )
                            ]
                        )
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                    xl=8,
                    className="mb-1",
                ),
                # From Season
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("From:", style={"height": "34px"}),
                                dcc.Dropdown(
                                    id="start-season",
                                    options=[
                                        {"label": str(s), "value": s}
                                        for s in sorted(df["season"].unique())
                                    ],
                                    value=df["season"].min(),
                                    placeholder="Start",
                                    style={
                                        "minWidth": "100px",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                ),
                            ],
                            className="justify-content-end",
                            style={"flexWrap": "nowrap"},
                        ),
                    ],
                    xs=6,
                    sm=6,
                    md=6,
                    lg=6,
                    xl=2,
                ),
                # To Season
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("To:", style={"height": "34px"}),
                                dcc.Dropdown(
                                    id="end-season",
                                    options=[
                                        {"label": str(s), "value": s}
                                        for s in sorted(df["season"].unique())
                                    ],
                                    value=df["season"].max(),
                                    placeholder="End",
                                    style={
                                        "minWidth": "100px",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                    },
                                ),
                            ],
                            className="justify-content-start",
                            style={"flexWrap": "nowrap"},
                        )
                    ],
                    xs=6,
                    sm=6,
                    md=6,
                    lg=6,
                    xl=2,
                ),
            ],
            className="mb-4 g-3 align-items-top",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.Img(
                                                src="/assets/logos/more_info.png",
                                                style={
                                                    "width": "15px",
                                                    "height": "15px",
                                                    "cursor": "pointer",
                                                },
                                                id="info-icon4",
                                                className="info-icon",
                                            ),
                                            style={
                                                "position": "absolute",
                                                "top": "10px",
                                                "right": "0px",
                                                "width": "24px",
                                                "height": "24px",
                                                "display": "flex",
                                                "alignItems": "center",
                                                "justifyContent": "center",
                                                "zIndex": "100",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="coach-tendency-graph",
                                            config={
                                                "displayModeBar": False,
                                                "responsive": True,
                                            },
                                            style={
                                                "height": "100%",
                                                "min-height": "400px",
                                            },
                                        ),
                                    ],
                                    style={"position": "relative"},
                                ),
                                dbc.Tooltip(
                                    "This chart shows the average go-for-it rate when recommended for the selected coach across the chosen date range, "
                                    "summarizing how often the coach followed model recommendations. Higher rates indicate a greater tendency to go for "
                                    "it when analytics suggest it is optimal.",
                                    target="info-icon4",
                                    placement="left",
                                    style={
                                        "maxWidth": "300px",
                                        "fontSize": "13px",
                                        "zIndex": "1000",
                                        "whiteSpace": "pre-line",
                                    },
                                ),
                            ],
                            className="bg-white",
                            style={
                                "padding-left": "20px",
                                "border-radius": "16px",
                                "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                                "height": "100%",
                                "min-height": "400px",
                            },
                        )
                    ],
                    xs=12,
                    xl=6,
                    className="mb-4 px-1 pb-1 pt-1",
                ),
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.Img(
                                                src="/assets/logos/more_info.png",
                                                style={
                                                    "width": "15px",
                                                    "height": "15px",
                                                    "cursor": "pointer",
                                                },
                                                id="info-icon5",
                                                className="info-icon",
                                            ),
                                            style={
                                                "position": "absolute",
                                                "top": "10px",
                                                "right": "0px",
                                                "width": "24px",
                                                "height": "24px",
                                                "display": "flex",
                                                "alignItems": "center",
                                                "justifyContent": "center",
                                                "zIndex": "100",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="coach-wp-lost-graph",
                                            config={
                                                "displayModeBar": False,
                                                "responsive": True,
                                            },
                                            style={
                                                "height": "100%",
                                                "min-height": "400px",
                                            },
                                        ),
                                    ],
                                    style={"position": "relative"},
                                ),
                                dbc.Tooltip(
                                    "This chart summarizes the average win probability lost per season for the selected coach over the chosen date range. "
                                    "Win probability is lost when a coach opts to punt or attempt a field goal despite going for it being recommended. "
                                    "Higher values indicate a greater expected cost from conservative fourth down decisions across the selected seasons.",
                                    target="info-icon5",
                                    placement="left",
                                    style={
                                        "maxWidth": "300px",
                                        "fontSize": "13px",
                                        "zIndex": "1000",
                                        "whiteSpace": "pre-line",
                                    },
                                ),
                            ],
                            className="bg-white",
                            style={
                                "padding-left": "20px",
                                "border-radius": "16px",
                                "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                                "height": "100%",
                                "min-height": "400px",
                            },
                        )
                    ],
                    xs=12,
                    xl=6,
                    className="mb-4 px-1 pb-1 pt-1",
                ),
            ]
        ),
        html.Div(
            [
                html.H5(
                    html.B("Coach Tendencies Over Time"),
                    className="mt-4",
                    style={"color": "#000"},
                ),
                html.P(
                    "Explore how coaches have performed over time on fourth down based on the selected metric."
                ),
            ],
            style={"overflow": "hidden"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    "Coach:",
                                    style={
                                        "height": "34px",
                                        "border-top-right-radius": "0",
                                        "border-bottom-right-radius": "0",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="trend-coach-dropdown",
                                    options=[
                                        {"label": coach, "value": coach}
                                        for coach in all_coaches
                                    ],
                                    placeholder="Select Coach...",
                                    value="Lane Kiffin",
                                    style={
                                        "minWidth": "200px",
                                        "height": "36px",
                                        "border-top-left-radius": "0",
                                        "border-bottom-left-radius": "0",
                                        "fontSize": "13px",
                                        "whiteSpace": "nowrap",
                                    },
                                ),
                            ],
                            className="justify-content-center",
                            style={"flexWrap": "nowrap"},
                        )
                    ],
                    xs=12,
                    md=6,
                    className="mb-4",
                ),
                dbc.Col(
                    [
                        dbc.RadioItems(
                            id="trend-metric-radio",
                            options=[
                                {
                                    "label": "Go-for-it rate when recommended",
                                    "value": "go_rate",
                                },
                                {
                                    "label": "Win probability lost",
                                    "value": "wp_lost",
                                },
                            ],
                            value="wp_lost",
                            inline=True,
                            className="d-flex justify-content-center justify-content-md-start gap-3 pt-2",
                            inputCheckedClassName="border border-dark bg-dark",
                        )
                    ],
                    xs=12,
                    md=6,
                    className="mb-4 d-flex align-items-center",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.Img(
                                                src="/assets/logos/more_info.png",
                                                style={
                                                    "width": "15px",
                                                    "height": "15px",
                                                    "cursor": "pointer",
                                                },
                                                id="info-icon6",
                                                className="info-icon",
                                            ),
                                            style={
                                                "position": "absolute",
                                                "top": "10px",
                                                "right": "0px",
                                                "width": "24px",
                                                "height": "24px",
                                                "display": "flex",
                                                "alignItems": "center",
                                                "justifyContent": "center",
                                                "zIndex": "100",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="coach-trend-graph",
                                            config={
                                                "displayModeBar": False,
                                                "responsive": True,
                                            },
                                            style={
                                                "height": "100%",
                                                "min-height": "400px",
                                            },
                                        ),
                                    ],
                                    style={"position": "relative"},
                                ),
                                dbc.Tooltip(
                                    "This chart shows either how often a coach follows go-for-it recommendations on fourth down or how much "
                                    "win probability they give up by not doing so across seasons. Trends can reveal shifts in a coach’s "
                                    "decision-making philosophy, adaptation to analytics, or changes in situational context as teams and roles evolve over time.",
                                    target="info-icon6",
                                    placement="left",
                                    style={
                                        "maxWidth": "300px",
                                        "fontSize": "13px",
                                        "zIndex": "1000",
                                        "whiteSpace": "pre-line",
                                    },
                                ),
                            ],
                            className="bg-white",
                            style={
                                "padding-left": "20px",
                                "border-radius": "16px",
                                "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)",
                                "height": "100%",
                                "min-height": "400px",
                            },
                        )
                    ],
                    xs=12,
                    className="mb-4 px-1 pb-1 pt-1",
                )
            ]
        ),
    ],
    fluid=True,
    style={
        "padding-left": CONFIG["padding-left"],
        "padding-right": CONFIG["padding-right"],
    },
    className="responsive-container",
)


@dash.callback(
    Output("coach-tendency-graph", "figure"),
    Output("coach-wp-lost-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("coach-dropdown", "value"),
    Input("screen-width-store", "data"),
)
def update_graphs(start_season, end_season, selected_coaches, screen_width):
    if not selected_coaches:
        return go.Figure(), go.Figure()

    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]

    # Filter by selected coaches
    dff = dff[dff["coach_name"].isin(selected_coaches)].sort_values("season")

    if screen_width < 768:
        axis_fontsize = 11
    else:
        axis_fontsize = 13

    # Aggregate data for bar charts
    grouped = dff.groupby(["coach_name"], as_index=False).agg(
        {
            "n_go": "sum",
            "n_go_rec": "sum",
            "net_wp_lost": "sum",
            "fill_color": "last",
            "border_color": "last",
        }
    )
    grouped = grouped.merge(
        dff.groupby(["coach_name"]).agg(n_season=("season", "count")).reset_index(),
        on="coach_name",
        how="left",
    )
    grouped = grouped[grouped["n_go_rec"] > 0].copy()
    grouped["go_for_it_rate"] = grouped["n_go"] / grouped["n_go_rec"]
    grouped["avg_wp_lost_per_season"] = grouped["net_wp_lost"] / grouped["n_season"]

    ### PLOT 1
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
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
            hovertemplate="<b>%{y}</b><br>%{customdata[0]} play(s)<extra></extra>",
            name="",
            showlegend=False,
            customdata=grouped_sorted1[["n_go_rec"]].values,
        )
    )

    max_x1 = grouped_sorted1["go_for_it_rate"].max() if not grouped_sorted1.empty else 1

    BAR_HEIGHT = 20
    BAR_GAP = 10
    bottom_margin = 80
    min_height = 400
    x_range_multiplier = 1.15

    num_coaches = len(grouped_sorted1)
    calculated_height = num_coaches * (BAR_HEIGHT + BAR_GAP) + 150
    plot_height = max(calculated_height, min_height)

    fig1.update_layout(
        title=dict(
            text=(
                "<span style='font-size:16px'><b>Go-For-It Rate When Recommended</b></span><br>"
                "<span style='font-size:16px'><sub>'Recommended' when going for it has highest expected win probability</sub></span>"
            ),
            xanchor="left",
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
            range=[0, max_x1 * x_range_multiplier if max_x1 > 0 else 1],
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=plot_height,
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
        autosize=True,
        dragmode=False,
    )

    ### PLOT 2
    grouped_sorted2 = grouped.sort_values("avg_wp_lost_per_season", ascending=True)
    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
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
            hovertemplate="<b>%{y}</b><br>%{customdata[0]} season(s)<extra></extra>",
            name="",
            showlegend=False,
            customdata=grouped_sorted2[["n_season"]].values,
        )
    )

    max_x2 = (
        grouped_sorted2["avg_wp_lost_per_season"].max()
        if not grouped_sorted2.empty
        else 1
    )

    fig2.update_layout(
        title=dict(
            text=(
                "<span style='font-size:16px'><b>Win Probability Lost Per Season</b></span><br>"
                "<span style='font-size:16px'><sub>Due to not going for it on 4th down when recommended</sub></span>"
            ),
            xanchor="left",
            x=0,
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
            range=[0, max_x2 * x_range_multiplier if max_x2 > 0 else 1],
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height=plot_height,
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
    Input("trend-metric-radio", "value"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("screen-width-store", "data"),
)
def update_trend_graph(
    selected_coach, selected_metric, start_season, end_season, screen_width
):
    if selected_coach is None:
        return go.Figure()

    coach_df = df[
        (df["coach_name"] == selected_coach)
        & (df["season"] >= start_season)
        & (df["season"] <= end_season)
    ]

    coach_data = (
        coach_df.groupby("season")
        .agg(
            n_go=("n_go", "sum"),
            n_go_rec=("n_go_rec", "sum"),
            net_wp_lost=("net_wp_lost", "sum"),
            fill_color=("fill_color", "first"),
            border_color=("border_color", "first"),
        )
        .reset_index()
        .sort_values(["season"], ascending=True)
    )

    coach_data = coach_data[coach_data["n_go_rec"] > 0].copy()
    coach_data["go_rate"] = coach_data["n_go"] / coach_data["n_go_rec"]
    coach_data["wp_lost"] = coach_data["net_wp_lost"]

    if coach_data.empty:
        return go.Figure()

    if screen_width < 768:
        axis_fontsize = 11
        title_fontsize = 14
    else:
        axis_fontsize = 13
        title_fontsize = 16

    fill_color = coach_data["fill_color"].iloc[-1]
    border_color = coach_data["border_color"].iloc[-1]

    if selected_metric == "go_rate":
        y_col = "go_rate"
        y_title = "Go-For-It Rate When Recommended"
        chart_title = f"{selected_coach} Go-For-It Rate When Recommended Over Time"
        hovertemplate = "<b>Season %{x}</b><br>Go Rate: %{y:.1%}<br>Plays: %{customdata}<extra></extra>"
        yaxis_config = dict(
            tickformat=".0%",
            range=[0, min(1.1, max(coach_data[y_col].max() * 1.1, 0.1))],
        )
        customdata = coach_data["n_go_rec"]
    else:
        y_col = "wp_lost"
        y_title = "Win Probability Lost"
        chart_title = f"{selected_coach} Win Probability Lost Over Time"
        hovertemplate = "<b>Season %{x}</b><br>WP Lost: %{y:.1%}<extra></extra>"
        y_max = coach_data[y_col].max()
        yaxis_config = dict(
            tickformat=".0%",
            range=[0, max(y_max * 1.15, 0.01)],
        )
        customdata = None

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=coach_data["season"],
            y=coach_data[y_col],
            mode="lines+markers",
            line=dict(color=fill_color, width=3),
            marker=dict(color=border_color, size=10, line=dict(width=2, color="black")),
            hovertemplate=hovertemplate,
            name="",
            customdata=customdata,
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<span style='font-size:{title_fontsize}px'><b>{chart_title}</b></span>",
            x=0.5,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Season</span>",
        yaxis_title=f"<span style='font-size:{axis_fontsize}px'>{y_title}</span>",
        yaxis=yaxis_config,
        xaxis=dict(tickmode="linear", dtick=1),
        margin=dict(l=20, r=60, t=80, b=60),
        height=400,
        template="plotly_white",
        showlegend=False,
        hovermode="x unified",
        dragmode=False,
    )

    return fig
