"""
PhishGuard AI - Model Training Pipeline
=======================================
Trains, tunes, evaluates, and serializes the Random Forest Classifier
for PhishGuard AI URL risk detection.

Features:
- Stratified Train-Test splitting (80% / 20%).
- Hyperparameter tuning via GridSearchCV with 5-fold cross-validation.
- Full evaluation: Accuracy, Precision, Recall, F1-Score, ROC-AUC.
- Feature importance analysis.
- Serialization with joblib and export to backend models directory.
"""

import json
import os
import shutil
import time
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import GridSearchCV

from preprocessing import load_and_inspect_dataset, prepare_train_test_split, RANDOM_STATE
from feature_extraction import FEATURE_NAMES

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CURRENT_DIR, "dataset", "dataset_30features_11055.csv")
ML_MODELS_DIR = os.path.join(CURRENT_DIR, "models")
BACKEND_MODELS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "backend", "models"))
REPORTS_DIR = os.path.join(CURRENT_DIR, "reports")

os.makedirs(ML_MODELS_DIR, exist_ok=True)
os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def train_phishguard_model() -> Dict[str, Any]:
    print("=" * 65)
    print("      PhishGuard AI - Random Forest Model Training Pipeline")
    print("=" * 65)

    start_time = time.time()

    # 1. Load and inspect dataset
    print(f"\n[1/7] Loading dataset from: {DATASET_PATH}")
    df, diagnostics = load_and_inspect_dataset(DATASET_PATH)
    print(f"      Loaded: {diagnostics['cleaned_rows']} records, {diagnostics['cleaned_columns']} columns")
    print(f"      Duplicates removed: {diagnostics['duplicates_removed']}, Missing values: {diagnostics['total_missing_values']}")
    print(f"      Class distribution: {diagnostics['label_distribution']}")

    # 2. Train-test split
    print("\n[2/7] Splitting dataset (80% Train, 20% Test) with Stratification...")
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, target_column="label", test_size=0.20)
    print(f"      Training samples: {X_train.shape[0]} | Testing samples: {X_test.shape[0]}")
    print(f"      Feature count: {X_train.shape[1]}")

    # Verify column alignment with FEATURE_NAMES
    assert list(X_train.columns) == FEATURE_NAMES, "Feature column ordering mismatch!"

    # 3. Hyperparameter Tuning Setup
    print("\n[3/7] Setting up Hyperparameter Grid Search (5-fold Cross-Validation)...")
    param_grid = {
        "n_estimators": [100, 150, 200],
        "max_depth": [15, 25, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "criterion": ["gini", "entropy"],
    }

    base_rf = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)

    grid_search = GridSearchCV(
        estimator=base_rf,
        param_grid=param_grid,
        cv=5,
        scoring="f1",
        n_jobs=-1,
        verbose=1
    )

    print("      Executing Grid Search...")
    grid_search.fit(X_train, y_train)

    best_model: RandomForestClassifier = grid_search.best_estimator_
    best_params = grid_search.best_params_
    print(f"\n[4/7] Best Hyperparameters Identified:")
    for param, val in best_params.items():
        print(f"      - {param}: {val}")
    print(f"      Best 5-fold CV F1-Score: {grid_search.best_score_:.4f}")

    # 4. Evaluation on Unseen Test Set
    print("\n[5/7] Evaluating Best Model on Test Set...")
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred))
    rec = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_proba))
    cm = confusion_matrix(y_test, y_pred).tolist()

    print(f"      Test Accuracy:  {acc * 100:.2f}%")
    print(f"      Precision:      {prec * 100:.2f}%")
    print(f"      Recall:         {rec * 100:.2f}%")
    print(f"      F1-Score:       {f1 * 100:.2f}%")
    print(f"      ROC-AUC Score:  {roc_auc:.4f}")
    print("\n      Confusion Matrix:")
    print(f"        TN: {cm[0][0]:<5} | FP: {cm[0][1]:<5}")
    print(f"        FN: {cm[1][0]:<5} | TP: {cm[1][1]:<5}")

    print("\n      Detailed Classification Report:")
    report_str = classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"])
    print(report_str)

    # 5. Feature Importance Analysis
    print("\n[6/7] Computing Gini Feature Importances...")
    importances = best_model.feature_importances_
    feat_imp = []
    for name, imp in zip(FEATURE_NAMES, importances):
        feat_imp.append({"feature": name, "importance": round(float(imp), 5)})
    feat_imp.sort(key=lambda x: x["importance"], reverse=True)

    print("      Top 10 Most Influential Features:")
    for rank, item in enumerate(feat_imp[:10], start=1):
        print(f"      {rank:2d}. {item['feature']:<26} : {item['importance']:.5f}")

    # 6. Model Serialization & Metadata Export
    print("\n[7/7] Serializing Model & Metadata...")
    model_filename = "phishguard_rf_model.joblib"
    ml_model_path = os.path.join(ML_MODELS_DIR, model_filename)
    backend_model_path = os.path.join(BACKEND_MODELS_DIR, model_filename)

    # Save with joblib compression (level 3 for fast loading and low disk footprint)
    joblib.dump(best_model, ml_model_path, compress=3)
    shutil.copy2(ml_model_path, backend_model_path)
    print(f"      Model saved to: {ml_model_path}")
    print(f"      Synced to backend: {backend_model_path}")

    elapsed_time = round(time.time() - start_time, 2)

    metadata = {
        "model_name": "PhishGuard AI Random Forest Classifier",
        "algorithm": "RandomForestClassifier",
        "num_features": len(FEATURE_NAMES),
        "feature_names": FEATURE_NAMES,
        "classes": ["Legitimate", "Phishing"],
        "class_mapping": {"0": "Legitimate", "1": "Phishing"},
        "best_hyperparameters": best_params,
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": {
                "true_negative": cm[0][0],
                "false_positive": cm[0][1],
                "false_negative": cm[1][0],
                "true_positive": cm[1][1]
            }
        },
        "dataset": {
            "total_records": diagnostics["cleaned_rows"],
            "training_samples": int(X_train.shape[0]),
            "testing_samples": int(X_test.shape[0]),
            "phishing_count": diagnostics["label_counts"].get(1, 0),
            "legitimate_count": diagnostics["label_counts"].get(0, 0),
        },
        "feature_importances": feat_imp,
        "training_duration_seconds": elapsed_time,
        "random_state": RANDOM_STATE
    }

    ml_meta_path = os.path.join(ML_MODELS_DIR, "model_metadata.json")
    backend_meta_path = os.path.join(BACKEND_MODELS_DIR, "model_metadata.json")

    with open(ml_meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    shutil.copy2(ml_meta_path, backend_meta_path)
    print(f"      Metadata saved to: {ml_meta_path}")
    print(f"      Synced to backend: {backend_meta_path}")

    # Also save a text report
    report_file = os.path.join(REPORTS_DIR, "model_evaluation_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("PhishGuard AI - Model Evaluation Report\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Algorithm: Random Forest Classifier\n")
        f.write(f"Dataset Size: {diagnostics['cleaned_rows']} records\n")
        f.write(f"Features: 30 lexical & structural URL features\n\n")
        f.write(f"Accuracy:  {acc * 100:.2f}%\n")
        f.write(f"Precision: {prec * 100:.2f}%\n")
        f.write(f"Recall:    {rec * 100:.2f}%\n")
        f.write(f"F1-Score:  {f1 * 100:.2f}%\n")
        f.write(f"ROC-AUC:   {roc_auc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(f"  TN: {cm[0][0]}  FP: {cm[0][1]}\n")
        f.write(f"  FN: {cm[1][0]}  TP: {cm[1][1]}\n\n")
        f.write("Detailed Report:\n")
        f.write(report_str + "\n\n")
        f.write("Top 10 Features:\n")
        for rank, item in enumerate(feat_imp[:10], start=1):
            f.write(f"  {rank:2d}. {item['feature']:<25} : {item['importance']:.5f}\n")

    print(f"      Summary report saved to: {report_file}")
    print("=" * 65)
    print(f"[✓] Pipeline Completed Successfully in {elapsed_time}s!")
    print("=" * 65)

    return metadata


if __name__ == "__main__":
    train_phishguard_model()
