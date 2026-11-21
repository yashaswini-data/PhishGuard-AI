"""
PhishGuard AI - Data Preprocessing & Pipeline Module
====================================================
Handles dataset loading, inspection, missing value verification,
duplicate removal, stratified train/test splitting, and feature preparation.
"""

import os
from typing import Tuple, Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def load_and_inspect_dataset(csv_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Loads dataset from CSV, inspects shapes, nulls, duplicates, and returns
    the dataframe along with a summary diagnostic report.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    initial_shape = df.shape

    # 1. Inspect missing values
    missing_counts = df.isnull().sum()
    total_missing = int(missing_counts.sum())

    # 2. Inspect and handle duplicates
    duplicate_count = int(df.duplicated().sum())
    if duplicate_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)

    clean_shape = df.shape

    # 3. Label balance check
    if "label" in df.columns:
        label_distribution = df["label"].value_counts(normalize=True).to_dict()
        label_counts = df["label"].value_counts().to_dict()
    else:
        label_distribution = {}
        label_counts = {}

    diagnostics = {
        "initial_rows": initial_shape[0],
        "initial_columns": initial_shape[1],
        "cleaned_rows": clean_shape[0],
        "cleaned_columns": clean_shape[1],
        "duplicates_removed": duplicate_count,
        "total_missing_values": total_missing,
        "label_counts": label_counts,
        "label_distribution": label_distribution,
    }

    return df, diagnostics


def prepare_train_test_split(
    df: pd.DataFrame,
    target_column: str = "label",
    test_size: float = 0.20,
    random_state: int = RANDOM_STATE
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits features and target into stratified train and test sets.
    Stratification ensures both splits have the exact same class ratio,
    preventing sampling bias and data leakage.
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' missing from DataFrame columns.")

    X = df.drop(columns=[target_column])
    y = df[target_column].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "dataset_30features_11055.csv")
    df, stats = load_and_inspect_dataset(dataset_path)
    print("Dataset Diagnostics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    X_tr, X_te, y_tr, y_te = prepare_train_test_split(df)
    print(f"\nTrain set: X={X_tr.shape}, y={y_tr.shape}")
    print(f"Test set:  X={X_te.shape}, y={y_te.shape}")
