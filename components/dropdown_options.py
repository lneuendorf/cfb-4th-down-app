from dash import html


def build_dropdown_option(label, value=None):
    option_value = label if value is None else value
    option_text = "" if label is None else str(label)

    return {
        "label": html.Span(option_text, style={"color": "#252626"}),
        "value": option_value,
        "search": option_text,
    }
