import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from dash.dash_table import DataTable
from config.config import CONFIG
from components.dropdown_options import build_dropdown_option

dash.register_page(
    __name__,
    path="/game-decisions",
    name="Game Decisions",
    title="Game Decisions | CFB4thDown",
)

# Load the data
df = pd.read_parquet("data/game_decisions.parquet")

# Get unique conferences and years for dropdowns
all_conferences = sorted(df["Offense Conference"].dropna().unique())
all_years = sorted(df["Season"].unique(), reverse=True)


def build_filter_control(label, control, class_name="dashboard-control"):
    return html.Div(
        [html.Div(label, className="dashboard-control-label"), control],
        className=class_name,
    )


layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [
                        html.Div("Game Decisions", className="tendencies-section-kicker"),
                        html.H2(
                            "Explore and evaluate in-game 4th down decisions.",
                            className="tendencies-section-title",
                        ),
                    ],
                    className="tendencies-section-header",
                ),
                html.Div(
                    [
                        build_filter_control(
                            "Conference",
                            dcc.Dropdown(
                                id="conference-dropdown",
                                options=[
                                    build_dropdown_option(conf)
                                    for conf in all_conferences
                                ],
                                value="Big Ten",
                                placeholder="Select Conference",
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--medium",
                        ),
                        build_filter_control(
                            "Season",
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=[
                                    build_dropdown_option(str(year), year)
                                    for year in all_years
                                ],
                                value=df["Season"].max(),
                                placeholder="Select Season",
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--compact",
                        ),
                        build_filter_control(
                            "Offense",
                            dcc.Dropdown(
                                id="offense-team-dropdown",
                                placeholder="Select",
                                multi=False,
                                value="Wisconsin",
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--medium",
                        ),
                        build_filter_control(
                            "Week",
                            dcc.Dropdown(
                                id="week-dropdown",
                                placeholder="Select",
                                multi=False,
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--compact",
                        ),
                        build_filter_control(
                            "Recommendation",
                            dcc.Dropdown(
                                id="recommendation-dropdown",
                                placeholder="Select",
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--medium",
                        ),
                        build_filter_control(
                            "Decision",
                            dcc.Dropdown(
                                id="decision-dropdown",
                                placeholder="Select",
                                multi=False,
                                className="dashboard-control-dropdown",
                            ),
                            class_name="dashboard-control dashboard-control--medium",
                        ),
                    ],
                    className="game-decisions-filter-panel dashboard-control-bar dashboard-control-bar--dense",
                ),
            ],
            fluid=True,
            style={
                "padding-left": CONFIG["padding-left"],
                "padding-right": CONFIG["padding-right"],
                "fontFamily": "Arial, sans-serif",
            },
            className="responsive-container",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                DataTable(
                                    id="decision-table",
                                    columns=[
                                        {
                                            "name": ["", "Week"],
                                            "id": "Week",
                                            "type": "numeric",
                                        },
                                        {
                                            "name": ["Offense", "Team"],
                                            "id": "Offense Team",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Offense", "ELO ⓘ"],
                                            "id": "Pregame Offense Elo",
                                            "type": "numeric",
                                        },
                                        {
                                            "name": ["Offense", "Score"],
                                            "id": "Offense Score",
                                            "type": "numeric",
                                        },
                                        {
                                            "name": ["Defense", "Team"],
                                            "id": "Defense Team",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Defense", "ELO ⓘ"],
                                            "id": "Pregame Defense Elo",
                                            "type": "numeric",
                                        },
                                        {
                                            "name": ["Defense", "Score"],
                                            "id": "Defense Score",
                                            "type": "numeric",
                                        },
                                        {"name": ["Game State", "Time"], "id": "Time"},
                                        {
                                            "name": ["Game State", "Down & Dist"],
                                            "id": "Down & Distance",
                                        },
                                        {
                                            "name": ["Game State", "YTG ⓘ"],
                                            "id": "Yards to Goal",
                                            "type": "numeric",
                                        },
                                        # New Win Probability columns
                                        {
                                            "name": ["Expected Win Prob", "Go"],
                                            "id": "Win Probability Go",
                                            "type": "numeric",
                                            "format": {"specifier": ".2%"},
                                        },
                                        {
                                            "name": ["Expected Win Prob", "Field Goal"],
                                            "id": "Win Probability Field Goal",
                                            "type": "numeric",
                                            "format": {"specifier": ".2%"},
                                        },
                                        {
                                            "name": ["Expected Win Prob", "Punt"],
                                            "id": "Win Probability Punt",
                                            "type": "numeric",
                                            "format": {"specifier": ".2%"},
                                        },
                                        # Play Outcome columns
                                        {
                                            "name": ["Play Outcome", "Recommendation"],
                                            "id": "Recommendation",
                                        },
                                        {
                                            "name": ["Play Outcome", "Decision"],
                                            "id": "Decision",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Play Outcome", "Play Desc"],
                                            "id": "Desc",
                                        },
                                    ],
                                    cell_selectable=False,
                                    page_size=20,
                                    page_action="native",
                                    sort_action="native",
                                    filter_action="none",  # Disable the built-in filtering
                                    merge_duplicate_headers=True,
                                    style_table={
                                        "overflowX": "auto",
                                        "height": "100%",
                                        "minHeight": "400px",
                                        "fontFamily": "Arial, sans-serif",
                                        "width": "100%",
                                        "minWidth": "none",
                                    },
                                    style_header={
                                        "fontWeight": "bold",
                                        "border": "none",
                                        "fontFamily": "Arial, sans-serif",
                                        "textAlign": "center",
                                    },
                                    style_header_conditional=[
                                        {
                                            "if": {"header_index": 0},
                                            "fontWeight": "bold",
                                            "textAlign": "center",
                                            "borderBottom": "2px solid var(--border-color)",
                                        },
                                    ],
                                    style_cell={
                                        "backgroundColor": "var(--surface-bg-darker)",
                                        "textAlign": "center",
                                        "padding": "8px 10px",
                                        "whiteSpace": "normal",
                                        "height": "auto",
                                        "border": "none",
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "14px",
                                        "lineHeight": "1.3",
                                        "minWidth": "80px",
                                        "maxWidth": "300px",
                                        "overflow": "hidden",
                                        "textOverflow": "ellipsis",
                                    },
                                    style_cell_conditional=[
                                        {
                                            "if": {"column_id": "Desc"},
                                            "minWidth": "200px",
                                            "textAlign": "left",
                                        },
                                        {
                                            "if": {"column_id": "Recommendation"},
                                            "minWidth": "150px",
                                        },
                                        {
                                            "if": {"column_id": "Offense Team"},
                                            "minWidth": "150px",
                                            "textAlign": "left",
                                        },
                                        {
                                            "if": {"column_id": "Defense Team"},
                                            "minWidth": "150px",
                                            "textAlign": "left",
                                        },
                                        {
                                            "if": {"column_id": "Decision"},
                                            "minWidth": "100px",
                                        },
                                        {
                                            "if": {
                                                "column_id": [
                                                    "Week",
                                                    "Pregame Offense Elo",
                                                    "Offense Score",
                                                    "Pregame Defense Elo",
                                                    "Defense Score",
                                                    "Yards to Goal",
                                                ]
                                            },
                                            "textAlign": "center",
                                        },
                                        # Add vertical borders between major sections
                                        {
                                            "if": {"column_id": "Week"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Offense Score"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Defense Score"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Yards to Goal"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Win Probability Punt"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                    ],
                                    style_data={
                                        "backgroundColor": "var(--surface-bg)",
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "14px",
                                        "lineHeight": "1.3",
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"row_index": "odd"},
                                            "backgroundColor": "var(--table-stripe-bg)",
                                        },
                                    ],
                                    tooltip_delay=0,
                                    tooltip_duration=None,
                                    tooltip_header={
                                        "Pregame Offense Elo": [
                                            "",
                                            "Pregame team Elo rating, representing estimated team strength.",
                                        ],
                                        "Pregame Defense Elo": [
                                            "",
                                            "Pregame team Elo rating, representing estimated team strength.",
                                        ],
                                        "Yards to Goal": [
                                            "",
                                            "Distance from the line of scrimmage to the end zone.",
                                        ],
                                    },
                                    markdown_options={"html": True},
                                )
                            ],
                            fluid=True,
                            className="p-0",
                            style={
                                "borderRadius": "3px",
                                "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
                                "padding": "0px",
                                "overflow": "hidden",
                                "width": "100%",
                                "margin": "0 auto",
                            },
                        )
                    ],
                    xs=12,
                    className="mb-4 px-0",
                    style={"overflow": "hidden"},
                ),
            ],
            style={"margin": "0", "padding": "0", "width": "100%"},
        ),
    ],
    style={
        "paddingLeft": CONFIG["padding-left"],
        "paddingRight": CONFIG["padding-right"],
        "fontFamily": "Arial, sans-serif",
        "width": "100%",
        "maxWidth": "none",
        "@media (max-width: 480px)": {"paddingLeft": "8px", "paddingRight": "8px"},
    },
    className="responsive-container game-decisions-page",
)


@dash.callback(
    Output("offense-team-dropdown", "options"),
    Output("week-dropdown", "options"),
    Output("recommendation-dropdown", "options"),
    Output("decision-dropdown", "options"),
    Input("conference-dropdown", "value"),
    Input("year-dropdown", "value"),
)
def update_dropdown_options(selected_conference, selected_year):
    dff = df[df["Season"] == selected_year]
    dff = dff[dff["Offense Conference"] == selected_conference]

    offense_teams = [
        build_dropdown_option(team) for team in sorted(dff["Offense Team"].unique())
    ]
    weeks = [build_dropdown_option(week) for week in sorted(dff["Week"].unique())]

    # Only show these three options in recommendation dropdown
    recommendations = [
        build_dropdown_option("Field Goal"),
        build_dropdown_option("Go"),
        build_dropdown_option("Punt"),
    ]

    decisions = [build_dropdown_option(dec) for dec in sorted(dff["Decision"].unique())]

    return offense_teams, weeks, recommendations, decisions


@dash.callback(
    Output("decision-table", "data"),
    Input("conference-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("offense-team-dropdown", "value"),
    Input("week-dropdown", "value"),
    Input("recommendation-dropdown", "value"),
    Input("decision-dropdown", "value"),
)
def update_table(
    selected_conference,
    selected_year,
    selected_team,
    selected_week,
    selected_recommendation,
    selected_decision,
):
    dff = df[df["Season"] == selected_year]
    dff = dff[dff["Offense Conference"] == selected_conference]

    # Apply filters
    if selected_team:
        dff = dff[dff["Offense Team"] == selected_team]
    if selected_week:
        dff = dff[dff["Week"] == selected_week]
    if selected_recommendation:
        # Special handling for each recommendation type
        if selected_recommendation == "Go":
            dff = dff[
                dff["Recommendation"].str.contains(r"\bGo\b", case=False, regex=True)
            ]
        elif selected_recommendation == "Field Goal":
            dff = dff[dff["Recommendation"].str.contains("Field Goal", case=False)]
        elif selected_recommendation == "Punt":
            dff = dff[dff["Recommendation"].str.contains("Punt", case=False)]
    if selected_decision:
        dff = dff[dff["Decision"] == selected_decision]

    def recommendation_bucket(value):
        text = str(value).strip().lower()
        if "field goal" in text:
            return "field goal"
        if "punt" in text:
            return "punt"
        if "go" in text:
            return "go"
        return text

    def decision_bucket(value):
        text = str(value).strip().lower()
        if text == "field goal":
            return "field goal"
        if text == "punt":
            return "punt"
        if text == "go":
            return "go"
        return text

    dff["_decision_match"] = dff.apply(
        lambda row: (
            "match"
            if decision_bucket(row["Decision"])
            == recommendation_bucket(row["Recommendation"])
            else "mismatch"
        ),
        axis=1,
    )

    # Convert team names to markdown with logos
    dff["Offense Team"] = dff.apply(
        lambda x: f"<img src='{x['Offense Logo']}' style='height:30px; margin-right:5px;'> {x['Offense Team']}",
        axis=1,
    )
    dff["Defense Team"] = dff.apply(
        lambda x: f"<img src='{x['Defense Logo']}' style='height:30px; margin-right:5px;'> {x['Defense Team']}",
        axis=1,
    )
    dff["Decision"] = dff.apply(
        lambda row: (
            f"<span class='decision-chip decision-chip-{row['_decision_match']}'>{row['Decision']}</span>"
        ),
        axis=1,
    )

    return dff.to_dict("records")
