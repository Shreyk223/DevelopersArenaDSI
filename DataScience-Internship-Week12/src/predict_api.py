"""
Customer Churn Prediction API
==============================
Provides a clean prediction interface around the trained churn model.

Usage (command line):
    python predict_api.py

Usage (import):
    from deployment.predict_api import ChurnPredictor
    predictor = ChurnPredictor()
    result = predictor.predict({...})
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Union

# ── Path resolution (works whether run from project root or deployment/) ──────
BASE_DIR = r"D:\Week12_Project"

MODEL_PATH = r"D:\Week12_Project\models\churn_model.pkl"


NUMERIC_FEATURES     = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
CATEGORICAL_FEATURES = ["Contract", "PaymentMethod", "PaperlessBilling"]
ALL_FEATURES         = NUMERIC_FEATURES + CATEGORICAL_FEATURES

VALID_CONTRACTS     = ["Month-to-month", "One year", "Two year"]
VALID_PAYMENTS      = ["Credit Card", "Electronic Check", "Bank Transfer"]
VALID_PAPERLESS     = ["Yes", "No"]


class ValidationError(ValueError):
    """Raised when input data fails schema validation."""


class ChurnPredictor:
    """
    Thin wrapper around the serialised sklearn pipeline.

    Parameters
    ----------
    model_path : str, optional
        Path to the .pkl file produced by src/pipeline.py.
        Defaults to models/churn_model.pkl relative to this file.
    """

    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run `python src/pipeline.py` first to train and save the model."
            )
        self._pipeline = joblib.load(model_path)
        print(f"[ChurnPredictor] Model loaded from {model_path}")

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _validate(data: dict) -> None:
        """Raise ValidationError for missing keys or out-of-range values."""
        missing = [f for f in ALL_FEATURES if f not in data]
        if missing:
            raise ValidationError(f"Missing required fields: {missing}")

        if not (0 <= int(data["Tenure"]) <= 100):
            raise ValidationError("Tenure must be between 0 and 100 months.")
        if not (0 <= float(data["MonthlyCharges"]) <= 500):
            raise ValidationError("MonthlyCharges must be between 0 and 500.")
        if not (0 <= float(data["TotalCharges"]) <= 100_000):
            raise ValidationError("TotalCharges must be between 0 and 100,000.")
        if int(data["SeniorCitizen"]) not in (0, 1):
            raise ValidationError("SeniorCitizen must be 0 or 1.")
        if data["Contract"] not in VALID_CONTRACTS:
            raise ValidationError(f"Contract must be one of {VALID_CONTRACTS}.")
        if data["PaymentMethod"] not in VALID_PAYMENTS:
            raise ValidationError(f"PaymentMethod must be one of {VALID_PAYMENTS}.")
        if data["PaperlessBilling"] not in VALID_PAPERLESS:
            raise ValidationError(f"PaperlessBilling must be 'Yes' or 'No'.")

    @staticmethod
    def _to_df(data: Union[dict, list]) -> pd.DataFrame:
        records = data if isinstance(data, list) else [data]
        df = pd.DataFrame(records, columns=ALL_FEATURES)
        df["Tenure"]         = df["Tenure"].astype(int)
        df["MonthlyCharges"] = df["MonthlyCharges"].astype(float)
        df["TotalCharges"]   = df["TotalCharges"].astype(float)
        df["SeniorCitizen"]  = df["SeniorCitizen"].astype(int)
        return df

    # ── Public API ────────────────────────────────────────────────────────────

    def predict(self, customer: dict) -> dict:
        """
        Predict churn for a single customer.

        Parameters
        ----------
        customer : dict
            Keys: Tenure, MonthlyCharges, TotalCharges, SeniorCitizen,
                  Contract, PaymentMethod, PaperlessBilling

        Returns
        -------
        dict
            {
              "churn_prediction": 0 or 1,
              "churn_label": "Retained" or "Churned",
              "churn_probability": float,   # probability of churning
              "retain_probability": float,  # probability of staying
              "risk_tier": "Low" | "Medium" | "High",
              "recommendation": str
            }
        """
        self._validate(customer)
        df    = self._to_df(customer)
        pred  = int(self._pipeline.predict(df)[0])
        proba = self._pipeline.predict_proba(df)[0]

        churn_prob  = float(proba[1])
        retain_prob = float(proba[0])

        if churn_prob >= 0.70:
            risk_tier = "High"
            recommendation = ("Immediate intervention required. "
                              "Assign a retention specialist and offer a contract upgrade incentive.")
        elif churn_prob >= 0.40:
            risk_tier = "Medium"
            recommendation = ("Monitor closely. "
                              "Send a proactive satisfaction survey and targeted discount offer.")
        else:
            risk_tier = "Low"
            recommendation = ("Customer is stable. "
                              "Standard engagement — upsell opportunities may apply.")

        return {
            "churn_prediction":  pred,
            "churn_label":       "Churned" if pred == 1 else "Retained",
            "churn_probability": round(churn_prob,  4),
            "retain_probability": round(retain_prob, 4),
            "risk_tier":         risk_tier,
            "recommendation":    recommendation,
        }

    def predict_batch(self, customers: list) -> list:
        """
        Predict churn for multiple customers.

        Parameters
        ----------
        customers : list of dict
            Each dict has the same keys as predict().

        Returns
        -------
        list of dict  (same structure as predict() output, plus 'index')
        """
        results = []
        for i, customer in enumerate(customers):
            try:
                result = self.predict(customer)
                result["index"] = i
                results.append(result)
            except ValidationError as e:
                results.append({"index": i, "error": str(e)})
        return results

    def score_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Score an entire DataFrame and append prediction columns.
        Useful for batch-scoring new customer export files.

        Parameters
        ----------
        df : pd.DataFrame with columns matching ALL_FEATURES

        Returns
        -------
        pd.DataFrame with added columns:
            churn_prediction, churn_probability, risk_tier
        """
        out = df.copy()
        preds  = self._pipeline.predict(out[ALL_FEATURES])
        probas = self._pipeline.predict_proba(out[ALL_FEATURES])[:, 1]
        out["churn_prediction"]  = preds
        out["churn_probability"] = probas.round(4)
        out["risk_tier"] = pd.cut(
            probas,
            bins=[-0.001, 0.40, 0.70, 1.001],
            labels=["Low", "Medium", "High"]
        )
        return out


# ── CLI demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    predictor = ChurnPredictor()

    print("\n" + "="*60)
    print("DEMO: Single-customer prediction")
    print("="*60)

    # High-risk customer: month-to-month, electronic check, short tenure
    high_risk = {
        "Tenure": 3,
        "MonthlyCharges": 89.5,
        "TotalCharges": 268.5,
        "SeniorCitizen": 0,
        "Contract": "Month-to-month",
        "PaymentMethod": "Electronic Check",
        "PaperlessBilling": "Yes",
    }

    # Low-risk customer: long tenure, two-year contract
    low_risk = {
        "Tenure": 48,
        "MonthlyCharges": 55.0,
        "TotalCharges": 2640.0,
        "SeniorCitizen": 0,
        "Contract": "Two year",
        "PaymentMethod": "Credit Card",
        "PaperlessBilling": "No",
    }

    for label, customer in [("High-risk customer", high_risk), ("Low-risk customer", low_risk)]:
        result = predictor.predict(customer)
        print(f"\n── {label} ──")
        print(f"  Input  : Contract={customer['Contract']}, "
              f"Tenure={customer['Tenure']}mo, Monthly=${customer['MonthlyCharges']}")
        print(f"  Result : {result['churn_label']} | "
              f"Churn prob: {result['churn_probability']:.1%} | "
              f"Risk: {result['risk_tier']}")
        print(f"  Action : {result['recommendation']}")

    print("\n" + "="*60)
    print("DEMO: Batch prediction (3 customers)")
    print("="*60)

    batch = [high_risk, low_risk, {
        "Tenure": 18,
        "MonthlyCharges": 120.0,
        "TotalCharges": 2160.0,
        "SeniorCitizen": 1,
        "Contract": "One year",
        "PaymentMethod": "Bank Transfer",
        "PaperlessBilling": "Yes",
    }]

    batch_results = predictor.predict_batch(batch)
    for r in batch_results:
        idx = r.get("index", "?")
        if "error" in r:
            print(f"  Customer {idx}: ERROR — {r['error']}")
        else:
            print(f"  Customer {idx}: {r['churn_label']} | "
                  f"P(churn)={r['churn_probability']:.1%} | Tier={r['risk_tier']}")

    print("\n✅ API demo complete.")
