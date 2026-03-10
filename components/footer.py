from dash import html

footer = html.Footer(
    className="footer text-center app-footer",
    children=[
        html.Div(
            [
                html.A(
                    html.Img(
                        src="/assets/logos/substack.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://substack.com/@lukeneuendorf",
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/logos/bluesky.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://bsky.app/profile/lukeneuendorf.bsky.social",
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/logos/x.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://x.com/lukeneuendorf",
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/logos/github.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://github.com/lneuendorf",
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/logos/linkedin.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://www.linkedin.com/in/luke-neuendorf/",
                    target="_blank",
                ),
            ],
            style={"marginBottom": "18px", "marginTop": "20px"},
        ),
        html.P("Built with Dash & Plotly", style={"marginTop": "10px"}),
    ],
    style={
        "width": "100%",
        "boxShadow": "0 -1px 5px rgba(0,0,0,0.1)",
    },
)
