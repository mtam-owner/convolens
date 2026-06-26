import streamlit as st


def kpi_card(label: str, value: str, note: str | None = None) -> None:
    note_html = f'<div class="kpi-note">{note}</div>' if note else ""

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )