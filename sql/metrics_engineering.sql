-- Executive KPI layer
-- Purpose: create one dashboard-ready table for KPI monitoring.

WITH patient_level AS (
    SELECT
        patient_id,
        MAX(d1_retained) AS d1_retained,
        MAX(d7_retained) AS d7_retained,
        MAX(d30_retained) AS d30_retained,
        MAX(treatment_completed) AS treatment_completed,
        MAX(follow_up_completed) AS follow_up_completed,
        MAX(outcome_success) AS outcome_success,
        MAX(engagement_score) AS engagement_score,
        SUM(treatment_cost) AS treatment_cost
    FROM patient_engagement
    GROUP BY patient_id
)
SELECT
    COUNT(*) AS total_patients,
    ROUND(AVG(d1_retained) * 100, 2) AS d1_retention_rate,
    ROUND(AVG(d7_retained) * 100, 2) AS d7_retention_rate,
    ROUND(AVG(d30_retained) * 100, 2) AS d30_retention_rate,
    ROUND(AVG(CASE WHEN engagement_score >= 7 THEN 1 ELSE 0 END) * 100, 2) AS engagement_rate,
    ROUND(AVG(treatment_completed) * 100, 2) AS treatment_completion_rate,
    ROUND(AVG(follow_up_completed) * 100, 2) AS follow_up_completion_rate,
    ROUND(AVG(outcome_success) * 100, 2) AS outcome_success_rate,
    ROUND(SUM(treatment_cost), 2) AS total_treatment_cost
FROM patient_level;
