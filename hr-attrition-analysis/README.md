# HR Employee Attrition Analysis

End-to-end HR analytics project: identifying why employees leave, predicting who's at risk, and translating both into business recommendations and a Power BI dashboard.

## Business Problem
A company is losing 16% of its workforce annually. HR needs to know **who is leaving, why, and who's likely to leave next** — so retention spend can be targeted instead of spread thin across everyone.

## Dataset
[IBM HR Analytics Employee Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — 1,470 employees, 35 features (demographics, compensation, satisfaction, performance, tenure). No missing values.

## Key Findings
| Driver | Finding |
|---|---|
| Overtime | 30.5% attrition vs. 10.4% for non-overtime — **~3x risk** |
| Job Role | Sales Representatives: 39.8% attrition, the highest of any role |
| Income | Lowest income quartile: 29.3% vs. 10.3% in the top quartile |
| Business Travel | Frequent travelers: 24.9% vs. 8.0% for non-travelers |
| Marital Status | Single employees: 25.5% vs. 12.5% for married employees |
| Tenure | Leavers average 5.1 years at the company vs. 7.4 for stayers |

## Approach
1. **Data Cleaning** — verified no nulls/duplicates, dropped constant/ID columns (`01_data_exploration.py`)
2. **EDA** — attrition rate broken down across 6+ business dimensions (`02_eda_attrition_drivers.py`)
3. **Visualization** — 8 charts covering distribution, drivers, and model output (`03_visualizations.py`)
4. **Predictive Model** — logistic regression (44 features, standardized, class-balanced) to rank drivers and score risk (`04_predictive_model.py`)
5. **Power BI Export** — every employee scored with an attrition risk probability and risk band (`05_powerbi_export.py`)
6. **Dashboard** — built from the export using the guide in `outputs/POWERBI_BUILD_GUIDE.md`

## Model Performance
- **Accuracy:** 77.7% | **ROC-AUC:** 0.81
- Correctly flags **64% of actual leavers** on held-out test data (vs. a 16% random baseline)
- Evaluated with a stratified 75/25 train-test split; metrics reported on test data only

## Top Statistical Drivers (Logistic Regression)
![Top Drivers](outputs/08_top_attrition_drivers.png)

## Repo Structure
```
hr_attrition_project/
├── data/
│   ├── HR_Employee_Attrition.csv          # raw dataset
│   └── HR_Employee_Attrition_clean.csv     # cleaned dataset
├── notebooks/
│   ├── 01_data_exploration.py
│   ├── 02_eda_attrition_drivers.py
│   ├── 03_visualizations.py
│   ├── 04_predictive_model.py
│   ├── 05_powerbi_export.py
│   └── generate_memo.js
├── outputs/
│   ├── 01-08_*.png                         # charts
│   ├── HR_Attrition_PowerBI_Ready.csv       # risk-scored, dashboard-ready
│   ├── HR_Attrition_Insight_Memo.docx       # business memo deliverable
│   ├── POWERBI_BUILD_GUIDE.md               # DAX measures + layout guide
│   ├── attrition_breakdown_summary.csv
│   └── model_top_drivers.csv
└── README.md
```

## Tools
Python (pandas, scikit-learn, matplotlib, seaborn) · Power BI · SQL-style groupby analysis

## Recommendations
1. Cap or compensate overtime in Sales and Lab Technician roles
2. Introduce structured 18–24 month promotion checkpoints
3. Prioritize retention spend using the model's risk score, not tenure alone
4. Re-examine frequent-travel role design for at-risk segments

---
*Author: Saptarshi Mandal — built as a portfolio project for Data/Business Analyst roles.*
