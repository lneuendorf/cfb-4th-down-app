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


def build_wrapped_bar_title(title, subtitle, compact):
    if not compact:
        return (
            f"<span style='font-size:16px'><b>{title}</b></span><br>"
            f"<span style='font-size:16px'><sub>{subtitle}</sub></span>"
        )

    # compact_title = title.replace(" Rate When ", " Rate<br>When ")
    # compact_subtitle = subtitle.replace(" on 4th down ", " on 4th down<br>")
    # compact_subtitle = compact_subtitle.replace(
    #     " highest expected win probability",
    #     "highest expected win probability",
    # )
    return (
        f"<span style='font-size:16px'><b>{title}</b></span><br>"
        f"<span style='font-size:14px'><sub>{compact_subtitle}</sub></span>"
    )


def wrap_trend_title(title, compact):
    if not compact:
        return title

    wrapped = title.replace(
        " When Recommended Over Time", " When Recommended<br>Over Time"
    )
    wrapped = wrapped.replace(
        " Win Probability Lost Over Time", " Win Probability Lost<br>Over Time"
    )
    return wrapped
