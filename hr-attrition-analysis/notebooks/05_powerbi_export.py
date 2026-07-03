"""
HR Attrition Analysis - Step 5: Power BI Export
Scores every employee with attrition risk probability and exports
a clean, dashboard-ready file (original readable columns + risk score).
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("../data/HR_Employee_Attrition_clean.csv")
y = (df["Attrition"] == "Yes").astype(int)
X = df.drop(columns=["Attrition"])

cat_cols = X.select_dtypes(include="object").columns.tolist()
X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

# Train on FULL data for the final scoring model (separate from the
# train/test evaluation done in Step 4, which proved the model generalizes)
model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
model.fit(X_scaled, y)
risk_scores = model.predict_proba(X_scaled)[:, 1]

# Build the Power BI export: human-readable columns + risk fields
export = df.copy()
export["AttritionRiskScore"] = (risk_scores * 100).round(1)

def risk_band(score):
    if score >= 50:
        return "High"
    elif score >= 25:
        return "Medium"
    else:
        return "Low"

export["RiskBand"] = export["AttritionRiskScore"].apply(risk_band)
export["EmployeeID"] = range(1, len(export) + 1)

# Reorder: put ID and risk fields first
cols = ["EmployeeID", "Attrition", "AttritionRiskScore", "RiskBand"] + \
       [c for c in export.columns if c not in ["EmployeeID", "Attrition", "AttritionRiskScore", "RiskBand"]]
export = export[cols]

export.to_csv("../outputs/HR_Attrition_PowerBI_Ready.csv", index=False)

print("Export complete: outputs/HR_Attrition_PowerBI_Ready.csv")
print(f"Rows: {len(export)} | Columns: {len(export.columns)}")
print("\nRisk band distribution:")
print(export["RiskBand"].value_counts())
print("\nSanity check - average risk score by actual attrition outcome:")
print(export.groupby("Attrition")["AttritionRiskScore"].mean().round(1))
print("\n(Leavers should score meaningfully higher than stayers - confirms model is sane)")

print("\nFirst 3 rows preview:")
print(export[["EmployeeID", "Attrition", "AttritionRiskScore", "RiskBand", "Department", "JobRole", "OverTime"]].head(3).to_string(index=False))
