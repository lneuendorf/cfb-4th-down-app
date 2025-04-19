import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path="/team-tendencies", name="Team Tendencies")

# Load data once
df = pd.read_parquet("data/team_tendencies.parquet")

layout = dbc.Container([
    html.H2("Team Tendencies", className="mt-4"),
    html.P("Explore how different teams behave on 4th down."),

    dbc.Row([
        dbc.Col([
            dcc.RangeSlider(
                id='season-range',
                min=df['season'].min(),
                max=df['season'].max(),
                step=1,
                value=[df['season'].min(), df['season'].max()],
                marks={str(season): str(season) for season in sorted(df['season'].unique())},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ])
    ], className="my-3"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='conference-dropdown',
                options=[{'label': conf, 'value': conf} for conf in sorted(df['offense_conference'].dropna().unique())],
                placeholder="Select a Conference",
                multi=False,
                value='Big Ten',  # Default value
            )
        ])
    ], className="mb-3"),

    dcc.Graph(id="team-tendency-graph", config={"displayModeBar": False, "staticPlot": True}),
    dcc.Graph(id="wp-lost-graph", config={"displayModeBar": False, "staticPlot": True})
], fluid=True)


@dash.callback(
    Output("team-tendency-graph", "figure"),
    Output("wp-lost-graph", "figure"),
    Input("season-range", "value"),
    Input("conference-dropdown", "value")
)
def update_graphs(season_range, selected_conference):
    dff = df[(df["season"] >= season_range[0]) & (df["season"] <= season_range[1])]
    if selected_conference:
        dff = dff[dff["offense_conference"] == selected_conference]

    grouped = (
        dff.groupby(["offense_team", "offense_color", "offense_alternate_color", "offense_logos"], as_index=False)
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

    # Plot 1: Go For It Rate
    fig1 = go.Figure()
    grouped_sorted1 = grouped.sort_values("go_for_it_rate", ascending=True)

    fig1.add_trace(go.Bar(
        x=grouped_sorted1["go_for_it_rate"],
        y=grouped_sorted1["offense_team"],
        orientation="h",
        marker_color=grouped_sorted1["offense_color"],
        marker_line_color=grouped_sorted1["offense_alternate_color"],
        marker_line_width=1.5,
        text=[f"{x:.1%} (n={n})" for x, n in zip(grouped_sorted1["go_for_it_rate"], grouped_sorted1["n_go_rec"])],
        textposition="inside",
        insidetextanchor="end",  # places text near end of bar
        textfont=dict(color="white", size=12),
        hoverinfo="skip",  # disables hover
        hovertemplate=None  # also disables hover
    ))

    for i, row in grouped_sorted1.iterrows():
        fig1.add_layout_image(
            dict(
                source=row["offense_logos"],
                x=row["go_for_it_rate"] + 0.01,
                y=row["offense_team"],
                xref="x",
                yref="y",
                sizex=0.03,
                sizey=1,
                xanchor="left",
                yanchor="middle",
                layer="above"
            )
        )

    fig1.update_layout(
        title="Go For It Rate by Team",
        xaxis_title="Go For It Rate",
        yaxis_title="",
        xaxis_tickformat=".0%",
        margin=dict(l=120, r=80, t=60, b=60),
        height=max(400, 30 * len(grouped_sorted1)),
        template="plotly_white",
        yaxis=dict(
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted1["offense_team"].tolist(),
        )
    )

    # Plot 2: Average Win Probability Lost per Season
    fig2 = go.Figure()
    grouped_sorted2 = grouped.sort_values("avg_wp_lost_per_season", ascending=True)

    fig2.add_trace(go.Bar(
        x=grouped_sorted2["avg_wp_lost_per_season"],
        y=grouped_sorted2["offense_team"],
        orientation="h",
        marker_color=grouped_sorted2["offense_color"],
        marker_line_color=grouped_sorted2["offense_alternate_color"],
        marker_line_width=1.5,
        text=[f"{wp:.3f} (n={n})" for wp, n in zip(grouped_sorted2["avg_wp_lost_per_season"], grouped_sorted2["n_season"])],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="skip",
        hovertemplate=None
    ))


    x_range = grouped_sorted2["avg_wp_lost_per_season"].max() - grouped_sorted2["avg_wp_lost_per_season"].min()
    logo_sizex = x_range * 0.03  # same relative size as fig1

    for i, row in grouped_sorted2.iterrows():
        fig2.add_layout_image(
            dict(
                source=row["offense_logos"],
                x=row["avg_wp_lost_per_season"] + logo_sizex * 0.15,
                y=row["offense_team"],
                xref="x",
                yref="y",
                sizex=logo_sizex,
                sizey=1,
                xanchor="left",
                yanchor="middle",
                layer="above"
            )
        )

    fig2.update_layout(
        title="Average Win Probability Lost Per Season",
        xaxis_title="Avg WP Lost / Season",
        yaxis_title="",
        margin=dict(l=120, r=80, t=60, b=60),
        height=max(400, 30 * len(grouped_sorted2)),
        template="plotly_white",
        yaxis=dict(
            automargin=True,
            categoryorder="array",
            categoryarray=grouped_sorted2["offense_team"].tolist(),
        )
    )

    return fig1, fig2