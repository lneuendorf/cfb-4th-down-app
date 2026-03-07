import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash import Input, Output
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

if __name__ == "__main__":
    app.run(debug=False)
