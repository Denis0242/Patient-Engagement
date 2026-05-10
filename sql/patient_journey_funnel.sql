-- Patient journey funnel analysis
-- Purpose: calculate funnel volume and drop-off by stage.

WITH stage_counts AS (
    SELECT
        funnel_stage,
        funnel_stage_order,
        COUNT(DISTINCT patient_id) AS patients
    FROM patient_engagement
    GROUP BY funnel_stage, funnel_stage_order
),
funnel AS (
    SELECT
        funnel_stage,
        funnel_stage_order,
        patients,
        LAG(patients) OVER (ORDER BY funnel_stage_order) AS previous_stage_patients
    FROM stage_counts
)
SELECT
    funnel_stage,
    funnel_stage_order,
    patients,
    previous_stage_patients,
    CASE
        WHEN previous_stage_patients IS NULL THEN 0
        ELSE ROUND((previous_stage_patients - patients) * 100.0 / previous_stage_patients, 2)
    END AS drop_off_pct
FROM funnel
ORDER BY funnel_stage_order;
