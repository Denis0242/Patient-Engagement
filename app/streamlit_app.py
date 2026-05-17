import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Patient Engagement & Outcomes Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    app_dir = Path(__file__).resolve().parent
    data_path = app_dir.parent / "data" / "patient_engagement.csv"
    df = pd.read_csv(data_path)
    df.columns = [c.strip() for c in df.columns]
    df["Journey Date"] = pd.to_datetime(df["Journey Date"], errors="coerce")
    return df

df = load_data()

BLUE = "#3f73ad"
LIGHT_BLUE = "#dff0ff"
MID_BLUE = "#8ec1e4"
DARK_BLUE = "#27507d"

st.markdown("""
<style>
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 1rem;
}

.main-title {
    text-align:center;
    color:#2f66a3;
    font-size:34px;
    font-weight:800;
    margin-top:10px;
    margin-bottom:2px;
    line-height:1.2;
}

.subtitle {
    text-align:center;
    color:#5d6d7e;
    font-size:15px;
    margin-top:0;
    margin-bottom:20px;
}

.kpi-card {
    background:#ffffff;
    border:1px solid #e5edf5;
    border-radius:14px;
    padding:16px 12px;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
    min-height:112px;
}

.kpi-label {
    color:#3f73ad;
    font-size:18px;
    font-weight:600;
    line-height:1.15;
}

.kpi-value {
    color:#111111;
    font-size:28px;
    font-weight:800;
    margin-top:10px;
}

.section-title {
    color:#2f66a3;
    font-size:22px;
    font-weight:700;
    margin-top:14px;
    margin-bottom:8px;
    text-align:center;
}

.summary-card {
    border-radius:14px;
    padding:18px;
    min-height:150px;
    border:1px solid #e6e6e6;
}

.summary-title {
    font-weight:800;
    font-size:17px;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">Patient Engagement & Outcomes Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Healthcare Product Analytics | Funnel, Retention, Cost, Risk & Treatment Completion</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Dashboard Filters")

    age = st.multiselect("Age Group", sorted(df["Age Group"].dropna().unique()))
    condition = st.multiselect("Condition", sorted(df["Condition"].dropna().unique()))
    device = st.multiselect("Device", sorted(df["Device Type"].dropna().unique()))
    region = st.multiselect("Region", sorted(df["Region"].dropna().unique()))
    visit = st.multiselect("Visit Type", sorted(df["Visit Type"].dropna().unique()))

    date_min, date_max = df["Journey Date"].min().date(), df["Journey Date"].max().date()
    date_range = st.date_input(
        "Date",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )

filtered = df.copy()

if age:
    filtered = filtered[filtered["Age Group"].isin(age)]
if condition:
    filtered = filtered[filtered["Condition"].isin(condition)]
if device:
    filtered = filtered[filtered["Device Type"].isin(device)]
if region:
    filtered = filtered[filtered["Region"].isin(region)]
if visit:
    filtered = filtered[filtered["Visit Type"].isin(visit)]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[
        (filtered["Journey Date"] >= start) &
        (filtered["Journey Date"] <= end)
    ]

patient_level = filtered.groupby("Patient ID", as_index=False).agg({
    "D1 Retained": "max",
    "D7 Retained": "max",
    "D30 Retained": "max",
    "Treatment Completed": "max",
    "Outcome Success": "max",
    "Engagement Score": "max",
    "Treatment Cost": "sum"
})

def pct(x):
    return f"{x:.2%}"

total_patients = patient_level["Patient ID"].nunique()
d1 = patient_level["D1 Retained"].mean() if len(patient_level) else 0
d7 = patient_level["D7 Retained"].mean() if len(patient_level) else 0
d30 = patient_level["D30 Retained"].mean() if len(patient_level) else 0
engagement = patient_level["Engagement Score"].mean() / 10 if len(patient_level) else 0
completion = patient_level["Treatment Completed"].mean() if len(patient_level) else 0

kpis = [
    ("Total Patients", f"{total_patients:,}"),
    ("D1 Retention", pct(d1)),
    ("D7 Retention", pct(d7)),
    ("D30 Retention", pct(d30)),
    ("Engagement Rate", pct(engagement)),
    ("Treatment Completion Rate", pct(completion)),
]

cols = st.columns(6)
for col, (label, value) in zip(cols, kpis):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

left, mid, right = st.columns([1.15, 1.25, 1])

with left:
    st.markdown('<div class="section-title">Patient Journey Funnel</div>', unsafe_allow_html=True)

    funnel = (
        filtered.groupby(["Funnel Stage", "Funnel Stage Order"], as_index=False)["Patient ID"]
        .nunique()
        .sort_values("Funnel Stage Order")
    )

    fig = go.Figure(
        go.Funnel(
            y=funnel["Funnel Stage"],
            x=funnel["Patient ID"],
            textinfo="value",
            textposition="inside",
            marker={
                "color": ["#5f93c2", "#74a8cd", "#8fbcdc", "#b2d6ec", "#d7ecf7"]
            }
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

with mid:
    st.markdown('<div class="section-title">Patient Retention Trend</div>', unsafe_allow_html=True)

    trend = (
        filtered.set_index("Journey Date")
        .resample("W")
        .agg({
            "D1 Retained": "mean",
            "D7 Retained": "mean",
            "D30 Retained": "mean"
        })
        .reset_index()
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["Journey Date"],
        y=trend["D1 Retained"],
        mode="lines",
        name="D1 Retention",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=trend["Journey Date"],
        y=trend["D7 Retained"],
        mode="lines",
        name="D7 Retention",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=trend["Journey Date"],
        y=trend["D30 Retained"],
        mode="lines",
        name="D30 Retention",
        line=dict(width=3, color="red")
    ))

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_tickformat=".0%",
        legend=dict(
            orientation="h",
            y=1.12,
            x=0.05,
            font=dict(size=11)
        ),
        xaxis_title="Week of Date",
        yaxis_title="",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Cost by Condition</div>', unsafe_allow_html=True)

    cost = (
        filtered[filtered["Treatment Cost"] > 0]
        .groupby("Condition", as_index=False)["Treatment Cost"]
        .mean()
        .sort_values("Treatment Cost")
    )

    fig = px.bar(
        cost,
        x="Treatment Cost",
        y="Condition",
        orientation="h"
    )

    fig.update_traces(
        marker_color="#74a8cd",
        text=None,
        hovertemplate="<b>%{y}</b><br>Avg Cost: $%{x:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

left, mid, right = st.columns([1.1, 1.0, 1.1])

with left:
    st.markdown('<div class="section-title">Patients Drop-off Analysis</div>', unsafe_allow_html=True)

    f = funnel.sort_values("Funnel Stage Order").copy()
    f["Drop-off Rate"] = 1 - (f["Patient ID"].shift(-1) / f["Patient ID"])
    drop = f.dropna(subset=["Drop-off Rate"])

    fig = px.bar(
        drop,
        x="Funnel Stage",
        y="Drop-off Rate",
        text=drop["Drop-off Rate"].map(lambda v: f"{v:.2%}")
    )

    fig.update_traces(
        marker_color="#74a8cd",
        textposition="outside"
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_tickformat=".0%",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

with mid:
    st.markdown('<div class="section-title">Patient Risk Segmentation</div>', unsafe_allow_html=True)

    risk = (
        filtered.groupby("Patient Risk Category", as_index=False)["Patient ID"]
        .nunique()
        .sort_values("Patient ID", ascending=False)
    )

    fig = px.pie(
        risk,
        names="Patient Risk Category",
        values="Patient ID",
        hole=0.58
    )

    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=11,
        marker=dict(line=dict(color="white", width=2))
    )

    fig.update_layout(
        height=300,
        margin=dict(l=45, r=45, t=10, b=10),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            dict(
                text=f"Total Patients<br>{total_patients:,}",
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Engagement Distribution</div>', unsafe_allow_html=True)

    fig = px.histogram(
        patient_level,
        x="Engagement Score",
        nbins=10,
        text_auto=True
    )

    fig.update_traces(marker_color="#74a8cd")

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Engagement Score",
        yaxis_title="Patients",
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("## Executive Decision Summary")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    """
    <div class="summary-card" style="background:#dff0ff">
        <div class="summary-title">INSIGHT</div>
        Patient drop-off is highest between consultation and treatment, while D30 retention remains low, indicating weak long-term engagement.
    </div>
    """,
    unsafe_allow_html=True
)

c2.markdown(
    """
    <div class="summary-card" style="background:#fff4cc">
        <div class="summary-title">ACTION</div>
        Analyze barriers preventing patients from completing treatment and re-engaging after initial visits.
    </div>
    """,
    unsafe_allow_html=True
)

c3.markdown(
    """
    <div class="summary-card" style="background:#dcf7df">
        <div class="summary-title">RECOMMENDATION</div>
        Implement targeted follow-ups and digital reminders to improve treatment completion and long-term retention.
    </div>
    """,
    unsafe_allow_html=True
)

c4.markdown(
    """
    <div class="summary-card" style="background:#ffe1e8">
        <div class="summary-title">DECISION</div>
        Prioritize reducing treatment-stage drop-off and improving D30 retention before scaling patient acquisition.
    </div>
    """,
    unsafe_allow_html=True
)