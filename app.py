import dash
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
import dash_bootstrap_components as dbc
from flask import request

from components.navbar import header
from components.footer import footer

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.ZEPHYR,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css",
    ],
    update_title=None,
)

server = app.server

# Disable Flask/Dash response caching (prevents stale frontend after deploy)
server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
server.config["ETAG_DISABLED"] = True


@server.after_request
def add_cache_headers(response):
    path = request.path

    # Never cache dynamic app responses
    if path == "/" or path.startswith("/_dash-") or path == "/favicon.ico":
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    # Cache static assets
    elif path.startswith("/assets/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

    return response


app.title = "CFB 4th Down Decisions"

app.layout = html.Div(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        dcc.Store(id="screen-width-store"),
        dcc.Interval(id="resize-listener", interval=100000, n_intervals=1),
        header,
        dcc.Location(id="url"),
        html.Div(
            dash.page_container,
            style={"flex": "1"},  # This makes the content grow to fill space
        ),
        footer,
    ],
    id="app-shell",
    className="app-shell theme-light",
    style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"},
)

app.clientside_callback(
    """
    function(n_intervals) {
        return window.innerWidth;
    }
    """,
    Output("screen-width-store", "data"),
    Input("resize-listener", "n_intervals"),
)

app.clientside_callback(
    """
    function(theme) {
        const mode = theme === "dark" ? "dark" : "light";
        document.documentElement.setAttribute("data-bs-theme", mode);
        document.body.setAttribute("data-bs-theme", mode);
        return `app-shell theme-${mode}`;
    }
    """,
    Output("app-shell", "className"),
    Input("theme-store", "data"),
)


@app.callback(
    Output("theme-store", "data"),
    Input("theme-toggle-desktop", "n_clicks"),
    Input("theme-toggle-mobile", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(desktop_clicks, mobile_clicks, current_theme):
    if ctx.triggered_id not in {"theme-toggle-desktop", "theme-toggle-mobile"}:
        return no_update
    return "light" if current_theme == "dark" else "dark"


@app.callback(
    Output("theme-toggle-desktop", "children"),
    Output("theme-toggle-desktop", "className"),
    Output("theme-toggle-mobile", "children"),
    Output("theme-toggle-mobile", "className"),
    Input("theme-store", "data"),
)
def update_theme_button(theme):
    is_dark = theme == "dark"
    desktop_icon = html.I(
        id="theme-toggle-icon-desktop",
        className=f"bi {'bi-sun-fill' if is_dark else 'bi-moon-stars-fill'}",
    )
    mobile_icon = html.I(
        id="theme-toggle-icon-mobile",
        className=f"bi {'bi-sun-fill' if is_dark else 'bi-moon-stars-fill'}",
    )
    desktop_class_name = (
        "theme-toggle-btn theme-toggle-btn-dark d-none d-lg-inline-flex ms-lg-3"
    )
    mobile_class_name = "theme-toggle-btn theme-toggle-btn-dark d-inline-flex d-lg-none"
    if not is_dark:
        desktop_class_name = (
            "theme-toggle-btn theme-toggle-btn-light d-none d-lg-inline-flex ms-lg-3"
        )
        mobile_class_name = (
            "theme-toggle-btn theme-toggle-btn-light d-inline-flex d-lg-none"
        )
    return desktop_icon, desktop_class_name, mobile_icon, mobile_class_name


@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_navbar(n_clicks, is_open):
    if not n_clicks:
        return no_update
    return not is_open


if __name__ == "__main__":
    app.run(debug=False)
