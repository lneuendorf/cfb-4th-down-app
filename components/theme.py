import html
import textwrap
import plotly.graph_objects as go


def apply_plotly_theme(fig, is_dark):
    template = "plotly_dark" if is_dark else "plotly_white"
    font_color = "#f4f7fb" if is_dark else "#252626"
    paper_bgcolor = "#161b22" if is_dark else "#ffffff"
    plot_bgcolor = "#161b22" if is_dark else "#ffffff"
    grid_color = "rgba(255,255,255,0.12)" if is_dark else "rgba(37,38,38,0.12)"
    zero_line_color = "rgba(255,255,255,0.2)" if is_dark else "rgba(37,38,38,0.2)"

    fig.update_layout(
        template=template,
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font=dict(color=font_color),
        hoverlabel=dict(font=dict(color=font_color)),
        title_font=dict(color=font_color),
    )
    fig.update_xaxes(
        gridcolor=grid_color,
        zerolinecolor=zero_line_color,
        linecolor=grid_color,
        tickfont=dict(color=font_color),
        title_font=dict(color=font_color),
    )
    fig.update_yaxes(
        gridcolor=grid_color,
        zerolinecolor=zero_line_color,
        linecolor=grid_color,
        tickfont=dict(color=font_color),
        title_font=dict(color=font_color),
    )

    return fig


def build_empty_state_figure(
    is_dark,
    message="Make selections to view data.",
    height=400,
):
    muted_color = "#b7c0cb" if is_dark else "#5f6368"

    fig = go.Figure()
    apply_plotly_theme(fig, is_dark)
    fig.update_layout(
        height=height,
        showlegend=False,
        hovermode=False,
        dragmode=False,
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=[
            dict(
                text=html.escape(message),
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="center",
                font=dict(size=15, color=muted_color),
            )
        ],
    )
    fig.update_xaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        fixedrange=True,
    )
    fig.update_yaxes(
        visible=False,
        showgrid=False,
        zeroline=False,
        fixedrange=True,
    )
    return fig


def _estimate_plot_width(screen_width, columns=1):
    viewport_width = max(screen_width or 1280, 320)
    horizontal_padding = 72 if viewport_width >= 768 else 28

    if columns == 2 and viewport_width >= 1200:
        return max((viewport_width - horizontal_padding) / 2, 320)

    return max(viewport_width - horizontal_padding, 320)


def _wrap_plot_text(text, max_chars):
    if not text:
        return ""

    wrapper = textwrap.TextWrapper(
        width=max(12, int(max_chars)),
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines = wrapper.wrap(text)
    return "<br>".join(html.escape(line) for line in lines)


def _count_wrapped_lines(wrapped_text):
    if not wrapped_text:
        return 0
    return wrapped_text.count("<br>") + 1


def _fit_single_line_font_size(
    text, plot_width, base_font_size, width_factor, min_font_size=None
):
    if not text:
        return base_font_size

    # Spaces render narrower than letters, so discount them slightly in the fit estimate.
    normalized_chars = sum(0.55 if char.isspace() else 1 for char in text)
    estimated_font_size = plot_width / max(normalized_chars * width_factor, 1)
    minimum_size = (
        min_font_size if min_font_size is not None else max(10, base_font_size * 0.68)
    )
    return round(min(base_font_size, max(minimum_size, estimated_font_size)), 1)


def build_responsive_plot_title(
    title,
    subtitle=None,
    screen_width=None,
    columns=1,
    title_font_size=16,
    subtitle_font_size=16,
    title_width_factor=0.5,
    subtitle_width_factor=0.52,
):
    plot_width = _estimate_plot_width(screen_width, columns=columns)
    fitted_title_font_size = _fit_single_line_font_size(
        title,
        plot_width,
        title_font_size,
        title_width_factor,
        min_font_size=max(12, title_font_size * 0.72),
    )
    escaped_title = html.escape(title)
    title_text = f"<span style='font-size:{fitted_title_font_size}px; white-space:nowrap; display:inline-block;'><b>{escaped_title}</b></span>"
    title_lines = 1

    if not subtitle:
        return {
            "text": title_text,
            "lines": title_lines,
        }

    fitted_subtitle_font_size = _fit_single_line_font_size(
        subtitle,
        plot_width,
        subtitle_font_size,
        subtitle_width_factor,
    )
    escaped_subtitle = html.escape(subtitle)
    return {
        "text": (
            f"{title_text}<br>"
            f"<span style='font-size:{fitted_subtitle_font_size}px; white-space:nowrap; display:inline-block;'><sub>{escaped_subtitle}</sub></span>"
        ),
        "lines": title_lines + 1,
    }


def get_plot_title_margin(title_lines, has_subtitle=False, base=72):
    extra_lines = max(title_lines - (2 if has_subtitle else 1), 0)
    per_line = 18 if has_subtitle else 20
    return base + (extra_lines * per_line)


def build_wrapped_bar_title(title, subtitle, compact):
    screen_width = 700 if compact else 1400
    subtitle_font_size = 14 if compact else 16
    return build_responsive_plot_title(
        title,
        subtitle=subtitle,
        screen_width=screen_width,
        columns=2,
        title_font_size=16,
        subtitle_font_size=subtitle_font_size,
    )


def wrap_trend_title(title, compact):
    screen_width = 700 if compact else 1400
    return build_responsive_plot_title(
        title,
        screen_width=screen_width,
        columns=1,
        title_font_size=16,
    )
