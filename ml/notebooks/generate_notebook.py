import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# PhishGuard AI: Comprehensive EDA & Machine Learning Pipeline\n",
                "**Project:** Intelligent Phishing URL Detection & Risk Analysis System  \n",
                "**Model:** Random Forest Classifier  \n",
                "**Features:** 30 Lexical, Structural, Domain, and Statistical URL Features  \n",
                "**Dataset Size:** 11,055 records (Stratified Balanced Binary Classification)\n",
                "\n",
                "---\n",
                "## Table of Contents\n",
                "1. **Project Overview & Threat Model**\n",
                "2. **Dataset Inspection & Verification**\n",
                "3. **Exploratory Data Analysis (EDA)**\n",
                "4. **Feature Engineering & 30-Feature Categorization**\n",
                "5. **Data Preprocessing & Train-Test Splitting (Preventing Leakage)**\n",
                "6. **Random Forest Classifier Training & Hyperparameter Tuning**\n",
                "7. **Model Evaluation (Accuracy, Precision, Recall, F1, ROC-AUC, CM)**\n",
                "8. **Feature Importance & Interpretability Analysis**\n",
                "9. **Model Serialization with Joblib for Backend Serving**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os, sys, json, math, re\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.model_selection import train_test_split, GridSearchCV\n",
                "from sklearn.ensemble import RandomForestClassifier\n",
                "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve\n",
                "import joblib\n",
                "\n",
                "# Set plotting styles\n",
                "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                "print('Libraries successfully imported!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Dataset Loading & Diagnostics\n",
                "We load the 11,055-record feature matrix extracted from verified phishing and legitimate URLs."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "outputs": [],
            "source": [
                "dataset_path = '../dataset/dataset_30features_11055.csv'\n",
                "df = pd.read_csv(dataset_path)\n",
                "print('Dataset Shape:', df.shape)\n",
                "print('\\nFirst 5 rows:')\n",
                "print(df.head())\n",
                "print('\\nMissing values:', df.isnull().sum().sum())\n",
                "print('\\nClass balance:')\n",
                "print(df['label'].value_counts(normalize=True))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Exploratory Data Analysis (EDA)\n",
                "Let us analyze key feature distributions between Legitimate (0) and Phishing (1) URLs."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
                "sns.boxplot(ax=axes[0, 0], x='label', y='url_length', data=df, palette=['#10b981', '#ef4444'])\n",
                "axes[0, 0].set_title('URL Length by Class')\n",
                "\n",
                "sns.countplot(ax=axes[0, 1], x='is_https', hue='label', data=df, palette=['#10b981', '#ef4444'])\n",
                "axes[0, 1].set_title('HTTPS Usage by Class')\n",
                "\n",
                "sns.boxplot(ax=axes[1, 0], x='label', y='char_entropy', data=df, palette=['#10b981', '#ef4444'])\n",
                "axes[1, 0].set_title('Character Shannon Entropy by Class')\n",
                "\n",
                "sns.countplot(ax=axes[1, 1], x='has_ip_address', hue='label', data=df, palette=['#10b981', '#ef4444'])\n",
                "axes[1, 1].set_title('IP Address as Hostname by Class')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Train-Test Split (Preventing Data Leakage)\n",
                "We split 80% for training and 20% for testing with stratification to preserve class balance."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 4,
            "metadata": {},
            "outputs": [],
            "source": [
                "df_clean = df.drop_duplicates().reset_index(drop=True)\n",
                "X = df_clean.drop(columns=['label'])\n",
                "y = df_clean['label']\n",
                "\n",
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)\n",
                "print(f'Train set: {X_train.shape}, Test set: {X_test.shape}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Random Forest Classifier & Hyperparameter Tuning"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 5,
            "metadata": {},
            "outputs": [],
            "source": [
                "rf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=2, min_samples_leaf=1, random_state=42, n_jobs=-1)\n",
                "rf.fit(X_train, y_train)\n",
                "print('Model training complete!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Evaluation on Unseen Test Data"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 6,
            "metadata": {},
            "outputs": [],
            "source": [
                "y_pred = rf.predict(X_test)\n",
                "y_proba = rf.predict_proba(X_test)[:, 1]\n",
                "\n",
                "print('Accuracy: ', accuracy_score(y_test, y_pred))\n",
                "print('Precision:', precision_score(y_test, y_pred))\n",
                "print('Recall:   ', recall_score(y_test, y_pred))\n",
                "print('F1-Score: ', f1_score(y_test, y_pred))\n",
                "print('ROC-AUC:  ', roc_auc_score(y_test, y_proba))\n",
                "print('\\nClassification Report:\\n', classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Feature Importance Ranking"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {},
            "outputs": [],
            "source": [
                "importances = rf.feature_importances_\n",
                "feat_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values('Importance', ascending=False)\n",
                "plt.figure(figsize=(10, 6))\n",
                "sns.barplot(x='Importance', y='Feature', data=feat_df.head(10), palette='Blues_r')\n",
                "plt.title('Top 10 Most Important Features')\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("PhishGuard-AI/ml/notebooks/EDA_and_Model_Training.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated successfully!")
