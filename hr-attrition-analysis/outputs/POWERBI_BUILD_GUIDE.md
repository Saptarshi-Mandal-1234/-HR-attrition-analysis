# Power BI Dashboard Build Guide — HR Attrition Analysis

## 1. Import the data
1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Select `HR_Attrition_PowerBI_Ready.csv`
3. Click **Load** (not Transform — the data is already clean)

## 2. DAX Measures to create
Go to **Home → New Measure** and add each of these:

```
Total Employees = COUNTROWS('HR_Attrition_PowerBI_Ready')

Total Leavers = CALCULATE([Total Employees], 'HR_Attrition_PowerBI_Ready'[Attrition] = "Yes")

Attrition Rate % = DIVIDE([Total Leavers], [Total Employees], 0)

Avg Monthly Income = AVERAGE('HR_Attrition_PowerBI_Ready'[MonthlyIncome])

Avg Risk Score = AVERAGE('HR_Attrition_PowerBI_Ready'[AttritionRiskScore])

High Risk Employees = CALCULATE([Total Employees], 'HR_Attrition_PowerBI_Ready'[RiskBand] = "High")

Avg Tenure (Years) = AVERAGE('HR_Attrition_PowerBI_Ready'[YearsAtCompany])

Overtime Attrition Rate =
CALCULATE([Attrition Rate %], 'HR_Attrition_PowerBI_Ready'[OverTime] = "Yes")
```

## 3. Dashboard Layout (2 pages)

### Page 1: Executive Overview
| Visual | Fields | Position |
|---|---|---|
| Card | `Total Employees` | Top-left |
| Card | `Attrition Rate %` | Top-left (next to above) |
| Card | `High Risk Employees` | Top-left |
| Card | `Avg Monthly Income` | Top-left |
| Donut chart | Attrition (Yes/No) count | Top-right |
| Bar chart | Attrition Rate % by `Department` | Middle-left |
| Bar chart | Attrition Rate % by `JobRole` (sort descending) | Middle-right |
| Stacked bar | `RiskBand` count by `Department` | Bottom |
| Slicers | `Department`, `Gender`, `OverTime`, `BusinessTravel` | Left rail |

### Page 2: Risk Drill-Down
| Visual | Fields | Position |
|---|---|---|
| Table | EmployeeID, Department, JobRole, MonthlyIncome, AttritionRiskScore, RiskBand — filtered to RiskBand = "High" | Full width top |
| Scatter chart | X = `YearsAtCompany`, Y = `AttritionRiskScore`, color = `Attrition` | Bottom-left |
| Bar chart | Attrition Rate % by `MaritalStatus` | Bottom-right |
| KPI | `Overtime Attrition Rate` vs overall `Attrition Rate %` | Bottom-right small |

## 4. Formatting tips (for a clean, professional look)
- Theme: View → Themes → pick a neutral corporate theme (e.g. "Executive")
- Color rule: Red (#E15759) = high risk / left, Blue (#4E79A7) = retained / safe — matches the charts already generated in `outputs/`
- Add a title text box at the top: "Employee Attrition Risk Dashboard — [Your Name]"
- Use **tooltips** on the JobRole bar chart to show headcount alongside rate

## 5. Publish & share
- File → Publish to Power BI Service (free account works)
- Or: File → Export → PDF for a static version to attach to your resume/LinkedIn post
- Get the **Publish to Web** link (if using Power BI Service) to embed in your LinkedIn Featured section

---
**Why this matters for interviews:** Be ready to explain the "High Risk Employees" card and the model behind it (Step 4: logistic regression, 77.7% accuracy, ROC-AUC 0.81). Interviewers will probe how the risk score was derived — knowing this cold is what separates a real project from a copy-pasted dashboard.
