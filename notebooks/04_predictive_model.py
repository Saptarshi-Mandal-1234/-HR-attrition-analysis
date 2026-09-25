"""
HR Attrition Analysis - Step 4: Predictive Model
Logistic Regression to rank attrition drivers + predict risk.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix,
                               roc_auc_score, accuracy_score)
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data/HR_Employee_Attrition_clean.csv")
y = (df["Attrition"] == "Yes").astype(int)
X = df.drop(columns=["Attrition"])

# One-hot encode categoricals
cat_cols = X.select_dtypes(include="object").columns.tolist()
X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)

print(f"Features after encoding: {X_encoded.shape[1]}")
print(f"Class balance -> No: {(y==0).sum()} ({(y==0).mean()*100:.1f}%) | "
      f"Yes: {(y==1).sum()} ({(y==1).mean()*100:.1f}%)")

# Train/test split (stratified because of class imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.25, random_state=42, stratify=y
)

# Scale features (needed for fair coefficient comparison)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic regression with class_weight='balanced' (since only 16% attrition)
model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n" + "=" * 60)
print("MODEL PERFORMANCE (on held-out test set, n={})".format(len(y_test)))
print("=" * 60)
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, y_proba):.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Stayed", "Left"]))

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(f"                 Predicted Stay  Predicted Leave")
print(f"Actual Stay      {cm[0][0]:>14}  {cm[0][1]:>15}")
print(f"Actual Leave     {cm[1][0]:>14}  {cm[1][1]:>15}")

leavers_caught = cm[1][1] / (cm[1][0] + cm[1][1]) * 100
print(f"\n-> Model correctly flags {leavers_caught:.0f}% of employees who actually left")
print(f"   (vs. {y.mean()*100:.0f}% baseline if we randomly guessed)")

# ---------- Feature importance (odds ratios) ----------
coefs = pd.DataFrame({
    "Feature": X_encoded.columns,
    "Coefficient": model.coef_[0]
})
coefs["OddsRatio"] = np.exp(coefs["Coefficient"])
coefs["AbsImpact"] = coefs["Coefficient"].abs()
top_drivers = coefs.sort_values("AbsImpact", ascending=False).head(15)

print("\n" + "=" * 60)
print("TOP 15 ATTRITION DRIVERS (by standardized coefficient)")
print("=" * 60)
print("(Positive = increases attrition risk | Negative = decreases risk)\n")
print(top_drivers[["Feature", "Coefficient", "OddsRatio"]].to_string(index=False))

# Save chart
fig, ax = plt.subplots(figsize=(8, 6))
top_drivers_sorted = top_drivers.sort_values("Coefficient")
colors = ["#E15759" if c > 0 else "#4E79A7" for c in top_drivers_sorted["Coefficient"]]
ax.barh(top_drivers_sorted["Feature"], top_drivers_sorted["Coefficient"], color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Standardized Coefficient (impact on attrition log-odds)")
ax.set_title("Top 15 Attrition Drivers — Logistic Regression", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("../outputs/08_top_attrition_drivers.png", dpi=150)
plt.close()

# Save model results for report
top_drivers.to_csv("../outputs/model_top_drivers.csv", index=False)
print("\nSaved feature importance chart and CSV to outputs/")
