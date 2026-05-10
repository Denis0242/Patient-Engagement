import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Patient Engagement & Outcomes", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "patient_engagement.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Journey Date"])
    return df

df = load_data()

st.title("Patient Engagement & Outcomes Dashboard")
st.caption("Healthcare product analytics view for retention, engagement, treatment completion, risk, and cost.")

with st.sidebar:
    st.header("Filters")
    region = st.multiselect("Region", sorted(df["Region"].dropna().unique()))
    condition = st.multiselect("Condition", sorted(df["Condition"].dropna().unique()))
    device = st.multiselect("Device Type", sorted(df["Device Type"].dropna().unique()))
    visit_type = st.multiselect("Visit Type", sorted(df["Visit Type"].dropna().unique()))

filtered = df.copy()
if region:
    filtered = filtered[filtered["Region"].isin(region)]
if condition:
    filtered = filtered[filtered["Condition"].isin(condition)]
if device:
    filtered = filtered[filtered["Device Type"].isin(device)]
if visit_type:
    filtered = filtered[filtered["Visit Type"].isin(visit_type)]

patient_level = filtered.groupby("Patient ID").agg(
    d1_retained=("D1 Retained", "max"),
    d7_retained=("D7 Retained", "max"),
    d30_retained=("D30 Retained", "max"),
    treatment_completed=("Treatment Completed", "max"),
    follow_up_completed=("Follow-up Completed", "max"),
    outcome_success=("Outcome Success", "max"),
    engagement_score=("Engagement Score", "max"),
    treatment_cost=("Treatment Cost", "sum"),
).reset_index()

cols = st.columns(6)
cols[0].metric("Total Patients", f"{patient_level['Patient ID'].nunique():,}")
cols[1].metric("D1 Retention", f"{patient_level['d1_retained'].mean():.2%}")
cols[2].metric("D7 Retention", f"{patient_level['d7_retained'].mean():.2%}")
cols[3].metric("D30 Retention", f"{patient_level['d30_retained'].mean():.2%}")
cols[4].metric("Engagement Rate", f"{(patient_level['engagement_score'] >= 7).mean():.2%}")
cols[5].metric("Treatment Completion", f"{patient_level['treatment_completed'].mean():.2%}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Patient Journey Funnel")
    funnel = (
        filtered.groupby(["Funnel Stage", "Funnel Stage Order"])["Patient ID"]
        .nunique()
        .reset_index(name="Patients")
        .sort_values("Funnel Stage Order")
    )
    st.bar_chart(funnel.set_index("Funnel Stage")["Patients"])

with right:
    st.subheader("Cost by Condition")
    cost = filtered.groupby("Condition")["Treatment Cost"].sum().sort_values(ascending=False)
    st.bar_chart(cost)

left, right = st.columns(2)

with left:
    st.subheader("Retention Trend by Week")
    weekly = (
        filtered.assign(week=filtered["Journey Date"].dt.to_period("W").dt.start_time)
        .groupby("week")[["D1 Retained", "D7 Retained", "D30 Retained"]]
        .mean()
    )
    st.line_chart(weekly)

with right:
    st.subheader("Patient Risk Segmentation")
    risk = filtered.groupby("Patient Risk Category")["Patient ID"].nunique().sort_values(ascending=False)
    st.bar_chart(risk)

st.subheader("Insight → Action → Recommendation → Decision")
st.markdown(
    """
**Insight:** Patient drop-off is concentrated around treatment and follow-up stages, while D30 retention is lower than early retention.  
**Action:** Analyze barriers preventing patients from completing treatment and re-engaging after initial visits.  
**Recommendation:** Implement targeted reminders and care navigation for high-risk and low-engagement patients.  
**Decision:** Prioritize reducing treatment-stage drop-off and improving D30 retention before scaling acquisition.
"""
)

st.subheader("Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)
