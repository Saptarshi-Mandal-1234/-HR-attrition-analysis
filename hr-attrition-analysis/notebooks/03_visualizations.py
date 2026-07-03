"""
HR Attrition Analysis - Step 3: Visualizations
Generates publication-ready charts for dashboard/README use.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE_LEAVE = "#E15759"
PALETTE_STAY = "#4E79A7"

df = pd.read_csv("../data/HR_Employee_Attrition_clean.csv")
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

OUT = "../outputs"

# ---------- Chart 1: Overall attrition rate ----------
fig, ax = plt.subplots(figsize=(5, 5))
counts = df["Attrition"].value_counts()
colors = [PALETTE_STAY, PALETTE_LEAVE]
ax.pie(counts, labels=[f"Stayed\n{counts['No']} ({counts['No']/len(df)*100:.1f}%)",
                        f"Left\n{counts['Yes']} ({counts['Yes']/len(df)*100:.1f}%)"],
       colors=colors, startangle=90, wedgeprops=dict(width=0.4), textprops={'fontsize': 11})
ax.set_title("Overall Employee Attrition (n=1,470)", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/01_overall_attrition.png", dpi=150)
plt.close()

# ---------- Chart 2: Attrition by OverTime ----------
fig, ax = plt.subplots(figsize=(6, 4.5))
rate = df.groupby("OverTime")["AttritionFlag"].mean().mul(100).sort_values(ascending=False)
bars = ax.bar(rate.index, rate.values, color=[PALETTE_LEAVE, PALETTE_STAY])
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Overtime Status", fontsize=13, fontweight="bold")
for bar, val in zip(bars, rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/02_attrition_by_overtime.png", dpi=150)
plt.close()

# ---------- Chart 3: Attrition by Job Role ----------
fig, ax = plt.subplots(figsize=(8, 5.5))
rate = df.groupby("JobRole")["AttritionFlag"].mean().mul(100).sort_values(ascending=True)
colors_bar = [PALETTE_LEAVE if v > rate.mean() else PALETTE_STAY for v in rate.values]
ax.barh(rate.index, rate.values, color=colors_bar)
ax.set_xlabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Job Role", fontsize=13, fontweight="bold")
for i, val in enumerate(rate.values):
    ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUT}/03_attrition_by_jobrole.png", dpi=150)
plt.close()

# ---------- Chart 4: Attrition by Marital Status ----------
fig, ax = plt.subplots(figsize=(6, 4.5))
rate = df.groupby("MaritalStatus")["AttritionFlag"].mean().mul(100).sort_values(ascending=False)
bars = ax.bar(rate.index, rate.values, color=sns.color_palette("Reds_r", len(rate)))
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Marital Status", fontsize=13, fontweight="bold")
for bar, val in zip(bars, rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/04_attrition_by_marital_status.png", dpi=150)
plt.close()

# ---------- Chart 5: Attrition by Income Quartile ----------
fig, ax = plt.subplots(figsize=(6.5, 4.5))
df["IncomeQuartile"] = pd.qcut(df["MonthlyIncome"], 4, labels=["Q1\n(Lowest)", "Q2", "Q3", "Q4\n(Highest)"])
rate = df.groupby("IncomeQuartile")["AttritionFlag"].mean().mul(100)
bars = ax.bar(rate.index.astype(str), rate.values, color=sns.color_palette("Blues_r", 4))
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Monthly Income Quartile", fontsize=13, fontweight="bold")
for bar, val in zip(bars, rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/05_attrition_by_income_quartile.png", dpi=150)
plt.close()

# ---------- Chart 6: Attrition by Business Travel ----------
fig, ax = plt.subplots(figsize=(6, 4.5))
rate = df.groupby("BusinessTravel")["AttritionFlag"].mean().mul(100).sort_values(ascending=False)
bars = ax.bar(rate.index, rate.values, color=sns.color_palette("Oranges_r", 3))
ax.set_ylabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Business Travel Frequency", fontsize=13, fontweight="bold")
plt.xticks(rotation=15)
for bar, val in zip(bars, rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/06_attrition_by_business_travel.png", dpi=150)
plt.close()

# ---------- Chart 7: Age distribution stayed vs left ----------
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.kdeplot(data=df, x="Age", hue="Attrition", fill=True, alpha=0.4,
            palette={"No": PALETTE_STAY, "Yes": PALETTE_LEAVE}, ax=ax)
ax.set_title("Age Distribution: Stayed vs Left", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/07_age_distribution.png", dpi=150)
plt.close()

print("All 7 charts generated successfully in outputs/")
import os
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        size_kb = os.path.getsize(f"{OUT}/{f}") / 1024
        print(f"  {f} ({size_kb:.0f} KB)")
