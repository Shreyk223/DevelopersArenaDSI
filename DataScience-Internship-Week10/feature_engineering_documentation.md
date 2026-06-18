# Feature Engineering Documentation — Customer Churn Prediction

This document defines every engineered feature created in
`churn_prediction_pipeline.ipynb` (Day 5): the exact formula, the business/statistical
rationale, and a worked example using customer `C00001` (`Tenure=6`,
`MonthlyCharges=64`, `TotalCharges=1540`, `Contract='One year'`,
`PaperlessBilling='No'`, `SeniorCitizen=1`).

---

## 1. Customer Lifetime Value (`CustomerLifetimeValue`)

**Formula:**
```
CustomerLifetimeValue = Tenure × MonthlyCharges
```

**Rationale:** approximates the total revenue a customer represents if billed at
their current monthly rate for their full tenure so far. It combines two raw signals
(how long someone has stayed, how much they pay) into a single magnitude that
correlates strongly and negatively with churn — customers with low lifetime value
(short tenure and/or low monthly rate) churn more often, as confirmed in the Day 5
boxplot comparison.

**Worked example (C00001):** `6 × 64 = 384`.

---

## 2. Average Monthly Spend (`AvgMonthlySpend`)

**Formula:**
```
AvgMonthlySpend = TotalCharges / Tenure   (Tenure replaced with 1 if Tenure == 0, to avoid division by zero)
```

**Rationale:** `TotalCharges` is the actual cumulative amount billed, which can
differ from `Tenure × MonthlyCharges` because of promotions, plan changes, or
prorated billing in real-world data. Dividing back out by tenure recovers the
customer's *true* historic average monthly bill, which turned out to be the single
strongest predictor of churn in the feature-selection step (Day 6).

**Worked example (C00001):** `1540 / 6 ≈ 256.67`.

---

## 3. Payment Efficiency Ratio (`PaymentEfficiency`)

**Formula:**
```
PaymentEfficiency = TotalCharges / CustomerLifetimeValue   (CustomerLifetimeValue replaced with 1 if it is 0)
```

**Rationale:** compares actual billing (`TotalCharges`) to the simple expectation of
"current rate × tenure" (`CustomerLifetimeValue`). A ratio close to 1 means billing
has been consistent with the customer's current rate for their whole tenure; a ratio
far from 1 flags a customer whose historical billing diverges from their current
plan (e.g. they recently changed plans, or have had irregular billing) — both
plausible churn risk signals.

**Worked example (C00001):** `1540 / 384 ≈ 4.01` — this customer's historical
average bill is much higher than their *current* `MonthlyCharges`, suggesting they
downgraded plans at some point.

---

## 4. Tenure Group (`TenureGroup` → one-hot `TenureGroup_New` / `TenureGroup_Established` / `TenureGroup_Loyal`)

**Formula:**
```
TenureGroup = "New"          if 0  < Tenure <= 12
            = "Established"  if 12 < Tenure <= 36
            = "Loyal"        if 36 < Tenure <= 100
```
(then one-hot encoded into three binary columns)

**Rationale:** churn risk is rarely linear across a customer's lifecycle — it is
common in subscription businesses for risk to be concentrated in the first year and
then taper off. Bucketing `Tenure` into lifecycle stages lets a model learn a
different baseline risk per stage directly, rather than relying on a single linear
coefficient on raw tenure.

**Worked example (C00001):** `Tenure=6` → `"New"` → `TenureGroup_New=1`,
`TenureGroup_Established=0`, `TenureGroup_Loyal=0`.

---

## 5. High Spender Flag (`HighSpenderFlag`)

**Formula:**
```
HighSpenderFlag = 1 if MonthlyCharges > 75th_percentile(MonthlyCharges), else 0
```
(the 75th percentile, ≈158, is computed once on the training data and reused —
never recomputed per row — so the threshold is stable when scoring new customers)

**Rationale:** a simple, interpretable binary flag isolating the top quartile of
payers. High-paying customers may be more price-sensitive to alternatives, so this
flag lets the model treat "premium" customers as a distinct group rather than just
a high value on a continuous scale.

**Worked example (C00001):** `MonthlyCharges=64 ≤ 158` → `HighSpenderFlag = 0`.

---

## 6. Contract Risk Score (`ContractRiskScore`)

**Formula:**
```
ContractRiskScore = (2 - Contract_Ordinal) × 1.0
                   + PaperlessBilling_Bin × 0.5
                   + SeniorCitizen × 0.5
```
where `Contract_Ordinal` is 0 (Month-to-month), 1 (One year), or 2 (Two year).

**Rationale:** a single composite score that blends three separate churn-risk
signals identified during exploration: shorter contracts carry the most weight
(the `(2 - Contract_Ordinal)` term gives Month-to-month customers a base score of 2,
One-year customers 1, Two-year customers 0), with paperless billing and senior
citizen status each adding a smaller `0.5` nudge. The weights were chosen
heuristically based on the relative strength of each signal observed during
exploration, not fit by an optimization process — this is documented as a
limitation, and the score is still validated against the target (Day 6) before being
trusted, where it ranked ahead of several raw columns in both correlation and
Random Forest importance.

**Worked example (C00001):** `Contract='One year' → Contract_Ordinal=1`,
`PaperlessBilling='No' → 0`, `SeniorCitizen=1`.
`ContractRiskScore = (2 - 1) × 1.0 + 0 × 0.5 + 1 × 0.5 = 1.5`.

---

## Summary Table

Ranks below are out of the 12 candidate features compared in `preprocessing_report.md`
Section 8 (1 = strongest), verified directly from the notebook's Day 6 output —
not estimated.

| Feature | Type | Range (this dataset, verified) | Correlation rank | RF importance rank |
|---|---|---|---|---|
| `CustomerLifetimeValue` | Continuous | 30 – 13,124 | 3rd | 3rd |
| `AvgMonthlySpend` | Continuous | 3.11 – 7,217.0 | 2nd | 2nd |
| `PaymentEfficiency` | Continuous ratio | 0.02 – 208.07 | 4th | 5th |
| `TenureGroup` (one-hot ×3) | Categorical | New / Established / Loyal | not in candidate list — evaluated qualitatively via the Day 5 boxplot, not numerically ranked | — |
| `HighSpenderFlag` | Binary | 0 / 1 | 9th | 10th |
| `ContractRiskScore` | Continuous score | 0.0 – 3.0 | 6th | 7th |

For reference, the two strongest signals overall were the *raw* `Tenure` column
(rank 1 on both metrics) and the engineered `AvgMonthlySpend` (rank 2 on both) — see
`preprocessing_report.md` Section 8 for the full 12-feature ranking and how the
production pipeline (Step 7) uses these results.

**Caveat on the wide `AvgMonthlySpend` / `PaymentEfficiency` ranges:** these two
ratio features can take extreme values for short-tenure customers. Checking
`TotalCharges` against `Tenure × MonthlyCharges` directly shows almost no
correlation between them (Pearson r ≈ -0.04), meaning `TotalCharges` in this
dataset was not generated as a strict function of tenure and rate. For a customer
with `Tenure = 1` and a comparatively large `TotalCharges`, dividing by a tenure of
1 produces a very large ratio (the maximum `AvgMonthlySpend` of 7,217 belongs to
exactly this case). This is flagged in `preprocessing_report.md` Section 11 as a
limitation: outlier capping (Day 4) was applied to the three *raw* numeric columns
before these ratios were derived, not to the derived ratios themselves, so a future
iteration of this pipeline should also cap or log-transform `AvgMonthlySpend` and
`PaymentEfficiency` directly.
