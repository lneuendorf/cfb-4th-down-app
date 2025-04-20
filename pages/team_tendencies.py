import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config.config import CONFIG


dash.register_page(__name__, path="/team-tendencies", name="Team Tendencies")

# Load data once
df = (
    pd.read_parquet("data/team_tendencies.parquet")
    .replace(
        {
            "offense_color": {
                "#null": "#FFFFFF",
            },
            "offense_alternate_color": {
                "#null": "#000",
            },
        }
    )
)

# Fix: make the the darker color the bourder color column, and the lighter color the fill color
df["fill_color"] = np.where(
    df.offense_color > df.offense_alternate_color,
    df.offense_alternate_color,
    df.offense_color
)
df["border_color"] = np.where(
    df.offense_color < df.offense_alternate_color, 
    df.offense_alternate_color, 
    df.offense_color
)

# if bourder color is white, make light grey
df["border_color"] = np.where(
    df["border_color"] > "#fafafa",
    "#ebebeb",
    df["border_color"]
)

layout = dbc.Container([
    html.H4("Team Tendencies", className="mt-4", style={'color': '#000'}),
    html.P("Explore how different teams behave on 4th down."),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='start-season',
                options=[{'label': str(s), 'value': s} for s in sorted(df['season'].unique())],
                value=df['season'].min(),
                placeholder="Start Season"
            )
        ], xs=12, md=4),
        dbc.Col([
            dcc.Dropdown(
                id='end-season',
                options=[{'label': str(s), 'value': s} for s in sorted(df['season'].unique())],
                value=df['season'].max(),
                placeholder="End Season"
            )
        ], xs=12, md=4),
        dbc.Col([
            dcc.Dropdown(
                id='conference-dropdown',
                options=[{'label': conf, 'value': conf} for conf in sorted(df['offense_conference'].dropna().unique())],
                placeholder="Select Conference",
                multi=False,
                value='Big Ten',
            )
        ], xs=12, md=4)
    ], className="mb-4 g-2"),  # g-2 adds gutter spacing

    dbc.Row([
        dbc.Col([
            dbc.Container(
                dcc.Graph(id="team-tendency-graph", config={"displayModeBar": False}),
                className="bg-white p-3",
                style={"border-radius": "16px", "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)"}
            )
        ], xs=12, xl=6, className="mb-4"),
        dbc.Col([
            dbc.Container(
                dcc.Graph(id="wp-lost-graph", config={"displayModeBar": False}),
                className="bg-white p-3",
                style={"border-radius": "16px", "box-shadow": "0 2px 6px rgba(0,0,0,0.05), 0 0 5px rgba(0,0,0,0.1)"}
            )
        ], xs=12, xl=6, className="mb-4")
    ])
], 
fluid=True,
style={
    "padding-left": CONFIG['padding-left'],
    "padding-right": CONFIG['padding-right'],
    "max-width": CONFIG['max-width'],
})


@dash.callback(
    Output("team-tendency-graph", "figure"),
    Output("wp-lost-graph", "figure"),
    Input("start-season", "value"),
    Input("end-season", "value"),
    Input("conference-dropdown", "value")
)
def update_graphs(start_season, end_season, selected_conference):
    dff = df[(df["season"] >= start_season) & (df["season"] <= end_season)]
    if selected_conference:
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
        hoverinfo="skip",
        hovertemplate=None,
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
    logo_sizex = 0.03 * (1 + (14 / len(grouped_sorted1)))  # Dynamic logo size based on number of teams
    
    # Calculate bottom margin based on number of teams
    bottom_margin = 80 + (10 if len(grouped_sorted1) > 10 else 0)

    for _, row in grouped_sorted1.iterrows():
        fig1.add_layout_image(dict(
            source=row["offense_logos"],
            x=row["go_for_it_rate"] + (max_x1 * 0.02),
            y=row["offense_team"],
            xref="x",
            yref="y",
            sizex=logo_sizex,
            sizey=0.8,  # Slightly reduced sizey for better mobile display
            xanchor="left",
            yanchor="middle",
            layer="above"
        ))

    fig1.update_layout(
        title=dict(
            text="Go-For-It Rate When Recommended<br><sub>Plays in final 30 seconds excluded. 'Optimal' defined as +1.5% WP over kicking</sub>",
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
            range=[0, max_x1 * 1.15]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height= 40 * len(grouped_sorted1),
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,  # Increased gap between bars
        bargroupgap=0.05
    )
    
    # Add annotation for sample size
    fig1.add_annotation(
        x=0.5, y=-0.08,  # Adjusted y position to be below axis label
        xref="paper", yref="paper",
        text="(n = number of plays where going for it was recommended)",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top"  # Changed to top anchor
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
        text=[f"{wp:.2f}%" for wp in grouped_sorted2["avg_wp_lost_per_season"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hoverinfo="skip",
        hovertemplate=None,
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

    # Calculate dynamic right margin based on max value
    max_x2 = grouped_sorted2["avg_wp_lost_per_season"].max()
    
    for _, row in grouped_sorted2.iterrows():
        fig2.add_layout_image(dict(
            source=row["offense_logos"],
            x=row["avg_wp_lost_per_season"] + (max_x2 * 0.02),
            y=row["offense_team"],
            xref="x",
            yref="y",
            sizex=logo_sizex,
            sizey=0.8,  # Slightly reduced sizey for better mobile display
            xanchor="left",
            yanchor="middle",
            layer="above"
        ))

    fig2.update_layout(
        title=dict(
            text="Average Win Probability Lost Per Season<br><sub>Due to not going for it when recommended</sub>",
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
            tickformat=".1f",  # Changed to show decimal points instead of percentage
            range=[0, max_x2 * 1.15]
        ),
        margin=dict(l=20, r=60, t=100, b=bottom_margin),
        height= 40 * len(grouped_sorted2),
        template="plotly_white",
        barmode="overlay",
        bargap=0.2,  # Increased gap between bars
        bargroupgap=0.05
    )

    fig2.add_annotation(
        x=0.5, y=-0.08,  # Adjusted y position to be below axis label
        xref="paper", yref="paper",
        text="(n = number of seasons across selected years)",
        showarrow=False,
        font=dict(size=10),
        xanchor="center",
        yanchor="top"  # Changed to top anchor
    )

    return fig1, fig2