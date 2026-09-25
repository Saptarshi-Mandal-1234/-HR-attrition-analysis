"""
HR Attrition Analysis - Step 1: Data Exploration & Cleaning
Dataset: IBM HR Analytics Employee Attrition (1470 employees, 35 features)
"""
import pandas as pd

# Load data
df = pd.read_csv("../data/HR_Employee_Attrition.csv")

print("=" * 60)
print("SHAPE:", df.shape)
print("=" * 60)

print("\nMissing values per column:")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().sum() > 0 else "No missing values found.")

print("\nDuplicate rows:", df.duplicated().sum())

print("\nAttrition value counts:")
print(df["Attrition"].value_counts())
print("\nOverall attrition rate: {:.2f}%".format(
    (df["Attrition"] == "Yes").mean() * 100
))

# Columns that are useless for analysis (constant or ID-like)
useless_cols = []
for col in df.columns:
    if df[col].nunique() == 1:
        useless_cols.append(col)
print("\nConstant columns (no analytical value):", useless_cols)
print("Example values:", {c: df[c].unique()[0] for c in useless_cols})

# Drop useless columns for cleaned dataset
drop_cols = useless_cols + ["EmployeeNumber"]
df_clean = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Save cleaned version
df_clean.to_csv("../data/HR_Employee_Attrition_clean.csv", index=False)
print(f"\nCleaned dataset saved: {df_clean.shape[1]} columns (dropped {len(drop_cols)})")
