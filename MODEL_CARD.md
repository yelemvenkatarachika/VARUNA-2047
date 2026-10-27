# Model Card: VARUNA 2047 Agricultural Climate Risk Predictor

## Model Details
- **Architecture**: Gradient Boosted Decision Trees (XGBoost Classifier) & Logistic Regression Baselines
- **Model Version**: 2.0.0-ScientificIntegrityAudit
- **Model License**: MIT Open Access
- **Primary Task**: Binary Seasonal Monsoon Deficit Risk Estimation ($P(\text{JJAS Rainfall} < 80\% \text{ of Climatological Mean})$)
- **Forecast Issuance Date**: **May 31** strictly before Southwest Monsoon onset

## Intended Use
- **Primary Use Case**: Probabilistic early-warning decision support and climate signal tracking for agricultural planners in Telangana districts.
- **Beneficiaries**: District agricultural extension officers, irrigation engineers, rural credit and crop insurance contingency planners.
- **Out-of-Scope Use**: NOT intended as an automated operational forecast for binding financial disbursements without meteorological ground-truthing. Must be used alongside Indian Ocean Dipole (IOD) monitoring and IMD seasonal outlooks.

## Training & Evaluation Data
- **Geographic Pilot**: Telangana, India (Warangal, Hanamkonda, Karimnagar, Nizamabad, Adilabad, Khammam)
- **Training Period**: 1982–2014 (33 years, 198 district-years)
- **Validation Period**: 2015–2018 (4 years, 24 district-years)
- **Untouched Out-of-Sample Test Period**: 2019–2024 (6 years, 36 district-years)
- **Split Strategy**: Strictly chronological. No temporal shuffling. No target leakage.

## Quantitative Performance Comparison (Untouched Held-Out Test 2019–2024)

> **CRITICAL SCIENTIFIC INTEGRITY AUDIT FINDING:**  
> On the untouched 2019–2024 held-out test period, **the Climatological Base Rate model decisively outperforms all Machine Learning models** on Brier Score (0.0408 vs 0.1698–0.2182) and Log Loss (0.2257 vs 0.5192–0.6264).  
> In this 6-year period, Telangana experienced zero deficit seasons ($N_+ = 0, N_- = 36$). Because ML models detected the 2019 and 2023 El Niño signals and elevated deficit probabilities, but no regional drought materialized (buffered by positive IOD and Bay depressions), the models issued false alarms and suffered severe Brier penalties.  
> ROC-AUC is **mathematically undefined** on the untouched test set because ground truth contains only negative cases.

| Model Name | Features | Brier Score (lower is better) | Log Loss | ROC-AUC | F1-Score | False Alarms ($p \ge 0.5$) |
|---|---|---|---|---|---|---|
| **Climatological Base Rate (Best)** | Base Climatology ($p=0.202$) | **0.0408** | **0.2257** | Undefined ($N_+=0$) | 0.0000 | 0 / 36 |
| ENSO-Only Logistic Regression | Niño 3.4 & ONI | 0.2182 | 0.6264 | Undefined ($N_+=0$) | 0.0000 | 12 / 36 |
| ENSO + Climate Logistic Regression | ENSO + Pre-Monsoon Rain | 0.1698 | 0.5192 | Undefined ($N_+=0$) | 0.0000 | 9 / 36 |
| VARUNA Multimodal XGBoost | Multimodal Stack | 0.1913 | 0.5308 | Undefined ($N_+=0$) | 0.0000 | 14 / 36 |

## Explainability & SHAP Importance
Top features influencing seasonal deficit risk estimation in the XGBoost tree ensemble:
- **nino34_trend**: SHAP impact 1.1871
- **nino34_mam**: SHAP impact 0.6284
- **preseason_rainfall_mam_mm**: SHAP impact 0.1945
- **preseason_may_ndvi**: SHAP impact 0.0971
- **preseason_rainfall_mam_anom_mm**: SHAP impact 0.0904
- **prev_year_jjas_rainfall_mm**: SHAP impact 0.0735
- **preseason_may_ndvi_anomaly**: SHAP impact 0.0661
- **nino34_djf**: SHAP impact 0.0604

## Limitations, Diagnostics & Scientific Honesty
1. **Climatology Superiority**: In climate regimes where target anomalies do not occur, static climatology produces significantly lower quadratic error than dynamic models that elevate risk based on large-scale teleconnections.
2. **Teleconnection Buffering**: The 2023 Super El Niño did not cause drought in Telangana due to a mitigating positive Indian Ocean Dipole (+1.8°C) and favorable late-monsoon Bay of Bengal depressions. The models lack an explicit IOD predictor, causing overconfident false alarms in 2023.
3. **Severe Class Imbalance & Spatial Correlation**: 36 test samples from 6 adjacent Telangana districts share regional synoptic weather, reducing effective degrees of freedom.
4. **Diagnostic vs Test Window Disclosure**: A 10-year diagnostic window (2015–2024, ROC-AUC 0.7830) was evaluated post-hoc to examine performance across both drought (2015) and wet (2020) regimes. It must NEVER be conflated with the pure untouched 2019–2024 test set.
