-- Patient Engagement & Outcomes Dashboard SQL
-- Representative queries designed to match the Tableau and Streamlit visuals.

-- 1. KPI Summary
SELECT
    COUNT(DISTINCT patient_id) AS total_patients,
    AVG(d1_retained) AS d1_retention,
    AVG(d7_retained) AS d7_retention,
    AVG(d30_retained) AS d30_retention,
    AVG(treatment_completed) AS treatment_completion_rate,
    AVG(outcome_success) AS outcome_success_rate,
    AVG(engagement_score) / 10.0 AS engagement_rate
FROM patient_engagement;

-- 2. Patient Journey Funnel
SELECT
    funnel_stage,
    funnel_stage_order,
    COUNT(DISTINCT patient_id) AS patients
FROM patient_engagement
GROUP BY funnel_stage, funnel_stage_order
ORDER BY funnel_stage_order;

-- 3. Weekly Retention Trend
SELECT
    DATE_TRUNC('week', journey_date) AS week_of_date,
    AVG(d1_retained) AS d1_retention,
    AVG(d7_retained) AS d7_retention,
    AVG(d30_retained) AS d30_retention
FROM patient_engagement
GROUP BY 1
ORDER BY 1;

-- 4. Cost and Outcome by Condition
SELECT
    condition,
    AVG(treatment_cost) AS avg_treatment_cost,
    AVG(treatment_completed) AS treatment_completion_rate,
    AVG(outcome_success) AS outcome_success_rate
FROM patient_engagement
WHERE treatment_cost > 0
GROUP BY condition
ORDER BY avg_treatment_cost DESC;

-- 5. Risk Segmentation
SELECT
    patient_risk_category,
    COUNT(DISTINCT patient_id) AS patients,
    AVG(d30_retained) AS d30_retention,
    AVG(treatment_completed) AS treatment_completion_rate
FROM patient_engagement
GROUP BY patient_risk_category
ORDER BY patients DESC;
