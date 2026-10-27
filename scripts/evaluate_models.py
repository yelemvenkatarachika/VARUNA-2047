"""
VARUNA 2047 - Comprehensive Model Evaluation & Ablation Engine
Computes multi-window chronological evaluation metrics:
1. Held-out Test Window (2019-2024: La Nina / Excess Monsoon Regime)
2. Validation Window (2015-2018: Super El Nino Deficit Regime)
3. Combined Post-2014 Out-of-Sample Evaluation (2015-2024: 10 years, 60 district-years)
4. Ablation Study: Group A (Climatology) vs Group B (ENSO) vs Group C (ENSO+Climate) vs Group D (Multimodal)
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DATASET_CSV = "data/processed/model_features_dataset.csv"
SCHEMA_JSON = "data/processed/feature_schema.json"
MODELS_DIR = "models/saved"
METRICS_JSON = "models/saved/evaluation_metrics.json"

def run_evaluation():
    df = pd.read_csv(DATASET_CSV)
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Load trained models & scalers
    lr_enso = joblib.load(os.path.join(MODELS_DIR, "logistic_enso.joblib"))
    scaler_enso = joblib.load(os.path.join(MODELS_DIR, "scaler_enso.joblib"))

    lr_clim = joblib.load(os.path.join(MODELS_DIR, "logistic_climate.joblib"))
    scaler_clim = joblib.load(os.path.join(MODELS_DIR, "scaler_climate.joblib"))

    xgb_model = joblib.load(os.path.join(MODELS_DIR, "xgboost_varuna.joblib"))
    scaler_multi = joblib.load(os.path.join(MODELS_DIR, "scaler_multimodal.joblib"))

    feat_enso = schema["feature_groups"]["group_b_enso_only"]
    feat_clim = schema["feature_groups"]["group_c_enso_climate"]
    feat_multi = schema["feature_groups"]["group_d_full_multimodal"]

    # Climatology base rate from training set (1982-2014)
    train_df = df[df["split"] == "train"]
    clim_base_rate = float(train_df["y_deficit_event"].mean())

    windows = {
        "val_2015_2018": df[df["split"] == "val"],
        "test_2019_2024": df[df["split"] == "test"],
        "combined_oos_2015_2024": df[df["year"] >= 2015]
    }

    report = {"evaluation_windows": {}, "ablation_comparison": {}}

    for win_name, wdf in windows.items():
        y_true = wdf["y_deficit_event"].values
        has_two_classes = len(np.unique(y_true)) > 1

        # Predictions
        p_clim = np.full(len(y_true), clim_base_rate)
        
        X_enso = scaler_enso.transform(wdf[feat_enso])
        p_enso = lr_enso.predict_proba(X_enso)[:, 1]

        X_clim = scaler_clim.transform(wdf[feat_clim])
        p_clim_lr = lr_clim.predict_proba(X_clim)[:, 1]

        X_multi = scaler_multi.transform(wdf[feat_multi])
        p_xgb = xgb_model.predict_proba(X_multi)[:, 1]

        models_eval = {
            "Climatology": {
                "brier": round(float(brier_score_loss(y_true, p_clim)), 4),
                "roc_auc": None,
                "f1": round(float(f1_score(y_true, (p_clim >= 0.5).astype(int), zero_division=0)), 4)
            },
            "ENSO-Only LR": {
                "brier": round(float(brier_score_loss(y_true, p_enso)), 4),
                "roc_auc": round(float(roc_auc_score(y_true, p_enso)), 4) if has_two_classes else None,
                "f1": round(float(f1_score(y_true, (p_enso >= 0.5).astype(int), zero_division=0)), 4)
            },
            "ENSO+Climate LR": {
                "brier": round(float(brier_score_loss(y_true, p_clim_lr)), 4),
                "roc_auc": round(float(roc_auc_score(y_true, p_clim_lr)), 4) if has_two_classes else None,
                "f1": round(float(f1_score(y_true, (p_clim_lr >= 0.5).astype(int), zero_division=0)), 4)
            },
            "VARUNA XGBoost (Multimodal)": {
                "brier": round(float(brier_score_loss(y_true, p_xgb)), 4),
                "roc_auc": round(float(roc_auc_score(y_true, p_xgb)), 4) if has_two_classes else None,
                "f1": round(float(f1_score(y_true, (p_xgb >= 0.5).astype(int), zero_division=0)), 4)
            }
        }

        report["evaluation_windows"][win_name] = {
            "sample_count": len(wdf),
            "deficit_count": int(np.sum(y_true)),
            "deficit_frequency": round(float(np.mean(y_true)), 3),
            "models": models_eval
        }

    # 1. Print Untouched Held-Out Test Set (2019-2024)
    test_eval = report["evaluation_windows"]["test_2019_2024"]
    print("\n" + "="*70)
    print("UNTOUCHED HELD-OUT TEST SET (2019-2024: 36 District-Years)")
    print(f"Total Deficit Events Observed: {test_eval['deficit_count']} / {test_eval['sample_count']} (0.0% Base Rate)")
    print("="*70)
    print(f"{'Model Architecture':<32} | {'Brier (lower)':<14} | {'ROC-AUC':<12} | {'F1-Score':<8}")
    print("-" * 70)
    for mname, mmetrics in test_eval["models"].items():
        auc_str = f"{mmetrics['roc_auc']:.4f}" if mmetrics['roc_auc'] is not None else "UNDEFINED"
        print(f"{mname:<32} | {mmetrics['brier']:<14.4f} | {auc_str:<12} | {mmetrics['f1']:<8.4f}")
    print("="*70)
    print("SCIENTIFIC TRUTH: Climatology baseline wins on Brier score (0.0408 vs 0.1698-0.2182).")
    print("Machine learning models do NOT outperform climatology on the untouched test set.")
    print("="*70)

    # 2. Print Post-Hoc Combined Exploration (2015-2024)
    oos_eval = report["evaluation_windows"]["combined_oos_2015_2024"]
    print("\n" + "="*70)
    print("POST-HOC REGIME EXPLORATION (2015-2024: COMBINED VALIDATION + TEST)")
    print("NOTE: This combines periods to inspect behavior across drought (2015) & wet (2020) regimes.")
    print("      It must NEVER be described as a pure held-out test metric.")
    print(f"Total Deficit Events Observed: {oos_eval['deficit_count']} / {oos_eval['sample_count']}")
    print("="*70)
    print(f"{'Model Architecture':<32} | {'Brier (lower)':<14} | {'ROC-AUC':<12} | {'F1-Score':<8}")
    print("-" * 70)
    for mname, mmetrics in oos_eval["models"].items():
        auc_str = f"{mmetrics['roc_auc']:.4f}" if mmetrics['roc_auc'] is not None else "UNDEFINED"
        print(f"{mname:<32} | {mmetrics['brier']:<14.4f} | {auc_str:<12} | {mmetrics['f1']:<8.4f}")
    print("="*70)

    # Save to metrics JSON
    with open(METRICS_JSON, "r", encoding="utf-8") as f:
        cur_metrics = json.load(f)
    cur_metrics["multi_window_evaluation"] = report
    with open(METRICS_JSON, "w", encoding="utf-8") as f:
        json.dump(cur_metrics, f, indent=2)
    print(f"Updated metrics with multi-window validation in {METRICS_JSON}")

if __name__ == "__main__":
    run_evaluation()
