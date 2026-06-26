PLOTLY_TEMPLATE = "plotly_white"

PRIMARY = "#234A6B"
PRIMARY_MUTED = "#6F8FAE"
GRID = "#e1e5eb"
TEXT = "#111827"
MUTED_TEXT = "#5f6b7a"
PAPER = "#ffffff"
PLOT = "#ffffff"

CHART_LAYOUT = {
    "paper_bgcolor": PAPER,
    "plot_bgcolor": PLOT,
    "font": {"color": TEXT, "size": 12},
    "title": {
        "font": {"color": TEXT, "size": 15},
        "x": 0,
        "xanchor": "left",
    },
    "margin": {"l": 45, "r": 25, "t": 45, "b": 45},
    "showlegend": False,
}

AXIS_STYLE = {
    "showline": False,
    "showgrid": True,
    "gridcolor": GRID,
    "zeroline": False,
    "ticks": "",
    "color": MUTED_TEXT,
}