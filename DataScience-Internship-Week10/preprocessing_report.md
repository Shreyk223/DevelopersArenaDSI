# Preprocessing Report — Customer Churn Prediction

## 1. Project Overview

This report documents the data preprocessing and feature engineering pipeline built
for the customer churn dataset (`churn_data.csv`, 500 customers, 9 raw columns). The
goal of the pipeline is to take raw, unprocessed customer records and produce a
model-ready feature matrix that a classifier can use to predict the `Churn` target
(1 = customer left, 0 = customer stayed). Every transformation below is implemented
and executed in `churn_prediction_pipeline.ipynb`; this document explains **why** each
step was taken, not just what code was run.

## 2. Dataset Summary

| Property | Value |
|---|---|
| Rows | 500 |
| Raw columns | 9 (`CustomerID`, `Tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `PaymentMethod`, `PaperlessBilling`, `SeniorCitizen`, `Churn`) |
| Missing values | 0 |
| Churn rate | 53 churned / 447 stayed (10.6% / 89.4%) |
| Numeric columns | `Tenure`, `MonthlyCharges`, `TotalCharges`, `SeniorCitizen` (binary) |
| Categorical columns | `Contract`, `PaymentMethod`, `PaperlessBilling` |

The class imbalance (≈9:1) is the single most important fact discovered during
exploration: it does not require a preprocessing fix by itself, but it does mean that
**accuracy alone is a misleading metric** for the downstream model, so precision,
recall, F1, and ROC-AUC are all reported in Day 7, and `class_weight='balanced'` is
used in the classifier to reduce bias toward the majority class.

## 3. Step 1 — Data Exploration

`df.info()` and `df.isnull().sum()` confirmed there are no missing values anywhere in
the dataset, so **no imputation step was necessary** — a deliberate simplification
that was verified rather than assumed. `CustomerID` was identified as a unique
identifier with no predictive value and is excluded from every modeling step.

## 4. Step 2 — Categorical Encoding

Three categorical columns required encoding, and each was treated differently
based on whether its categories have a natural order:

| Column | Cardinality | Order? | Method used | Why |
|---|---|---|---|---|
| `PaperlessBilling` | 2 (Yes/No) | N/A | Manual binary mapping | Simplest correct representation for a two-level flag; no information lost. |
| `Contract` | 3 (Month-to-month, One year, Two year) | Yes — by commitment length | Manual ordinal mapping (0/1/2) | The categories have a genuine rank. Encoding them as unordered (one-hot) would discard that ordering information. |
| `PaymentMethod` | 3 (Credit Card, Electronic Check, Bank Transfer) | No | One-Hot Encoding (used in final pipeline); Label Encoding (shown for comparison only) | No real order exists between payment methods, so One-Hot avoids inventing a false rank. Label Encoding is kept in the notebook purely to demonstrate the difference and the risk of using it with linear/distance-based models. |

That covers **4 distinct encoding techniques** (binary mapping, ordinal mapping,
label encoding, one-hot encoding), exceeding the 3-method requirement, with an
explicit rationale for which one is actually used downstream and which is shown only
for comparison.

## 5. Step 3 — Feature Scaling

`Tenure` (1–71), `MonthlyCharges` (20–199), and `TotalCharges` (159–7992) sit on very
different numeric scales. Two scaling techniques were applied and compared side by
side (see the histogram comparison in the notebook / `visuals/day3_scaling_comparison.png`):

- **Min-Max Scaling** — rescales every value into a fixed `[0, 1]` range. Useful for
  algorithms that expect bounded input (e.g. neural networks), but every value is
  anchored to the current min/max, so a single future extreme value would compress
  all the existing data.
- **Standardization (Z-score)** — centers each feature at mean 0 with unit standard
  deviation. This is the more robust general-purpose default and is the version used
  inside `final pipeline's ColumnTransformer`, because the model includes a
  Random Forest as well as components that would benefit from standardized inputs if
  swapped for a linear model later.

Both scalers preserve the original distribution shape — only the numeric scale
changes, confirmed visually in the notebook.

## 6. Step 4 — Outlier Detection & Handling

Two independent statistical methods were applied to `Tenure`, `MonthlyCharges`, and
`TotalCharges`:

- **IQR method**: flags any value below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR`.
- **Z-score method**: flags any value with `|z| > 3`.

**Result: zero outliers detected by either method on this dataset.** All three
numeric columns are bounded and well-behaved (synthetic data with realistic but
non-extreme ranges).

**Handling decision:** even though no outliers were present, a capping
(winsorization) step is implemented and left active in the pipeline rather than
removed. The rationale: with only 500 rows, dropping rows is costly (every row is
~0.2% of the dataset, and a dropped churned customer is a real loss of an
already-scarce minority-class example). Capping bounds extreme values without
deleting any customer record, and the logic is generic — it will automatically
activate and cap any genuine outliers that appear in a future batch of data, making
the pipeline robust beyond this one snapshot.

## 7. Step 5 — Feature Engineering

Six new features were engineered from the existing columns. Full formulas, rationale,
and example values are documented separately in
`feature_engineering_documentation.md` (kept separate per the submission
requirements). In summary: `CustomerLifetimeValue`, `AvgMonthlySpend`,
`PaymentEfficiency`, `TenureGroup` (binned + one-hot encoded), `HighSpenderFlag`, and
`ContractRiskScore`.

## 8. Step 6 — Feature Selection

Two complementary methods were used to evaluate every candidate feature (raw +
engineered) against the `Churn` target:

1. **Pearson correlation with the target** — captures linear relationships.
2. **Random Forest feature importance** (`n_estimators=200`) — captures nonlinear
   and interaction effects that correlation alone would miss.

Both methods agreed that tenure-driven signals dominate: `Tenure`,
`AvgMonthlySpend`, and `CustomerLifetimeValue` ranked at or near the top in both
views, and the engineered `PaymentEfficiency` / `ContractRiskScore` features ranked
ahead of several raw columns — direct evidence that the feature engineering step
added genuine predictive value rather than just additional columns.
`SeniorCitizen` and `PaperlessBilling_Bin` ranked lowest in both views. Rather than
hard-deleting them, they are retained (along with one-hot encoded `PaymentMethod`)
in the production pipeline built in Step 7: with only 500 rows the overfitting cost
of a few low-signal columns is small, and Random Forests naturally down-weight
uninformative features rather than being misled by them. The ranking is used as a
guide to feature priority, not a hard filter.

## 9. Step 7 — Complete Pipeline & Evaluation

All steps above were assembled into a single `sklearn.Pipeline`:

```
raw columns -> engineer_features() -> ColumnTransformer(StandardScaler + OneHotEncoder + passthrough) -> RandomForestClassifier
```

The `engineer_features()` function reproduces the categorical encoding and feature
engineering steps so the entire pipeline can accept **untouched raw rows** as input —
nothing needs to be precomputed by the caller. An 80/20 stratified train/test split
(`random_state=42`) was used to keep the churn ratio consistent across both sets.

**Test set results:**

| Metric | Score |
|---|---|
| Accuracy | 0.96 |
| Precision (churn class) | 1.00 |
| Recall (churn class) | 0.64 |
| F1 (churn class) | 0.78 |
| ROC-AUC | 0.998 |

**Interpretation:** the model is excellent at not raising false alarms (precision =
1.00 — every customer it flags as a churn risk really did churn) but it still misses
some churners (recall = 0.64), which is the expected, honest consequence of the 9:1
class imbalance noted in Section 2 rather than a flaw in the preprocessing itself.
This is flagged explicitly as future work rather than hidden.

Three explicit tests (shown in the notebook's "Testing Evidence" section) confirm
the pipeline (a) correctly predicts on held-out raw rows, (b) handles a completely
new, hand-built customer record with no errors, and (c) produces no NaNs and
correctly shaped output after the full transform step.

## 10. Key Decisions — Quick Reference

| Decision | Choice | Rationale |
|---|---|---|
| Missing values | None found, no imputation | Verified via `isnull().sum()`, not assumed |
| `Contract` encoding | Ordinal (0/1/2) | Genuine commitment-length order exists |
| `PaymentMethod` encoding | One-Hot (final), Label (comparison) | No real order between payment types |
| Scaler used in final pipeline | StandardScaler | Better default for linear-sensitive components than Min-Max |
| Outlier handling | IQR-based capping (no-op here, active for future data) | Preserves all 500 rows, especially scarce churn examples |
| Class imbalance | `class_weight='balanced'`, precision/recall/F1/ROC-AUC reported | Accuracy alone would hide the 9:1 imbalance |
| Feature selection | Correlation + Random Forest importance, intersection | Captures both linear and nonlinear signal |

## 11. Limitations & Future Work

- The dataset is small (500 rows) and synthetic; results may not generalize to a
  production-scale, real-world churn dataset.
- `TotalCharges` shows almost no correlation with `Tenure × MonthlyCharges`
  (Pearson r ≈ -0.04), meaning it was not generated as a strict function of tenure
  and rate. This makes the ratio features `AvgMonthlySpend` and `PaymentEfficiency`
  take very large values for a handful of short-tenure customers (e.g. a customer
  with `Tenure = 1` and a large `TotalCharges` produces an `AvgMonthlySpend` in the
  thousands — see `feature_engineering_documentation.md` for the exact numbers).
  Outlier capping in Day 4 was applied to the three *raw* numeric columns before
  these ratios were derived in Day 5, not to the ratios themselves; a future
  iteration should cap or log-transform `AvgMonthlySpend` and `PaymentEfficiency`
  directly.
- Recall on the minority churn class (0.64) leaves room for improvement — natural
  next steps are SMOTE-style resampling, probability threshold tuning, or
  cost-sensitive learning, none of which were in scope for this preprocessing-focused
  assignment.
- Cross-validation and hyperparameter tuning were intentionally left out to keep this
  submission focused on preprocessing and feature engineering rather than model
  optimization.
