import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from components.navbar import navbar
from components.footer import footer
import components.callbacks  # Registers the callbacks

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "CFB 4th Down Decisions"

app.layout = html.Div([
    navbar,
    dcc.Location(id="url"),
    dash.page_container,  # This will render the content of the registered pages
    footer
])

if __name__ == "__main__":
    app.run(debug=False)
