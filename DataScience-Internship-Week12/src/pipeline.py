"""
Customer Churn Prediction Pipeline
===================================
End-to-end ML pipeline: EDA → preprocessing → model training → evaluation → serialisation.
Run this once to generate models/churn_model.pkl, models/preprocessor.pkl, and all figures/.
"""

import os
import warnings
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    roc_curve, precision_recall_curve, average_precision_score,
    ConfusionMatrixDisplay
)

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = r"D:\Week12_Project"

DATA_PATH = r"D:\Week12_Project\data\customer_churn.csv"

FIG_DIR = r"D:\Week12_Project\figures"

MDL_DIR = r"D:\Week12_Project\models"

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(MDL_DIR, exist_ok=True)

PALETTE = {"churn": "#E53E3E", "retain": "#2B6CB0", "neutral": "#4A5568"}

# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD & VALIDATE DATA
# ══════════════════════════════════════════════════════════════════════════════

def load_data():
    df = pd.read_csv(DATA_PATH)
    print(f"[load] {df.shape[0]} rows × {df.shape[1]} cols")
    print(f"[load] Missing values: {df.isnull().sum().sum()}")
    print(f"[load] Churn distribution:\n{df['Churn'].value_counts(normalize=True).round(3)}\n")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 2. EXPLORATORY DATA ANALYSIS  (saves 4 figures)
# ══════════════════════════════════════════════════════════════════════════════

def run_eda(df):
    # ── Fig 1: churn distribution ──────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(5, 4))
    counts = df["Churn"].value_counts()
    bars = ax.bar(["Retained", "Churned"], counts.values,
                  color=[PALETTE["retain"], PALETTE["churn"]], width=0.5, edgecolor="white")
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"{val}\n({val/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=11)
    ax.set_title("Churn Distribution (500 customers)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Count")
    ax.spines[["top","right"]].set_visible(False)
    ax.set_ylim(0, counts.max() * 1.2)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig1_churn_dist.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Fig 2: churn rate by contract type ────────────────────────────────
    contract_churn = df.groupby("Contract")["Churn"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = [PALETTE["churn"] if v > 0.15 else PALETTE["retain"] for v in contract_churn.values]
    bars = ax.barh(contract_churn.index, contract_churn.values * 100,
                   color=colors, height=0.5, edgecolor="white")
    for bar in bars:
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.1f}%", va="center", fontsize=11)
    ax.set_title("Churn Rate by Contract Type", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Churn Rate (%)")
    ax.set_xlim(0, contract_churn.max() * 130)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig2_churn_by_contract.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Fig 3: numeric distributions by churn ─────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    num_cols = ["Tenure", "MonthlyCharges", "TotalCharges"]
    for ax, col in zip(axes, num_cols):
        for churn_val, label, color in [(0, "Retained", PALETTE["retain"]),
                                         (1, "Churned",  PALETTE["churn"])]:
            vals = df[df["Churn"] == churn_val][col]
            ax.hist(vals, bins=20, alpha=0.6, label=label, color=color, edgecolor="white")
        ax.set_title(col, fontsize=12, fontweight="bold")
        ax.set_ylabel("Count")
        ax.spines[["top","right"]].set_visible(False)
        ax.legend(fontsize=9)
    plt.suptitle("Feature Distributions by Churn Status", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig3_distributions.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Fig 4: correlation heatmap (numeric) ──────────────────────────────
    num_df = df[["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]]
    corr = num_df.corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation Matrix", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig4_correlation.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print("[eda] Saved fig1–fig4")

# ══════════════════════════════════════════════════════════════════════════════
# 3. PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════

NUMERIC_FEATURES     = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
CATEGORICAL_FEATURES = ["Contract", "PaymentMethod", "PaperlessBilling"]

def build_preprocessor():
    return ColumnTransformer(transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
    ])

def prepare_data(df):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df["Churn"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[prep] Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")
    print(f"[prep] Train churn rate: {y_train.mean():.2%}  Test churn rate: {y_test.mean():.2%}\n")
    return X_train, X_test, y_train, y_test

# ══════════════════════════════════════════════════════════════════════════════
# 4. MODEL TRAINING & SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def train_models(X_train, y_train, preprocessor):
    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
        "Random Forest":       RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced"),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = {}
    print("[train] Cross-validation results (ROC-AUC):")
    for name, clf in candidates.items():
        pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
        scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
        results[name] = {"pipeline": pipe, "cv_auc": scores.mean(), "cv_std": scores.std()}
        print(f"  {name:<25} AUC = {scores.mean():.4f} ± {scores.std():.4f}")

    best_name = max(results, key=lambda k: results[k]["cv_auc"])
    best_pipe = results[best_name]["pipeline"]
    print(f"\n[train] Best model: {best_name}\n")
    return best_name, best_pipe, results

# ══════════════════════════════════════════════════════════════════════════════
# 5. EVALUATION  (saves 2 figures)
# ══════════════════════════════════════════════════════════════════════════════

def evaluate(best_name, best_pipe, X_train, X_test, y_train, y_test):
    best_pipe.fit(X_train, y_train)
    y_pred      = best_pipe.predict(X_test)
    y_prob      = best_pipe.predict_proba(X_test)[:, 1]
    roc_auc     = roc_auc_score(y_test, y_prob)
    avg_prec    = average_precision_score(y_test, y_prob)

    print(f"[eval] Test ROC-AUC : {roc_auc:.4f}")
    print(f"[eval] Avg Precision: {avg_prec:.4f}")
    print(f"\n[eval] Classification Report:\n{classification_report(y_test, y_pred, target_names=['Retained','Churned'])}")

    # ── Fig 5: Confusion matrix + ROC curve ───────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=["Retained", "Churned"]).plot(
        ax=ax1, cmap="Blues", colorbar=False)
    ax1.set_title(f"Confusion Matrix\n{best_name}", fontsize=12, fontweight="bold")

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    ax2.plot(fpr, tpr, color=PALETTE["churn"], lw=2, label=f"ROC (AUC = {roc_auc:.3f})")
    ax2.plot([0,1], [0,1], "k--", lw=1)
    ax2.fill_between(fpr, tpr, alpha=0.1, color=PALETTE["churn"])
    ax2.set_xlabel("False Positive Rate"); ax2.set_ylabel("True Positive Rate")
    ax2.set_title("ROC Curve", fontsize=12, fontweight="bold")
    ax2.legend(); ax2.spines[["top","right"]].set_visible(False)

    plt.suptitle("Model Evaluation", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig5_evaluation.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Fig 6: Feature importances (RF) or coefficients (LR) ──────────────
    clf = best_pipe.named_steps["clf"]
    prep = best_pipe.named_steps["prep"]
    cat_names = prep.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    feature_names = NUMERIC_FEATURES + cat_names

    if hasattr(clf, "feature_importances_"):
        importances = clf.feature_importances_
    else:
        importances = np.abs(clf.coef_[0])

    idx = np.argsort(importances)[-12:]
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = [PALETTE["churn"] if importances[i] > np.median(importances) else PALETTE["neutral"] for i in idx]
    ax.barh([feature_names[i] for i in idx], importances[idx], color=colors, edgecolor="white")
    ax.set_title(f"Top Feature Importances\n{best_name}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Importance")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig6_feature_importance.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print("[eval] Saved fig5–fig6")
    metrics = {
        "model": best_name,
        "test_roc_auc": round(roc_auc, 4),
        "avg_precision": round(avg_prec, 4),
    }
    return metrics

# ══════════════════════════════════════════════════════════════════════════════
# 6. SERIALISE
# ══════════════════════════════════════════════════════════════════════════════

def save_artifacts(best_pipe, metrics):
    joblib.dump(best_pipe, os.path.join(MDL_DIR, "churn_model.pkl"))
    with open(os.path.join(MDL_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\n[save] Model → models/churn_model.pkl")
    print(f"[save] Metrics → models/metrics.json")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    df                                             = load_data()
    run_eda(df)
    X_train, X_test, y_train, y_test               = prepare_data(df)
    preprocessor                                   = build_preprocessor()
    best_name, best_pipe, cv_results               = train_models(X_train, y_train, preprocessor)
    metrics                                        = evaluate(best_name, best_pipe, X_train, X_test, y_train, y_test)
    save_artifacts(best_pipe, metrics)
    print("\n✅ Pipeline complete.")
