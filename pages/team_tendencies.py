import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from config.config import CONFIG
from components.theme import (
    apply_plotly_theme,
    build_responsive_plot_title,
    get_plot_title_margin,
)

dash.register_page(
    __name__,
    path="/team-tendencies",
    name="Team Tendencies",
    title="Team Tendencies | CFB4thDown",
)

df = pd.read_parquet("data/team_tendencies.parquet")

PLOT_HEIGHT = 400

layout = dbc.Container(
    [
        html.Div(
            [
                html.Div("Comparison", className="tendencies-section-kicker"),
                html.H2(
                    "Team Fourth-Down Tendencies",
                    className="tendencies-section-title",
                ),
                html.P(
                    "Compare how teams behave on fourth down and how their decisions impact win probability.",
                    className="tendencies-section-subtitle",
                ),
            ],
            className="tendencies-section-header mt-2",
        ),
        html.Div(
            [
                html.Div("Filters", className="tendencies-filter-title"),
                dbc.Row(
                    [
                        # Conference Dropdown
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText(
                                            "Conference:",
                                            style={
                                                "height": "34px",
                                                "border-top-right-radius": "0",
                                                "border-bottom-right-radius": "0",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="conference-dropdown",
                                            options=[
                                                {"label": conf, "value": conf}
                                                for conf in ["All"]
                                                + sorted(
                                                    df["offense_conference"]
                                                    .dropna()
                                                    .unique()
                                                )
                                            ],
                                            placeholder="Select Conference",
                                            value="Big Ten",
                                            style={
                                                "minWidth": "200px",
                                                "height": "36px",
                                                "border-top-left-radius": "0",
                                                "border-bottom-left-radius": "0",
                                                "fontSize": "13px",
                                                "whiteSpace": "nowrap",
                                                "color": "#252626",
                                            },
                                        ),
                                    ],
                                    className="justify-content-xl-end justify-content-center px-xl-3",
                                    style={"flexWrap": "nowrap"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl=4,
                        ),
                        # Season
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText(
                                            "Season:",
                                            style={
                                                "height": "34px",
                                                "border-top-right-radius": "0",
                                                "border-bottom-right-radius": "0",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="season-dropdown",
                                            options=[
                                                {"label": str(s), "value": s}
                                                for s in sorted(df["season"].unique())
                                            ],
                                            value=2025
                                            if 2025 in df["season"].unique()
                                            else df["season"].max(),
                                            placeholder="Select Season",
                                            style={
                                                "minWidth": "120px",
                                                "height": "36px",
                                                "border-top-left-radius": "0",
                                                "border-bottom-left-radius": "0",
                                                "fontSize": "13px",
                                                "whiteSpace": "nowrap",
                                                "color": "#252626",
                                            },
                                        ),
                                    ],
                                    className="justify-content-xl-start justify-content-center",
                                    style={"flexWrap": "nowrap"},
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl=3,
                        ),
                        dbc.Col(
                            [
                                dbc.RadioItems(
                                    id="team-summary-metric-radio",
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
                                    className="tendencies-metric-radio d-flex justify-content-center justify-content-xl-start gap-3 pt-2",
                                    inputCheckedClassName="border border-dark bg-dark",
                                )
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl=5,
                            className="justify-content-xl-start justify-content-center",
                            style={"flexWrap": "nowrap"},
                        ),
                    ],
                    className="mb-0 g-3 align-items-center",
                ),
            ],
            className="tendencies-filter-panel",
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
                                            [
                                                html.Button(
                                                    html.I(className="bi bi-download"),
                                                    id="team-summary-download-button",
                                                    className="plot-action-button plot-download-button",
                                                    title="Download chart",
                                                    type="button",
                                                    **{
                                                        "data-graph-id": "team-summary-graph",
                                                        "data-filename": "team-summary-chart",
                                                        "data-export-width": "450",
                                                        "data-export-height": "550",
                                                    },
                                                ),
                                                html.Button(
                                                    html.Img(
                                                        src="/assets/logos/more_info.png",
                                                        className="info-icon",
                                                    ),
                                                    id="team-summary-info-icon",
                                                    className="plot-action-button plot-info-button",
                                                    title="About this chart",
                                                    type="button",
                                                ),
                                            ],
                                            className="plot-action-bar",
                                        ),
                                        dcc.Graph(
                                            id="team-summary-graph",
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
                                    id="team-summary-tooltip",
                                    target="team-summary-info-icon",
                                    placement="left",
                                    style={
                                        "maxWidth": "300px",
                                        "fontSize": "13px",
                                        "zIndex": "1000",
                                        "whiteSpace": "pre-line",
                                    },
                                ),
                            ],
                            className="bg-white tendencies-chart-card",
                            style={
                                "padding-left": "20px",
                                "border-radius": "16px",
                                "height": "100%",
                                "min-height": "400px",
                            },
                        )
                    ],
                    xs=12,
                    xl=12,
                    className="mb-4 px-1 pb-1 pt-1",
                ),
            ]
        ),
        html.Div(className="tendencies-section-divider"),
        html.Div(
            [
                html.Div("Trends", className="tendencies-section-kicker"),
                html.H2(
                    "Fourth-Down Trends Over Time",
                    className="tendencies-section-title",
                ),
                html.P(
                    "Track how a team's fourth-down decision making has evolved across seasons.",
                    className="tendencies-section-subtitle",
                ),
            ],
            className="tendencies-section-header",
        ),
        html.Div(
            [
                html.Div("Filters", className="tendencies-filter-title"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText(
                                            "Team:",
                                            style={
                                                "height": "34px",
                                                "border-top-right-radius": "0",
                                                "border-bottom-right-radius": "0",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="team-dropdown",
                                            options=[
                                                {"label": team, "value": team}
                                                for team in sorted(
                                                    df["offense_team"].unique()
                                                )
                                            ],
                                            placeholder="Select Team",
                                            value="Notre Dame",
                                            style={
                                                "minWidth": "200px",
                                                "height": "36px",
                                                "border-top-left-radius": "0",
                                                "border-bottom-left-radius": "0",
                                                "fontSize": "13px",
                                                "whiteSpace": "nowrap",
                                                "color": "#252626",
                                            },
                                        ),
                                    ],
                                    className="justify-content-center",
                                    style={"flexWrap": "nowrap"},
                                )
                            ],
                            xs=12,
                            md=6,
                            className="mb-0",
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
                                    className="tendencies-metric-radio d-flex justify-content-center justify-content-md-start gap-3 pt-2",
                                    inputCheckedClassName="border border-dark bg-dark",
                                )
                            ],
                            xs=12,
                            md=6,
                            className="mb-0 d-flex align-items-center",
                        ),
                    ],
                    className="mb-0 g-3 align-items-center",
                ),
            ],
            className="tendencies-filter-panel",
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
                                            [
                                                html.Button(
                                                    html.I(className="bi bi-download"),
                                                    id="team-trend-download-button",
                                                    className="plot-action-button plot-download-button",
                                                    title="Download chart",
                                                    type="button",
                                                    **{
                                                        "data-graph-id": "team-trend-graph",
                                                        "data-filename": "team-trend-chart",
                                                        "data-export-width": "700",
                                                        "data-export-height": "500",
                                                    },
                                                ),
                                                html.Button(
                                                    html.Img(
                                                        src="/assets/logos/more_info.png",
                                                        className="info-icon",
                                                    ),
                                                    id="info-icon3",
                                                    className="plot-action-button plot-info-button",
                                                    title="About this chart",
                                                    type="button",
                                                ),
                                            ],
                                            className="plot-action-bar",
                                        ),
                                        dcc.Graph(
                                            id="team-trend-graph",
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
                                    id="team-trend-tooltip",
                                    children="",
                                    target="info-icon3",
                                    placement="left",
                                    style={
                                        "maxWidth": "300px",
                                        "fontSize": "13px",
                                        "zIndex": "1000",
                                        "whiteSpace": "pre-line",
                                    },
                                ),
                            ],
                            className="bg-white tendencies-chart-card",
                            style={
                                "padding-left": "20px",
                                "border-radius": "16px",
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
    className="responsive-container tendencies-page team-tendencies-page",
)


@dash.callback(
    Output("team-summary-graph", "figure"),
    Output("team-summary-tooltip", "children"),
    Input("season-dropdown", "value"),
    Input("conference-dropdown", "value"),
    Input("team-summary-metric-radio", "value"),
    Input("screen-width-store", "data"),
    Input("theme-store", "data"),
)
def update_graphs(
    selected_season, selected_conference, selected_metric, screen_width, theme
):
    is_dark = theme == "dark"
    dff = df[df["season"] == selected_season]
    if selected_conference != "All":
        dff = dff[dff["offense_conference"] == selected_conference]

    if screen_width < 768:
        axis_fontsize = 11
    else:
        axis_fontsize = 13

    grouped = dff.groupby(
        ["offense_team", "fill_color", "border_color", "offense_logos"], as_index=False
    ).agg({"n_go": "sum", "n_go_rec": "sum", "net_wp_lost": "sum"})

    grouped = grouped[grouped["n_go_rec"] > 0].copy()
    grouped["go_for_it_rate"] = grouped["n_go"] / grouped["n_go_rec"]
    grouped["avg_wp_lost_per_season"] = grouped["net_wp_lost"]

    ### PLOT 1
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)
    fig1 = go.Figure()

    fig1.add_trace(
        go.Bar(
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
            hovertemplate="<b>%{y}</b> (%{customdata[0]} play(s))<extra></extra>",
            name="",
            showlegend=False,
            customdata=grouped_sorted1[["n_go_rec"]].values,
        )
    )

    max_x1 = grouped_sorted1["go_for_it_rate"].max() if not grouped_sorted1.empty else 1
    bottom_margin = 80
    min_height = 400
    BAR_HEIGHT = 20
    BAR_GAP = 10
    x_range_multiplier = 1.15
    calculated_height = len(grouped_sorted1) * (BAR_HEIGHT + BAR_GAP) + 150
    global PLOT_HEIGHT
    PLOT_HEIGHT = max(calculated_height, min_height)

    for _, row in grouped_sorted1.iterrows():
        fig1.add_layout_image(
            dict(
                source=row["offense_logos"],
                x=row["go_for_it_rate"] + (max_x1 * 0.02),
                y=row["offense_team"],
                xref="x",
                yref="y",
                sizex=1,
                sizey=0.8,
                xanchor="left",
                yanchor="middle",
                layer="above",
            )
        )

    fig1_title = build_responsive_plot_title(
        "Go-For-It Rate",
        subtitle="Percentage of analytically-recommended go situations where the team actually goes for it.",
        screen_width=screen_width,
        columns=2,
        subtitle_width_factor=0.5,
    )

    fig1.update_layout(
        title=dict(
            text=fig1_title["text"],
            xanchor="center",
            x=0.5,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Percent of time team went for it when recommended</span>",
        yaxis=dict(
            fixedrange=True,
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted1["offense_team"].tolist(),
            showticklabels=False,
            showgrid=False,
        ),
        xaxis=dict(
            fixedrange=True,
            tickformat=".0%",
            range=[0, max_x1 * x_range_multiplier if max_x1 > 0 else 1],
        ),
        margin=dict(
            l=20,
            r=60,
            t=get_plot_title_margin(fig1_title["lines"], has_subtitle=True, base=100),
            b=bottom_margin,
        ),
        meta={
            "export_title": "Go-For-It Rate",
            "export_subtitle": "Percentage of analytically-recommended go situations where the team actually goes for it.",
        },
        height=PLOT_HEIGHT,
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
            hovertemplate="<b>%{y}</b><extra></extra>",
            name="",
            showlegend=False,
        )
    )

    max_x2 = (
        grouped_sorted2["avg_wp_lost_per_season"].max()
        if not grouped_sorted2.empty
        else 1
    )

    for _, row in grouped_sorted2.iterrows():
        fig2.add_layout_image(
            dict(
                source=row["offense_logos"],
                x=row["avg_wp_lost_per_season"] + (max_x2 * 0.02),
                y=row["offense_team"],
                xref="x",
                yref="y",
                sizex=1,
                sizey=0.8,
                xanchor="left",
                yanchor="middle",
                layer="above",
            )
        )

    fig2_title = build_responsive_plot_title(
        "Win Probability Lost",
        subtitle="Due to not going for it on 4th down when analytically recommended",
        screen_width=screen_width,
        columns=2,
        subtitle_width_factor=0.5,
    )

    fig2.update_layout(
        title=dict(
            text=fig2_title["text"],
            xanchor="center",
            x=0.5,
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>WP Lost (percentage points)</span>",
        yaxis=dict(
            fixedrange=True,
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted2["offense_team"].tolist(),
            showticklabels=False,
            showgrid=False,
        ),
        xaxis=dict(
            fixedrange=True,
            tickformat=".0%",
            range=[0, max_x2 * x_range_multiplier if max_x2 > 0 else 1],
        ),
        margin=dict(
            l=20,
            r=60,
            t=get_plot_title_margin(fig2_title["lines"], has_subtitle=True, base=100),
            b=bottom_margin,
        ),
        meta={
            "export_title": "Win Probability Lost",
            "export_subtitle": "Due to not going for it on 4th down when analytically recommended",
        },
        height=PLOT_HEIGHT,
        barmode="overlay",
        bargap=0.2,
        bargroupgap=0.05,
        dragmode=False,
    )

    apply_plotly_theme(fig1, is_dark)
    apply_plotly_theme(fig2, is_dark)

    tooltip_go_rate = "Higher values indicate that a team often follows the model’s recommendation to go for it on fourth down. Lower values suggest a more conservative approach, even when going for it would increase expected win probability. This metric only includes situations where the model recommends going for it."
    tooltip_wp_lost = "This chart shows the average win probability lost for the teams in a given conference. Win probability is lost when a team punts or attempts a field goal instead of going for it when recommended by the model. Higher values indicate a greater expected cost from conservative fourth-down decisions."

    if selected_metric == "go_rate":
        return fig1, tooltip_go_rate

    return fig2, tooltip_wp_lost


@dash.callback(
    Output("team-trend-graph", "figure"),
    Output("team-trend-tooltip", "children"),
    Input("team-dropdown", "value"),
    Input("trend-metric-radio", "value"),
    Input("screen-width-store", "data"),
    Input("theme-store", "data"),
)
def update_trend_graph(selected_team, selected_metric, screen_width, theme):
    is_dark = theme == "dark"
    if selected_team is None:
        return go.Figure(), ""

    team_df = df[df["offense_team"] == selected_team]
    team_data = (
        team_df.groupby("season")
        .agg(
            n_go=("n_go", "sum"),
            n_go_rec=("n_go_rec", "sum"),
            net_wp_lost=("net_wp_lost", "sum"),
            fill_color=("fill_color", "first"),
            border_color=("border_color", "first"),
            offense_logos=("offense_logos", "first"),
        )
        .reset_index()
        .sort_values("season")
    )

    team_data = team_data[team_data["n_go_rec"] > 0].copy()
    team_data["go_rate"] = team_data["n_go"] / team_data["n_go_rec"]
    team_data["wp_lost"] = team_data["net_wp_lost"]

    if team_data.empty:
        return go.Figure(), ""

    if screen_width < 768:
        axis_fontsize = 11
        title_fontsize = 14
        logo_size = 0.8
    else:
        axis_fontsize = 13
        title_fontsize = 16
        logo_size = 1

    fill_color = team_data["fill_color"].iloc[0]
    border_color = team_data["border_color"].iloc[0]
    logo = team_data["offense_logos"].iloc[0]

    if selected_metric == "go_rate":
        y_col = "go_rate"
        y_title = "Go-For-It Rate When Recommended"
        chart_title = f"{selected_team} Go-For-It Rate When Recommended Over Time"
        chart_subtitle = "Percentage of analytically-recommended go situations where the team actually goes for it."
        hovertemplate = "<b>Season %{x}</b><br>Go Rate: %{y:.1%}<extra></extra>"
        tooltip_text = (
            "This chart shows how often "
            f"{selected_team} went for it when the model recommended doing so in each season. "
            "Higher values indicate the team followed high-leverage fourth-down recommendations more consistently over time."
        )
        yaxis_config = dict(
            tickformat=".0%",
            range=[0, min(1.1, max(team_data[y_col].max() * 1.1, 0.1))],
        )
    else:
        y_col = "wp_lost"
        y_title = "Win Probability Lost"
        chart_title = f"{selected_team} Win Probability Lost Over Time"
        chart_subtitle = (
            "Due to not going for it on 4th down when analytically recommended"
        )
        hovertemplate = "<b>Season %{x}</b><br>WP Lost: %{y:.1%}<extra></extra>"
        tooltip_text = (
            "This chart shows the estimated win probability "
            f"{selected_team} gave up in each season by not going for it when the model recommended it. "
            "Higher values indicate a larger cumulative cost from conservative fourth-down choices."
        )
        y_max = team_data[y_col].max()
        yaxis_config = dict(
            tickformat=".0%",
            range=[0, max(y_max * 1.15, 0.01)],
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=team_data["season"],
            y=team_data[y_col],
            mode="lines+markers",
            line=dict(color="rgba(210, 210, 210, 0.92)", width=5),
            marker=dict(color="rgba(210, 210, 210, 0.92)", size=12),
            hoverinfo="skip",
            showlegend=False,
            name="",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=team_data["season"],
            y=team_data[y_col],
            mode="lines+markers",
            line=dict(color=fill_color, width=3),
            marker=dict(
                color=border_color,
                size=10,
                line=dict(width=2, color="#D1CFCF" if is_dark else "black"),
            ),
            hovertemplate=hovertemplate,
            name="",
        )
    )

    fig.add_layout_image(
        dict(
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
        )
    )

    trend_title = build_responsive_plot_title(
        chart_title,
        subtitle=chart_subtitle,
        screen_width=screen_width,
        columns=1,
        title_font_size=title_fontsize,
        title_width_factor=0.7,
        subtitle_width_factor=0.55,
    )

    fig.update_layout(
        title=dict(
            text=trend_title["text"],
            x=0.5,
            xanchor="center",
        ),
        xaxis_title=f"<span style='font-size:{axis_fontsize}px'>Season</span>",
        yaxis_title=f"<span style='font-size:{axis_fontsize}px'>{y_title}</span>",
        yaxis=yaxis_config,
        xaxis=dict(tickmode="linear", dtick=1),
        margin=dict(
            l=20,
            r=60,
            t=get_plot_title_margin(trend_title["lines"], has_subtitle=True, base=100),
            b=60,
        ),
        meta={
            "export_title": chart_title,
            "export_subtitle": chart_subtitle,
        },
        height=400,
        showlegend=False,
        hovermode="x unified",
        dragmode=False,
    )

    apply_plotly_theme(fig, is_dark)

    return fig, tooltip_text
