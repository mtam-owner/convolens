from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from convolens.services.data_loader import load_analytics
from convolens.visualization.theme import AXIS_STYLE, CHART_LAYOUT, PLOTLY_TEMPLATE, PRIMARY


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
CSS_FILE = ASSET_DIR / "style.css"


def load_css() -> None:
    if CSS_FILE.exists():
        st.markdown(
            f"<style>{CSS_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


def apply_style(fig):
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def intent_trend(df: pd.DataFrame):
    chart_df = df.copy()

    chart_df["month"] = pd.to_datetime(chart_df["month"])
    chart_df = chart_df[chart_df["month"] >= "2017-07-01"]

    trend = (
        chart_df.groupby(["month", "intent"])
        .size()
        .reset_index(name="conversations")
        .sort_values("month")
    )

    fig = px.area(
        trend,
        x="month",
        y="conversations",
        color="intent",
        title="Monthly conversation mix by intent",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_xaxes(
        dtick="M3",
        tickformat="%b %Y",
    )

    return apply_style(fig)


def intent_distribution(df: pd.DataFrame):
    data = (
        df["intent"]
        .value_counts()
        .reset_index()
    )
    data.columns = ["intent", "conversations"]

    fig = px.treemap(
        data,
        path=["intent"],
        values="conversations",
        title="Intent share of support workload",
        template=PLOTLY_TEMPLATE,
    )

    fig.update_layout(**CHART_LAYOUT)
    return fig


def company_intent_heatmap(df: pd.DataFrame):
    top_companies = (
        df["company"]
        .value_counts()
        .head(15)
        .index
    )

    heatmap_df = df[df["company"].isin(top_companies)]

    matrix = (
        heatmap_df.groupby(["company", "intent"])
        .size()
        .reset_index(name="conversations")
    )

    fig = px.density_heatmap(
        matrix,
        x="intent",
        y="company",
        z="conversations",
        title="Company and intent concentration",
        template=PLOTLY_TEMPLATE,
        color_continuous_scale="Blues",
    )

    return apply_style(fig)


def risk_by_intent(df: pd.DataFrame):
    data = (
        df.groupby("intent")
        .agg(
            conversations=("conversation_id", "count"),
            avg_escalation=("escalation_score", "mean"),
            high_risk_rate=("risk_level", lambda x: (x == "High").mean() * 100),
        )
        .reset_index()
        .sort_values("high_risk_rate", ascending=False)
    )

    fig = px.scatter(
        data,
        x="conversations",
        y="high_risk_rate",
        size="avg_escalation",
        color="intent",
        hover_name="intent",
        title="Intent risk profile",
        template=PLOTLY_TEMPLATE,
    )

    return apply_style(fig)


def emerging_intents(df: pd.DataFrame):
    months = sorted(df["month"].dropna().unique())

    if len(months) < 2:
        return pd.DataFrame()

    previous_month = months[-2]
    current_month = months[-1]

    current = (
        df[df["month"] == current_month]
        .groupby("intent")
        .size()
        .reset_index(name="current")
    )

    previous = (
        df[df["month"] == previous_month]
        .groupby("intent")
        .size()
        .reset_index(name="previous")
    )

    merged = current.merge(previous, on="intent", how="outer").fillna(0)

    merged["change"] = merged["current"] - merged["previous"]
    merged["change_pct"] = merged.apply(
        lambda row: (row["change"] / row["previous"] * 100)
        if row["previous"] > 0
        else 0,
        axis=1,
    )

    return merged.sort_values("change", ascending=False)


st.set_page_config(
    page_title="Conversation Intelligence",
    layout="wide",
)

load_css()

st.title("Conversation Intelligence")
st.markdown(
    '<div class="section-caption">Intent patterns, risk concentration and emerging customer support issues</div>',
    unsafe_allow_html=True,
)

analytics = load_analytics()

with st.sidebar:
    st.header("Filters")

    company_options = sorted(analytics["company"].dropna().unique().tolist())
    intent_options = sorted(analytics["intent"].dropna().unique().tolist())

    selected_companies = st.multiselect(
        "Company",
        options=company_options,
        default=[],
    )

    selected_intents = st.multiselect(
        "Intent",
        options=intent_options,
        default=[],
    )

filtered = analytics.copy()

if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

if selected_intents:
    filtered = filtered[filtered["intent"].isin(selected_intents)]

st.subheader("Intelligence Overview")

total_intents = filtered["intent"].nunique()
dominant_intent = (
    filtered["intent"].value_counts().idxmax()
    if not filtered.empty
    else "N/A"
)
high_risk_rate = (filtered["risk_level"] == "High").mean() * 100
avg_escalation = filtered["escalation_score"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Detected Intents", f"{total_intents:,}")
col2.metric("Dominant Intent", dominant_intent)
col3.metric("High Risk Rate", f"{high_risk_rate:.1f}%")
col4.metric("Average Escalation", f"{avg_escalation:.3f}")

st.divider()

st.subheader("Intent Trends")
st.plotly_chart(intent_trend(filtered), use_container_width=True)

st.divider()

st.subheader("Intent Composition and Concentration")

left, right = st.columns(2)

with left:
    st.plotly_chart(intent_distribution(filtered), use_container_width=True)

with right:
    st.plotly_chart(company_intent_heatmap(filtered), use_container_width=True)

st.divider()

st.subheader("Risk by Intent")
st.plotly_chart(risk_by_intent(filtered), use_container_width=True)

st.divider()

st.subheader("Emerging Issues")

emerging = emerging_intents(filtered)

if emerging.empty:
    st.info("Not enough monthly data available for emerging issue comparison.")
else:
    emerging_display = emerging.head(10).copy()
    emerging_display["change_pct"] = emerging_display["change_pct"].round(1)

    emerging_display.columns = [
        "Intent",
        "Latest Month",
        "Previous Month",
        "Change",
        "Change %",
    ]

    st.dataframe(
        emerging_display,
        use_container_width=True,
        hide_index=True,
    )