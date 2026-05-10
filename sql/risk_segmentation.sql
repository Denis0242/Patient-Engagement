-- Patient risk segmentation
-- Purpose: summarize patients by risk category and engagement outcomes.

WITH patient_level AS (
    SELECT
        patient_id,
        patient_risk_category,
        MAX(engagement_score) AS engagement_score,
        MAX(treatment_completed) AS treatment_completed,
        MAX(d30_retained) AS d30_retained
    FROM patient_engagement
    GROUP BY patient_id, patient_risk_category
)
SELECT
    patient_risk_category,
    COUNT(*) AS patients,
    ROUND(AVG(engagement_score), 2) AS avg_engagement_score,
    ROUND(AVG(treatment_completed) * 100, 2) AS treatment_completion_rate,
    ROUND(AVG(d30_retained) * 100, 2) AS d30_retention_rate
FROM patient_level
GROUP BY patient_risk_category
ORDER BY patients DESC;
