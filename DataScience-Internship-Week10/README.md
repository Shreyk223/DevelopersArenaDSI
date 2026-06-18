# Customer Churn Prediction — Preprocessing & Feature Engineering

A complete, documented data preprocessing and feature engineering
pipeline that turns raw customer records into a churn prediction, built end-to-end in
`churn_prediction_pipeline.ipynb`.

## Project Overview

**Goal:** preprocess a 500-row customer dataset, engineer features that capture churn
risk, and train a baseline classifier that predicts which customers are likely to
leave (`Churn = 1`) versus stay (`Churn = 0`).

**What's implemented:**
- 4 categorical encoding methods (binary mapping, ordinal mapping, label encoding,
  one-hot encoding) — exceeds the 3-method requirement
- 2 feature scaling methods (Min-Max, Standardization), compared side by side
- Outlier detection via both IQR and Z-score methods, with a capping strategy
  documented and ready even though none were found in this dataset
- 6 new engineered features (`CustomerLifetimeValue`, `AvgMonthlySpend`,
  `PaymentEfficiency`, `TenureGroup`, `HighSpenderFlag`, `ContractRiskScore`)
- Feature selection via correlation analysis + Random Forest importance
- One reusable `sklearn.Pipeline` that takes raw rows in and returns predictions,
  validated with 3 explicit tests, reaching 96% accuracy / 0.998 ROC-AUC on a
  held-out test set

The notebook itself is organized into the same 7 days as the assignment brief, each
with a markdown header, the relevant code, and a short discussion of the result
directly underneath it.

## Technical Details

**Algorithms/structures used:**
- `LabelEncoder`, `OneHotEncoder`, plus two manual mapping dictionaries for encoding
- `MinMaxScaler` and `StandardScaler` for scaling
- IQR (`Q3 - Q1` fence) and Z-score (`|z| > 3`) for outlier detection
- `ColumnTransformer` to apply different preprocessing per column type inside one
  object, wrapped in an `sklearn.Pipeline` together with the final estimator
- `RandomForestClassifier` (`n_estimators=200`, `class_weight='balanced'`) as the
  classifier — chosen because it handles a mix of scaled numeric and one-hot
  categorical columns natively, gives interpretable feature importances for free
  , and is robust to the modest class imbalance once
  `class_weight='balanced'` is set
- `engineer_features()` is a plain function (not a custom sklearn transformer) so
  that both the notebook and a future script can call it directly on raw rows

See `preprocessing_report.md` for the rationale behind every choice above, and
`feature_engineering_documentation.md` for the exact formula behind each new feature.

## Visual Documentation

All charts below are generated live inside the notebook and saved to `visuals/` —
they are the actual output of running the pipeline, not mockups.

**Churn class distribution** — confirms the 89%/11% imbalance that shapes
every evaluation decision later in the project.

**Scaling comparison** — `MonthlyCharges` shown original, Min-Max scaled, and
Standard scaled side by side; the distribution shape is identical, only the axis
scale changes.

**Outlier boxplots** — visual confirmation that `Tenure`, `MonthlyCharges`,
and `TotalCharges` have no points beyond the IQR whiskers in this dataset.

**Engineered features by churn** — `CustomerLifetimeValue` and
`ContractRiskScore` plotted by churn status, showing the separation that makes them
useful predictors.

**Correlation & feature importance** — two bar charts ranking all 12
candidate features by linear correlation and by Random Forest importance.

**Confusion matrix** — the final model's test-set predictions broken down
into true/false positives and negatives.

## Testing Evidence

This part of the notebook includes three explicit, assertion-backed tests, run after the
pipeline is fit:

1. **Held-out raw samples** — 5 untouched rows are run through the full pipeline
   (encoding + feature engineering + scaling + prediction) and compared against
   their true `Churn` label.
2. **Brand-new hypothetical customer** — a hand-built single-row `DataFrame` with no
   pre-existing features is passed straight into the pipeline; an `assert` confirms
   the output is a valid binary prediction.
3. **No-NaN / shape check** — after the `ColumnTransformer` step, an `assert`
   confirms there are zero NaNs in the transformed matrix and that its row count
   matches the input.

All three pass in the executed notebook (see the "Testing Evidence" section, Day 7).
Standard classification metrics (accuracy, precision, recall, F1, ROC-AUC) and a
confusion matrix are also reported on a stratified 80/20 train/test split.
