import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash import Input, Output

from components.navbar import navbar
from components.footer import footer

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.ZEPHYR],  
)

server = app.server

app.title = "CFB 4th Down Decisions"

app.layout = html.Div([
    dcc.Store(id='screen-width-store'),
    dcc.Interval(id='resize-listener', interval=100000, n_intervals=1),
    navbar,
    dcc.Location(id="url"),
    html.Div(
        dash.page_container,
        style={"flex": "1"}  # This makes the content grow to fill space
    ),
    footer
], style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"})

app.clientside_callback(
    """
    function(n_intervals) {
        return window.innerWidth;
    }
    """,
    Output('screen-width-store', 'data'),
    Input('resize-listener', 'n_intervals')
)

if __name__ == "__main__":
    app.run(debug=False)