import datetime
from dash import html

footer = html.Footer(
    className="footer text-center app-footer",
    children=[
        html.Div(
            [
                html.A(
                    html.Img(
                        src="/assets/logos/x_v2.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://x.com/CFB4thDown",
                    target="_blank",
                ),
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
                        src="/assets/logos/github.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://github.com/lneuendorf",
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/logos/linkedin_v2.png",
                        className="social-icon social-icon-invertable",
                        style={"height": "24px", "margin": "0 10px"},
                    ),
                    href="https://www.linkedin.com/in/luke-neuendorf/",
                    target="_blank",
                ),
            ],
            style={"marginBottom": "18px", "marginTop": "20px"},
        ),
        # html.P(
        #     [
        #         "Data: ",
        #         html.A(
        #             "CollegeFootballData",
        #             href="https://collegefootballdata.com/",
        #             target="_blank",
        #             style={
        #                 "textDecoration": "none",
        #                 "fontStyle": "italic",
        #             },
        #         ),
        #         " using ",
        #         html.A(
        #             "cfbd-python",
        #             href="https://github.com/CFBD/cfbd-python",
        #             target="_blank",
        #             style={
        #                 "textDecoration": "none",
        #                 "fontStyle": "italic",
        #             },
        #         ),
        #     ],
        #     style={"marginTop": "10px"},
        # ),
        # © 2026 Elite Drafters. All rights reserved.
        html.P(
            f"© {datetime.datetime.now().year} CFB4thDown. All rights reserved.",
            style={"marginTop": "10px"},
        ),
    ],
    style={
        "width": "100%",
        "boxShadow": "0 -1px 5px rgba(0,0,0,0.1)",
    },
)
