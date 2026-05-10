-- Retention analysis
-- Purpose: calculate patient-level D1, D7, and D30 retention.

WITH patient_level AS (
    SELECT
        patient_id,
        MAX(d1_retained) AS d1_retained,
        MAX(d7_retained) AS d7_retained,
        MAX(d30_retained) AS d30_retained,
        MAX(treatment_completed) AS treatment_completed
    FROM patient_engagement
    GROUP BY patient_id
)
SELECT
    COUNT(*) AS total_patients,
    ROUND(AVG(d1_retained) * 100, 2) AS d1_retention_rate,
    ROUND(AVG(d7_retained) * 100, 2) AS d7_retention_rate,
    ROUND(AVG(d30_retained) * 100, 2) AS d30_retention_rate,
    ROUND(AVG(treatment_completed) * 100, 2) AS treatment_completion_rate
FROM patient_level;
