import html
import textwrap


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
    title_chars = plot_width / max(title_font_size * title_width_factor, 1)
    subtitle_chars = plot_width / max(subtitle_font_size * subtitle_width_factor, 1)
    wrapped_title = _wrap_plot_text(title, title_chars)
    title_lines = _count_wrapped_lines(wrapped_title)

    if not subtitle:
        return {
            "text": f"<span style='font-size:{title_font_size}px'><b>{wrapped_title}</b></span>",
            "lines": title_lines,
        }

    wrapped_subtitle = _wrap_plot_text(subtitle, subtitle_chars)
    subtitle_lines = _count_wrapped_lines(wrapped_subtitle)
    return {
        "text": (
            f"<span style='font-size:{title_font_size}px'><b>{wrapped_title}</b></span><br>"
            f"<span style='font-size:{subtitle_font_size}px'><sub>{wrapped_subtitle}</sub></span>"
        ),
        "lines": title_lines + subtitle_lines,
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
