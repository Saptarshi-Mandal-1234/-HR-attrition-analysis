# Reproduce the HR analysis

Install Python and `python -m pip install pandas numpy scikit-learn matplotlib seaborn`.

From `hr-attrition-analysis/notebooks`, run the numbered scripts 01 through 05 in order. Relative input/output paths assume that working directory. Original screenshots are in `hr-attrition-analysis/dashboard`; source data is in `hr-attrition-analysis/data`.

The existing model uses a stratified 75/25 split, training-only scaling and class-balanced logistic regression. Treat feature associations as descriptive, not causal, and do not use these scores for employment decisions. The Power BI screenshot may have an active department filter; its totals need not match the full dataset.
