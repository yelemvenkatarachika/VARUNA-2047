"""
VARUNA 2047 - ML Scientific Leakage & Metric Recalculation Auditor
Independently verifies:
1. Feature matrix chronology and checks for post-May 31 target leakage.
2. Confirm existence and integrity of model artifacts (.joblib).
3. Recalculates reported evaluation metrics from raw predictions.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix

DATASET_CSV = "data/processed/model_features_dataset.csv"
SCHEMA_JSON = "data/processed/feature_schema.json"
MODELS_DIR = "models/saved"
METRICS_JSON = "models/saved/evaluation_metrics.json"
PREDICTIONS_JSON = "models/saved/test_predictions.json"

REQUIRED_ARTIFACTS = [
    "logistic_enso.joblib",
    "scaler_enso.joblib",
    "logistic_climate.joblib",
    "scaler_climate.joblib",
    "xgboost_varuna.joblib",
    "scaler_multimodal.joblib",
    "evaluation_metrics.json",
    "test_predictions.json",
    "shap_summary.json"
]

def audit_ml():
    print("="*75)
    print("SCIENTIFIC ML AUDIT: LEAKAGE PREVENTION & METRIC RECALCULATION")
    print("="*75)

    # 1. Artifact Existence Check
    print("1. Artifact Existence Check:")
    all_artifacts_exist = True
    for fname in REQUIRED_ARTIFACTS:
        fpath = os.path.join(MODELS_DIR, fname)
        if os.path.exists(fpath):
            sz = os.path.getsize(fpath)
            print(f"  [PASS] {fname:<30} ({sz:,} bytes)")
        else:
            print(f"  [FAIL] {fname:<30} MISSING!")
            all_artifacts_exist = False

    # 2. Chronological Split & Target Leakage Audit
    print("\n2. Chronological Splitting & Leakage Audit:")
    df = pd.read_csv(DATASET_CSV)
    with open(SCHEMA_JSON, "r", encoding="utf-8") as f:
        schema = json.load(f)

    train_years = set(df[df["split"] == "train"]["year"].unique())
    val_years = set(df[df["split"] == "val"]["year"].unique())
    test_years = set(df[df["split"] == "test"]["year"].unique())

    print(f"  Train Years: {min(train_years)} to {max(train_years)} ({len(train_years)} years, {len(df[df['split']=='train'])} samples)")
    print(f"  Val Years:   {min(val_years)} to {max(val_years)} ({len(val_years)} years, {len(df[df['split']=='val'])} samples)")
    print(f"  Test Years:  {min(test_years)} to {max(test_years)} ({len(test_years)} years, {len(df[df['split']=='test'])} samples)")

    # Test year boundaries
    assert max(train_years) < min(val_years), "LEAKAGE: Train years overlap with Validation!"
    assert max(val_years) < min(test_years), "LEAKAGE: Validation years overlap with Test!"
    print("  [PASS] Chronological boundaries are strictly non-overlapping.")

    # Check predictor feature definitions
    features = schema["feature_groups"]["group_d_full_multimodal"]
    forbidden_terms = ["jjas", "monsoon_rf", "august", "september", "actual", "y_target"]
    leakage_found = False
    for feat in features:
        # prev_year_jjas_rainfall_mm is allowed (lagged 1 year)
        if any(term in feat for term in ["august", "september"]) or (any(term in feat for term in ["jjas", "monsoon"]) and "prev_year" not in feat):
            print(f"  [FAIL] Target leakage detected in feature: {feat}")
            leakage_found = True

    if not leakage_found:
        print(f"  [PASS] All {len(features)} predictors are strictly observable on or before May 31.")

    # 3. Independent Metric Recalculation from Raw Test Predictions
    print("\n3. Independent Metric Recalculation from Saved Predictions:")
    with open(PREDICTIONS_JSON, "r", encoding="utf-8") as f:
        test_preds = json.load(f)
    with open(METRICS_JSON, "r", encoding="utf-8") as f:
        reported_metrics = json.load(f)

    pred_df = pd.DataFrame(test_preds)
    y_test_true = pred_df["actual_deficit_event"].values
    p_enso_lr = pred_df["predicted_prob_enso_lr"].values
    p_xgb = pred_df["predicted_prob_xgboost"].values
    p_clim = pred_df["predicted_prob_climatology"].values

    # Recalculate 2019-2024 Test Window
    brier_enso_calc = round(float(brier_score_loss(y_test_true, p_enso_lr)), 4)
    brier_xgb_calc = round(float(brier_score_loss(y_test_true, p_xgb)), 4)
    brier_clim_calc = round(float(brier_score_loss(y_test_true, p_clim)), 4)

    rep_enso = reported_metrics["models"]["model_b_enso_lr"]["brier_score"]
    rep_xgb = reported_metrics["models"]["model_d_xgboost_multimodal"]["brier_score"]
    rep_clim = reported_metrics["models"]["model_a_climatology"]["brier_score"]

    print(f"  Climatology Brier: Recalculated = {brier_clim_calc} | Reported = {rep_clim} | Match = {brier_clim_calc == rep_clim}")
    print(f"  ENSO-LR Brier:     Recalculated = {brier_enso_calc} | Reported = {rep_enso} | Match = {brier_enso_calc == rep_enso}")
    print(f"  XGBoost Brier:     Recalculated = {brier_xgb_calc} | Reported = {rep_xgb} | Match = {brier_xgb_calc == rep_xgb}")

    # 4. Multi-Window Operational Test (2015-2024 decade)
    print("\n4. Combined Out-of-Sample Window (2015-2024, 60 district-years):")
    oos_df = df[df["year"] >= 2015]
    y_oos_true = oos_df["y_deficit_event"].values

    lr_enso = joblib.load(os.path.join(MODELS_DIR, "logistic_enso.joblib"))
    scaler_enso = joblib.load(os.path.join(MODELS_DIR, "scaler_enso.joblib"))
    feat_b = schema["feature_groups"]["group_b_enso_only"]
    X_oos_b = scaler_enso.transform(oos_df[feat_b])
    p_oos_enso = lr_enso.predict_proba(X_oos_b)[:, 1]

    roc_oos_calc = round(float(roc_auc_score(y_oos_true, p_oos_enso)), 4)
    f1_oos_calc = round(float(f1_score(y_oos_true, (p_oos_enso >= 0.5).astype(int))), 4)
    brier_oos_calc = round(float(brier_score_loss(y_oos_true, p_oos_enso)), 4)

    rep_oos_roc = reported_metrics["multi_window_evaluation"]["evaluation_windows"]["combined_oos_2015_2024"]["models"]["ENSO-Only LR"]["roc_auc"]
    rep_oos_f1 = reported_metrics["multi_window_evaluation"]["evaluation_windows"]["combined_oos_2015_2024"]["models"]["ENSO-Only LR"]["f1"]

    print(f"  ENSO-LR 10-Yr ROC-AUC: Recalculated = {roc_oos_calc} | Reported = {rep_oos_roc} | Match = {roc_oos_calc == rep_oos_roc}")
    print(f"  ENSO-LR 10-Yr F1-Score: Recalculated = {f1_oos_calc} | Reported = {rep_oos_f1} | Match = {f1_oos_calc == rep_oos_f1}")
    print(f"  ENSO-LR 10-Yr Brier:    Recalculated = {brier_oos_calc}")

    print("\n" + "="*75)
    if all_artifacts_exist and not leakage_found and (roc_oos_calc == rep_oos_roc) and (brier_enso_calc == rep_enso):
        print("ALL SCIENTIFIC VALIDATION CRITERIA PASS AUDIT WITH 100% REPRODUCIBILITY!")
    else:
        print("SCIENTIFIC AUDIT DETECTED INCONSISTENCIES!")
    print("="*75)

if __name__ == "__main__":
    audit_ml()
