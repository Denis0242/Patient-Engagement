# EDA, Cleaning & Feature Engineering

## 1. Load Data
Loaded `patient_engagement.csv` with **2,619 rows** and **21 columns**.

## 2. Dataset Overview
The dataset is patient journey event-level data covering portal engagement, appointment views, bookings, consultation, treatment completion, follow-up, and outcome success.

## 3. Missing Values
Recommended checks:

```python
df.isna().sum().sort_values(ascending=False)
```

Business rule: missing condition, visit type, device type, or patient risk values should be labeled `Unknown` rather than deleted immediately.

## 4. Duplicates
Recommended checks:

```python
df.duplicated().sum()
df.drop_duplicates(inplace=True)
```

## 5. Datatype Cleaning
- Convert `Journey Date` to datetime.
- Convert retention and treatment flags to numeric/binary fields.
- Confirm `Treatment Cost` and `Engagement Score` are numeric.

## 6. Column Cleaning
Standardize column names into snake_case for SQL and Python workflows.

## 7. Text Cleaning
Trim whitespace, standardize category casing, and validate categories for `Condition`, `Region`, `Device Type`, `Visit Type`, and `Patient Risk Category`.

## 8. Outlier Detection
Key outlier checks:

- Treatment cost below 0
- Engagement score outside 0–10
- Funnel stage order outside expected journey sequence

## 9. Range Validation
Retention, treatment completion, follow-up completion, and outcome success fields should be binary.

## 10. KPI Validation
Validated KPI logic:

- D1 Retention: 63.33%
- D7 Retention: 40.11%
- D30 Retention: 23.44%
- Engagement Rate: 43.67%
- Treatment Completion Rate: 27.00%
- Outcome Success Rate: 25.11%

## 11. Feature Engineering
Suggested features:

```text
patient_completed_journey
patient_retention_band
cost_band
high_cost_flag
low_engagement_flag
care_gap_flag
decision_signal
```

## 12. Business Logic Validation
- Portal open count should be the widest funnel stage.
- Treatment cost should mainly appear for completed treatment events.
- D30 retention should not exceed D1 retention under normal retention logic.

## 13. Summary Statistics
Use descriptive statistics to check distribution of engagement score and treatment cost.

## 14. Final Clean Dataset Export

```python
df.to_csv("data/patient_engagement_clean.csv", index=False)
```

## 15. Insight Summary
Patient retention weakens from D1 to D30, suggesting the main business opportunity is long-term engagement after the initial interaction. Treatment-stage drop-off should be prioritized before investing heavily in new patient acquisition.
