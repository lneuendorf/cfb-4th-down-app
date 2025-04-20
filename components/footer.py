from dash import html

footer = html.Footer(
    className="footer text-center",
    children=[
        html.Hr(style={"margin": "20px 0 10px 0", "borderTop": "1px solid #eee"}),
        html.Div([
            html.A(
                html.Img(
                    src="/assets/logos/bluesky.png",
                    style={"height": "24px", "margin": "0 10px"}
                ),
                href="https://bsky.app/profile/lukeneuendorf.bsky.social",
                target="_blank"
            ),
            html.A(
                html.Img(
                    src="/assets/logos/x.png",
                    style={"height": "24px", "margin": "0 10px"}
                ),
                href="https://x.com/luke_neuendorf",
                target="_blank"
            ),
            html.A(
                html.Img(
                    src="/assets/logos/github.png",
                    style={"height": "24px", "margin": "0 10px"}
                ),
                href="https://github.com/lneuendorf",
                target="_blank"
            ),
        ], style={"marginBottom": "10px"}),
        html.P(
            "Built with Dash & Plotly",
            style={"paddingBottom": "20px", "marginTop": "10px"}
        )
    ],
    style={
        "backgroundColor": "white",
        "color": "#333",
        "width": "100%",
        "marginTop": "20px", 
        "boxShadow": "0 -1px 5px rgba(0,0,0,0.1)"
    }
)