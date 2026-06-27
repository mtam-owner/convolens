import pandas as pd
import plotly.express as px

from convolens.visualization.theme import (
    AXIS_STYLE,
    CHART_LAYOUT,
    PLOTLY_TEMPLATE,
    PRIMARY,
)


def _apply_chart_style(fig):
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def _active_operating_period(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.assign(date=df["start_time"].dt.date)
        .groupby("date")
        .size()
        .reset_index(name="conversations")
        .sort_values("date")
    )

    if daily.empty:
        return daily

    threshold = max(10, daily["conversations"].quantile(0.05))
    active_dates = daily[daily["conversations"] >= threshold]["date"]

    if active_dates.empty:
        return daily

    start_date = active_dates.min()
    end_date = active_dates.max()

    daily = daily[(daily["date"] >= start_date) & (daily["date"] <= end_date)]

    full_range = pd.date_range(
        start=pd.to_datetime(start_date),
        end=pd.to_datetime(end_date),
        freq="D",
    )

    return (
        daily.assign(date=pd.to_datetime(daily["date"]))
        .set_index("date")
        .reindex(full_range, fill_value=0)
        .rename_axis("date")
        .reset_index()
    )


def conversation_volume_trend(df: pd.DataFrame):
    daily = _active_operating_period(df)

    fig = px.line(
        daily,
        x="date",
        y="conversations",
        title="Daily conversation volume",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(line={"color": PRIMARY, "width": 2.2})
    return _apply_chart_style(fig)


def top_companies_chart(df: pd.DataFrame, top_n: int = 15):
    company_volume = (
        df.dropna(subset=["company"])
        .groupby("company")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="conversations")
    )

    fig = px.bar(
        company_volume,
        x="conversations",
        y="company",
        orientation="h",
        title="Top companies by conversation volume",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(marker={"color": PRIMARY})
    fig = _apply_chart_style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    return fig


def response_time_distribution(df: pd.DataFrame):
    response_df = df[df["response_time_minutes"].notna()].copy()
    response_df = response_df[response_df["response_time_minutes"].between(0, 1440)]

    fig = px.histogram(
        response_df,
        x="response_time_minutes",
        nbins=60,
        title="Response time distribution",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(marker={"color": PRIMARY})
    return _apply_chart_style(fig)


def conversation_length_distribution(df: pd.DataFrame):
    length_df = df[df["message_count"].between(1, 50)]

    fig = px.histogram(
        length_df,
        x="message_count",
        nbins=50,
        title="Conversation length distribution",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(marker={"color": PRIMARY})
    return _apply_chart_style(fig)

def risk_level_distribution(df: pd.DataFrame):
    risk_order = ["High", "Medium", "Low"]

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .reindex(risk_order)
        .fillna(0)
        .reset_index()
    )

    risk_counts.columns = ["risk_level", "conversations"]

    fig = px.bar(
        risk_counts,
        x="risk_level",
        y="conversations",
        title="Conversation risk distribution",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(marker={"color": PRIMARY})
    return _apply_chart_style(fig)

def top_high_risk_companies(df: pd.DataFrame, top_n: int = 15):
    risk_df = df[df["risk_level"] == "High"]

    company_risk = (
        risk_df.dropna(subset=["company"])
        .groupby("company")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="high_risk_conversations")
    )

    fig = px.bar(
        company_risk,
        x="high_risk_conversations",
        y="company",
        orientation="h",
        title="Top companies by high-risk conversations",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_traces(marker={"color": PRIMARY})
    fig = _apply_chart_style(fig)
    fig.update_yaxes(categoryorder="total ascending")
    return fig