import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from html import escape
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


def format_pct(value):
    return f"{float(value) * 100:.1f}%"


def build_team_cell(abbreviation, team_name, logo_url):
    full_name = "" if pd.isna(team_name) else str(team_name).strip()
    short_name = "" if pd.isna(abbreviation) else str(abbreviation).strip()
    display_name = short_name or full_name
    tooltip_name = full_name or display_name
    escaped_display_name = escape(display_name)
    escaped_tooltip_name = escape(tooltip_name, quote=True)

    logo_html = ""
    if pd.notna(logo_url) and str(logo_url).strip():
        escaped_logo_url = escape(str(logo_url).strip(), quote=True)
        logo_html = (
            f"<span title='{escaped_tooltip_name}' style='display:inline-flex;'>"
            f"<img src='{escaped_logo_url}' alt='{escaped_display_name}' "
            "style='height:24px; width:24px; object-fit:contain; margin-right:6px;'>"
            "</span>"
        )

    return (
        "<span style='display:inline-flex; align-items:center; white-space:nowrap;'>"
        + logo_html
        + f"<span title='{escaped_tooltip_name}'>{escaped_display_name}</span>"
        + "</span>"
    )


def build_wp_summary_cell(row):
    options = [
        ("Go", float(row["Win Probability Go"]), "go"),
        ("FG", float(row["Win Probability Field Goal"]), "fg"),
        ("Punt", float(row["Win Probability Punt"]), "punt"),
    ]
    best_value = max(value for _, value, _ in options)
    return (
        "<div class='wp-summary-cell'>"
        + "".join(
            [
                (
                    (
                        "<div class='wp-summary-row wp-summary-row-best'>"
                        if abs(value - best_value) < 1e-9
                        else "<div class='wp-summary-row'>"
                    )
                    + f"<span class='wp-summary-label'>{label}</span>"
                    + "<span class='wp-summary-track'>"
                    + f"<span class='wp-summary-fill wp-summary-fill-{css_name}' style='width: {value * 100:.1f}%;'></span>"
                    + "</span>"
                    + "<span class='wp-summary-value-block'>"
                    + f"<span class='wp-summary-value'>{format_pct(value)}</span>"
                    + f"<span class='wp-summary-delta'>{(value - best_value) * 100:+.1f}</span>"
                    + "</span>"
                    + "</div>"
                )
                for label, value, css_name in options
            ]
        )
        + "</div>"
    )


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
                                placeholder="Select",
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
                                placeholder="Select",
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
                                            "name": ["Defense", "Team"],
                                            "id": "Defense Team",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Defense", "ELO ⓘ"],
                                            "id": "Pregame Defense Elo",
                                            "type": "numeric",
                                        },
                                        {"name": ["Game State", "Score"], "id": "Score"},
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
                                        {
                                            "name": [
                                                "Expected Win Prob ⓘ",
                                                "Go / FG / Punt ⓘ",
                                            ],
                                            "id": "WP Summary",
                                            "presentation": "markdown",
                                        },
                                        # Play Outcome columns
                                        {
                                            "name": ["Play Outcome", "Rec"],
                                            "id": "Recommendation",
                                        },
                                        {
                                            "name": ["Play Outcome", "Decision"],
                                            "id": "Decision",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Play Outcome", "WP Lost ⓘ"],
                                            "id": "WP Lost",
                                            "presentation": "markdown",
                                        },
                                        {
                                            "name": ["Play Outcome", "Play Desc"],
                                            "id": "Desc",
                                        },
                                    ],
                                    cell_selectable=False,
                                    fill_width=False,
                                    page_size=20,
                                    page_action="native",
                                    sort_action="custom",
                                    filter_action="none",  # Disable the built-in filtering
                                    merge_duplicate_headers=True,
                                    style_table={
                                        "overflowX": "auto",
                                        "height": "100%",
                                        "minHeight": "400px",
                                        "fontFamily": "Arial, sans-serif",
                                        "width": "fit-content",
                                        "maxWidth": "100%",
                                        "minWidth": "auto",
                                    },
                                    style_header={
                                        "fontWeight": "bold",
                                        "border": "none",
                                        "backgroundColor": "var(--surface-bg-darker)",
                                        "color": "var(--text-color)",
                                        "fontFamily": "Arial, sans-serif",
                                        "textAlign": "center",
                                        "padding": "6px 8px",
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
                                        "padding": "6px 8px",
                                        "whiteSpace": "nowrap",
                                        "height": "auto",
                                        "border": "none",
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "14px",
                                        "lineHeight": "1.3",
                                        "minWidth": "64px",
                                        "maxWidth": "240px",
                                        "overflow": "hidden",
                                        "textOverflow": "ellipsis",
                                    },
                                    style_cell_conditional=[
                                        {
                                            "if": {"column_id": "Desc"},
                                            "minWidth": "280px",
                                            "maxWidth": "560px",
                                            "textAlign": "left",
                                            "whiteSpace": "normal",
                                        },
                                        {
                                            "if": {"column_id": "Recommendation"},
                                            "minWidth": "88px",
                                            "maxWidth": "96px",
                                        },
                                        {
                                            "if": {"column_id": "Offense Team"},
                                            "minWidth": "94px",
                                            "maxWidth": "112px",
                                            "textAlign": "left",
                                        },
                                        {
                                            "if": {"column_id": "Defense Team"},
                                            "minWidth": "94px",
                                            "maxWidth": "112px",
                                            "textAlign": "left",
                                        },
                                        {
                                            "if": {"column_id": "Decision"},
                                            "minWidth": "88px",
                                            "maxWidth": "96px",
                                        },
                                        {
                                            "if": {"column_id": "WP Lost"},
                                            "minWidth": "82px",
                                            "maxWidth": "90px",
                                            "textAlign": "center",
                                        },
                                        {
                                            "if": {"column_id": "WP Summary"},
                                            "minWidth": "220px",
                                            "maxWidth": "236px",
                                            "textAlign": "left",
                                            "whiteSpace": "normal",
                                        },
                                        {
                                            "if": {
                                                "column_id": [
                                                    "Week",
                                                    "Pregame Offense Elo",
                                                    "Pregame Defense Elo",
                                                    "Score",
                                                    "Yards to Goal",
                                                ]
                                            },
                                            "textAlign": "center",
                                        },
                                        {
                                            "if": {"column_id": "Week"},
                                            "minWidth": "48px",
                                            "maxWidth": "52px",
                                        },
                                        {
                                            "if": {"column_id": "Score"},
                                            "minWidth": "60px",
                                            "maxWidth": "70px",
                                        },
                                        {
                                            "if": {"column_id": "Pregame Offense Elo"},
                                            "minWidth": "72px",
                                            "maxWidth": "78px",
                                        },
                                        {
                                            "if": {"column_id": "Pregame Defense Elo"},
                                            "minWidth": "72px",
                                            "maxWidth": "78px",
                                        },
                                        {
                                            "if": {"column_id": "Time"},
                                            "minWidth": "70px",
                                            "maxWidth": "78px",
                                        },
                                        {
                                            "if": {"column_id": "Down & Distance"},
                                            "minWidth": "96px",
                                            "maxWidth": "108px",
                                        },
                                        {
                                            "if": {"column_id": "Yards to Goal"},
                                            "minWidth": "64px",
                                            "maxWidth": "72px",
                                        },
                                        # Add vertical borders between major sections
                                        {
                                            "if": {"column_id": "Week"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Pregame Offense Elo"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Pregame Defense Elo"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "Yards to Goal"},
                                            "borderRight": "2px solid var(--border-color)",
                                        },
                                        {
                                            "if": {"column_id": "WP Summary"},
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
                                        "WP Summary": [
                                            "Model-estimated win probability for each decision option.",
                                            "Bars are ordered Go / FG / Punt; parentheses show difference from the best option.",
                                        ],
                                        "WP Lost": [
                                            "",
                                            "Win probability lost for not choosing the model-recommended decision.",
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
    Input("decision-table", "sort_by"),
)
def update_table(
    selected_conference,
    selected_year,
    selected_team,
    selected_week,
    selected_recommendation,
    selected_decision,
    sort_by,
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

    def recommendation_contains_decision(recommendation_value, decision_value):
        recommendation_text = str(recommendation_value).strip().lower()
        decision_text = decision_bucket(decision_value)
        if decision_text == "go" and "field goal" in recommendation_text:
            return False
        recommendation_options = []
        if "field goal" in recommendation_text:
            recommendation_options.append("field goal")
        if "go" in recommendation_text:
            recommendation_options.append("go")
        if "punt" in recommendation_text:
            recommendation_options.append("punt")
        if recommendation_options:
            return decision_text in recommendation_options
        return decision_text == recommendation_text

    def decision_bucket(value):
        text = str(value).strip().lower()
        if text == "field goal":
            return "field goal"
        if text == "punt":
            return "punt"
        if text == "go":
            return "go"
        return text

    def decision_wp(row, decision_name):
        bucket = decision_bucket(decision_name)
        if bucket == "go":
            return float(row["Win Probability Go"])
        if bucket == "field goal":
            return float(row["Win Probability Field Goal"])
        if bucket == "punt":
            return float(row["Win Probability Punt"])
        return None

    def wp_lost_value(row):
        if decision_bucket(row["Decision"]) == recommendation_bucket(
            row["Recommendation"]
        ):
            return 0.0

        chosen_wp = decision_wp(row, row["Decision"])
        if chosen_wp is None:
            return None

        best_wp = max(
            float(row["Win Probability Go"]),
            float(row["Win Probability Field Goal"]),
            float(row["Win Probability Punt"]),
        )
        return max(0.0, best_wp - chosen_wp)

    def wp_lost_chip(value):
        if value is None:
            return "<span class='wp-lost-chip wp-lost-chip-na'>—</span>"
        if value <= 0.01:
            level = "low"
        elif value < 0.03:
            level = "medium"
        else:
            level = "high"
        return (
            f"<span class='wp-lost-chip wp-lost-chip-{level}'>{value * 100:.1f}%</span>"
        )

    dff["_decision_match"] = dff.apply(
        lambda row: (
            "match"
            if recommendation_contains_decision(row["Recommendation"], row["Decision"])
            else "mismatch"
        ),
        axis=1,
    )
    dff["_wp_lost"] = dff.apply(wp_lost_value, axis=1)
    dff["_wp_max"] = dff[
        [
            "Win Probability Go",
            "Win Probability Field Goal",
            "Win Probability Punt",
        ]
    ].max(axis=1)

    sort_column_map = {
        "Week": "Week",
        "Offense Team": "Offense Abbreviation",
        "Pregame Offense Elo": "Pregame Offense Elo",
        "Defense Team": "Defense Abbreviation",
        "Pregame Defense Elo": "Pregame Defense Elo",
        "Time": "Time",
        "Down & Distance": "Down & Distance",
        "Yards to Goal": "Yards to Goal",
        "WP Summary": "_wp_max",
        "Recommendation": "Recommendation",
        "Decision": "Decision",
        "WP Lost": "_wp_lost",
        "Desc": "Desc",
    }

    if sort_by:
        for sort in reversed(sort_by):
            column_id = sort.get("column_id")
            ascending = sort.get("direction") == "asc"
            if column_id == "Score":
                dff = dff.sort_values(
                    by=["Offense Score", "Defense Score"],
                    ascending=[ascending, ascending],
                    kind="stable",
                )
            elif column_id in sort_column_map:
                dff = dff.sort_values(
                    by=sort_column_map[column_id],
                    ascending=ascending,
                    kind="stable",
                    na_position="last",
                )
    else:
        dff = dff.sort_values(by=["Week"], ascending=True, kind="stable")

    # Convert team abbreviations to markdown with logos and full-name hover text
    dff["Offense Team"] = dff.apply(
        lambda row: build_team_cell(
            row["Offense Abbreviation"], row["Offense Team"], row["Offense Logo"]
        ),
        axis=1,
    )
    dff["Defense Team"] = dff.apply(
        lambda row: build_team_cell(
            row["Defense Abbreviation"], row["Defense Team"], row["Defense Logo"]
        ),
        axis=1,
    )
    dff["Score"] = dff.apply(
        lambda row: f"{int(row['Offense Score'])}\u2013{int(row['Defense Score'])}",
        axis=1,
    )
    dff["WP Summary"] = dff.apply(build_wp_summary_cell, axis=1)
    dff["WP Lost"] = dff["_wp_lost"].apply(wp_lost_chip)
    dff["Decision"] = dff.apply(
        lambda row: (
            f"<span class='decision-chip decision-chip-{row['_decision_match']}'>{row['Decision']}</span>"
        ),
        axis=1,
    )

    return dff.to_dict("records")
