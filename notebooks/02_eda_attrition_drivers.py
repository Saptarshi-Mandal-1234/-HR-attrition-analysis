"""
HR Attrition Analysis - Step 2: EDA - What drives attrition?
"""
import pandas as pd

pd.set_option("display.width", 100)
df = pd.read_csv("../data/HR_Employee_Attrition_clean.csv")
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

def attrition_rate_by(col, sort=True):
    g = df.groupby(col)["AttritionFlag"].agg(["mean", "count"])
    g["mean"] = (g["mean"] * 100).round(1)
    g.columns = ["AttritionRate%", "HeadCount"]
    if sort:
        g = g.sort_values("AttritionRate%", ascending=False)
    return g

print("=" * 60)
print("ATTRITION RATE BY OVERTIME")
print("=" * 60)
print(attrition_rate_by("OverTime"))

print("\n" + "=" * 60)
print("ATTRITION RATE BY DEPARTMENT")
print("=" * 60)
print(attrition_rate_by("Department"))

print("\n" + "=" * 60)
print("ATTRITION RATE BY JOB ROLE")
print("=" * 60)
print(attrition_rate_by("JobRole"))

print("\n" + "=" * 60)
print("ATTRITION RATE BY JOB SATISFACTION (1=Low, 4=High)")
print("=" * 60)
print(attrition_rate_by("JobSatisfaction"))

print("\n" + "=" * 60)
print("ATTRITION RATE BY MARITAL STATUS")
print("=" * 60)
print(attrition_rate_by("MaritalStatus"))

print("\n" + "=" * 60)
print("ATTRITION RATE BY BUSINESS TRAVEL")
print("=" * 60)
print(attrition_rate_by("BusinessTravel"))

print("\n" + "=" * 60)
print("AVERAGE NUMERIC VALUES: STAYED vs LEFT")
print("=" * 60)
numeric_cols = ["Age", "MonthlyIncome", "DistanceFromHome", "TotalWorkingYears",
                 "YearsAtCompany", "YearsSinceLastPromotion", "NumCompaniesWorked",
                 "WorkLifeBalance", "EnvironmentSatisfaction"]
comparison = df.groupby("Attrition")[numeric_cols].mean().round(1).T
comparison.columns = ["Stayed (No)", "Left (Yes)"]
comparison["Gap"] = (comparison["Left (Yes)"] - comparison["Stayed (No)"]).round(1)
print(comparison)

print("\n" + "=" * 60)
print("ATTRITION RATE BY INCOME QUARTILE")
print("=" * 60)
df["IncomeQuartile"] = pd.qcut(df["MonthlyIncome"], 4, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4 (Highest)"])
print(attrition_rate_by("IncomeQuartile", sort=False))

# Save a summary table for the dashboard / report
summary_rows = []
for col in ["OverTime", "Department", "JobSatisfaction", "MaritalStatus", "BusinessTravel"]:
    t = attrition_rate_by(col)
    for idx, row in t.iterrows():
        summary_rows.append({"Dimension": col, "Segment": idx, "AttritionRate%": row["AttritionRate%"], "HeadCount": row["HeadCount"]})
pd.DataFrame(summary_rows).to_csv("../outputs/attrition_breakdown_summary.csv", index=False)
print("\nSaved breakdown summary to outputs/attrition_breakdown_summary.csv")
