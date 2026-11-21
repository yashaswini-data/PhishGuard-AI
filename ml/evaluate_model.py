"""
PhishGuard AI - Evaluation & Reporting Module
=============================================
Computes comprehensive performance diagnostics and generates publication-quality
visualizations: Confusion Matrix heatmap, ROC Curve, and Feature Importance bar charts.
"""

import json
import os
import joblib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless server execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc,
    confusion_matrix,
    classification_report
)

from preprocessing import load_and_inspect_dataset, prepare_train_test_split
from feature_extraction import FEATURE_NAMES

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CURRENT_DIR, "dataset", "dataset_30features_11055.csv")
MODEL_PATH = os.path.join(CURRENT_DIR, "models", "phishguard_rf_model.joblib")
REPORTS_DIR = os.path.join(CURRENT_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_evaluation_visualizations():
    print("=" * 60)
    print("   PhishGuard AI - Generating Evaluation Visualizations")
    print("=" * 60)

    # 1. Load trained model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model not found at: {MODEL_PATH}. Run train_model.py first.")

    model = joblib.load(MODEL_PATH)
    print(f"[*] Loaded trained model: {type(model).__name__}")

    # 2. Load and split test dataset
    df, _ = load_and_inspect_dataset(DATASET_PATH)
    _, X_test, _, y_test = prepare_train_test_split(df, target_column="label", test_size=0.20)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    cm = confusion_matrix(y_test, y_pred)

    print(f"[+] Performance Summary:")
    print(f"    Accuracy:  {acc * 100:.2f}%")
    print(f"    Precision: {prec * 100:.2f}%")
    print(f"    Recall:    {rec * 100:.2f}%")
    print(f"    F1-Score:  {f1 * 100:.2f}%")
    print(f"    ROC-AUC:   {roc_auc:.4f}")

    # Styling configuration
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Confusion Matrix Heatmap
    plt.figure(figsize=(7, 6))
    cm_labels = ["Legitimate (0)", "Phishing (1)"]
    group_counts = [f"{v:0.0f}" for v in cm.flatten()]
    group_percentages = [f"{v:.2%}" for v in cm.flatten() / np.sum(cm)]
    box_labels = [f"{v1}\n({v2})" for v1, v2 in zip(group_counts, group_percentages)]
    box_labels = np.asarray(box_labels).reshape(2, 2)

    sns.heatmap(
        cm,
        annot=box_labels,
        fmt="",
        cmap="Blues",
        xticklabels=cm_labels,
        yticklabels=cm_labels,
        cbar=True,
        linewidths=1.5,
        linecolor="#e0e0e0"
    )
    plt.title("PhishGuard AI - Test Confusion Matrix", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Class", fontsize=12, labelpad=10)
    plt.ylabel("Actual True Class", fontsize=12, labelpad=10)
    plt.tight_layout()
    cm_path = os.path.join(REPORTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[+] Saved Confusion Matrix to: {cm_path}")

    # 2. ROC Curve Plot
    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color="#0284c7", lw=2.5, label=f"Random Forest (AUC = {roc_auc:.4f})")
    plt.plot([0, 1], [0, 1], color="#94a3b8", lw=1.5, linestyle="--", label="Random Classifier (AUC = 0.50)")
    plt.xlim([-0.02, 1.02])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=12)
    plt.ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=12)
    plt.title("PhishGuard AI - Receiver Operating Characteristic (ROC)", fontsize=14, fontweight="bold", pad=15)
    plt.legend(loc="lower right", fontsize=11, frameon=True)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    roc_path = os.path.join(REPORTS_DIR, "roc_curve.png")
    plt.savefig(roc_path, dpi=300)
    plt.close()
    print(f"[+] Saved ROC Curve to: {roc_path}")

    # 3. Top 15 Feature Importances Bar Chart
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1][:15]
    top_features = [FEATURE_NAMES[i] for i in sorted_idx][::-1]
    top_scores = importances[sorted_idx][::-1]

    plt.figure(figsize=(10, 7))
    bars = plt.barh(range(len(top_features)), top_scores, color="#0ea5e9", edgecolor="#0284c7", height=0.65)
    plt.yticks(range(len(top_features)), top_features, fontsize=11)
    plt.xlabel("Gini Feature Importance Score", fontsize=12, labelpad=10)
    plt.title("PhishGuard AI - Top 15 Influential URL Features", fontsize=14, fontweight="bold", pad=15)
    plt.grid(axis="x", linestyle=":", alpha=0.6)

    # Annotate bar values
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.003, bar.get_y() + bar.get_height() / 2, f"{width:.4f}",
                 va="center", ha="left", fontsize=9, color="#1e293b")

    plt.tight_layout()
    fi_path = os.path.join(REPORTS_DIR, "feature_importance.png")
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"[+] Saved Feature Importance Plot to: {fi_path}")

    # 4. Probability Score Distribution
    plt.figure(figsize=(8, 5))
    df_proba = pd.DataFrame({"Probability": y_proba, "Class": ["Phishing" if y == 1 else "Legitimate" for y in y_test]})
    sns.histplot(
        data=df_proba,
        x="Probability",
        hue="Class",
        bins=25,
        kde=True,
        palette={"Legitimate": "#10b981", "Phishing": "#ef4444"},
        element="step",
        stat="density",
        common_norm=False
    )
    plt.title("PhishGuard AI - Predicted Probability Distribution", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Probability of Phishing (P(Y=1|X))", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.tight_layout()
    dist_path = os.path.join(REPORTS_DIR, "prediction_distribution.png")
    plt.savefig(dist_path, dpi=300)
    plt.close()
    print(f"[+] Saved Probability Distribution to: {dist_path}")

    print("=" * 60)
    print("[✓] All Visualizations Generated Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    generate_evaluation_visualizations()
