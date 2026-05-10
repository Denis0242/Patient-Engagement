-- Cost by condition
-- Purpose: identify conditions contributing the highest treatment cost.

SELECT
    condition,
    ROUND(SUM(treatment_cost), 2) AS total_treatment_cost,
    COUNT(DISTINCT patient_id) AS total_patients,
    ROUND(SUM(treatment_cost) / NULLIF(COUNT(DISTINCT patient_id), 0), 2) AS cost_per_patient
FROM patient_engagement
GROUP BY condition
ORDER BY total_treatment_cost DESC;
