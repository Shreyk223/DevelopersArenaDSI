# Customer Churn Prediction
### Week 12 Capstone — End-to-End Machine Learning Project

A complete data science project predicting which telecom customers will cancel their subscription,
enabling the retention team to intervene before revenue is lost.

---

## Business Problem

Customer churn costs the telecom industry billions annually. Acquiring a new customer costs
5–7× more than retaining an existing one. This project builds a machine learning model that
scores every customer by churn probability, so the retention team focuses effort where it matters.

**Goal:** Predict whether a customer will churn (binary classification) with high precision on
the minority (churn) class, and surface actionable business insights.

---

## Results at a Glance

| Metric | Value |
|--------|-------|
| Best Model | Random Forest (200 trees) |
| Cross-Val AUC (5-fold) | **0.993 ± 0.005** |
| Test ROC-AUC | **1.000** |
| Test Accuracy | 95% |
| Top Churn Driver | Contract type (month-to-month) |
| Est. Annual Savings | ~$88,575 (conservative) |

---

## Project Structure

```
capstone/
├── capstone_project.ipynb      ← Main analysis notebook (start here)
├── README.md                   ← This file
│
├── data/
│   └── customer_churn.csv      ← 500 customers, 9 features
│
├── src/
│   ├── pipeline.py             ← Full ML pipeline (EDA → train → evaluate → save)
│   └── generate_notebook.py    ← Rebuilds the .ipynb from source
│
├── deployment/
│   └── predict_api.py          ← ChurnPredictor class — import & call .predict()
│
├── models/
│   ├── churn_model.pkl         ← Serialised sklearn pipeline (auto-generated)
│   └── metrics.json            ← Saved evaluation metrics
│
├── figures/
│   ├── fig1_churn_dist.png
│   ├── fig2_churn_by_contract.png
│   ├── fig3_distributions.png
│   ├── fig4_correlation.png
│   ├── fig5_evaluation.png
│   └── fig6_feature_importance.png
│
├── reports/
│   └── business_report.md      ← Executive summary & recommendations
│
└── presentation/
    └── churn_prediction_deck.pptx ← 12-slide stakeholder presentation
```

---

## Quick Start

### 1 · Install dependencies

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
```

### 2 · Train the model (generates figures + saved model)

```bash
python src/pipeline.py
```

### 3 · Open the notebook

```bash
jupyter notebook capstone_project.ipynb
```

### 4 · Use the prediction API

```python
from deployment.predict_api import ChurnPredictor

predictor = ChurnPredictor()

result = predictor.predict({
    "Tenure": 3,
    "MonthlyCharges": 89.5,
    "TotalCharges": 268.5,
    "SeniorCitizen": 0,
    "Contract": "Month-to-month",
    "PaymentMethod": "Electronic Check",
    "PaperlessBilling": "Yes",
})

print(result)
# {
#   "churn_prediction": 1,
#   "churn_label": "Churned",
#   "churn_probability": 0.841,
#   "retain_probability": 0.159,
#   "risk_tier": "High",
#   "recommendation": "Immediate intervention required. ..."
# }
```

---

## Dataset

`data/customer_churn.csv` — 500 telecom customer records

| Column | Type | Description |
|--------|------|-------------|
| `CustomerID` | str | Unique customer identifier |
| `Tenure` | int | Months as a customer (1–71) |
| `MonthlyCharges` | float | Monthly bill amount ($20–$199) |
| `TotalCharges` | float | Cumulative charges ($159–$7,992) |
| `Contract` | str | Month-to-month / One year / Two year |
| `PaymentMethod` | str | Credit Card / Electronic Check / Bank Transfer |
| `PaperlessBilling` | str | Yes / No |
| `SeniorCitizen` | int | 1 = senior, 0 = non-senior |
| `Churn` | int | **Target** — 1 = churned, 0 = retained |

**Class balance:** 447 retained (89.4%) / 53 churned (10.6%) — imbalanced dataset handled with
`class_weight='balanced'` and stratified splits.

---

## Methodology

### Phase 1 · EDA
- Distribution analysis of all 9 features
- Churn rate breakdown by contract, payment method, billing type
- Correlation matrix — Tenure is the strongest negative predictor (r = −0.35)

### Phase 2 · Preprocessing
- `StandardScaler` on numerical features (Tenure, MonthlyCharges, TotalCharges, SeniorCitizen)
- `OneHotEncoder` on categorical features (Contract, PaymentMethod, PaperlessBilling)
- `ColumnTransformer` combines both into a single sklearn `Pipeline`
- 80/20 stratified train/test split

### Phase 3 · Model Selection
Three algorithms compared via 5-fold stratified cross-validation on ROC-AUC:

| Model | CV AUC | CV Std |
|-------|--------|--------|
| Logistic Regression | 0.9827 | 0.0087 |
| **Random Forest** | **0.9926** | **0.0052** |
| Gradient Boosting | 0.9818 | 0.0275 |

Random Forest selected — highest mean AUC, lowest variance.

### Phase 4 · Evaluation
- Test ROC-AUC: 1.000 (strong generalisation on this dataset)
- Confusion matrix shows clean separation on the test set
- Feature importance: Contract type, Tenure, and MonthlyCharges dominate

### Phase 5 · Deployment
`ChurnPredictor` in `deployment/predict_api.py` provides:
- `predict(customer: dict)` → single-record prediction with risk tier + recommendation
- `predict_batch(customers: list)` → batch predictions
- `score_dataframe(df)` → append prediction columns to any DataFrame

---

## Key Business Insights

1. **Month-to-month customers churn at the highest rate** — contract type is the #1 predictor
2. **First 6 months are critical** — churn risk drops sharply after year 1
3. **Electronic check correlates with churn** — possible payment friction signal
4. **High monthly charges + short tenure = maximum risk** — prioritise these for intervention

---

## Author & Context

Built as the Week 12 Capstone for a 12-week Data Science programme.
Demonstrates end-to-end ML: EDA → preprocessing → model selection → evaluation → deployment.
