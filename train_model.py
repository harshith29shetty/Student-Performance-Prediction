"""
train_model.py
Full pipeline: preprocessing -> EDA -> feature engineering -> model
training -> evaluation -> saving the best models + charts for the dashboard.

Run: python train_model.py
"""

"""Train and evaluate multiple classification models for the Student Performance Prediction project."""

import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURES = [
    "previous_cgpa",
    "attendance",
    "internal_marks",
    "assignment_completion",
    "lab_marks",
    "backlogs",
    "study_hours",
]
TARGET = "performance_category"
CLASS_ORDER = ["GOOD", "AVERAGE", "AT RISK"]


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=6, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            max_depth=8,
            class_weight="balanced",
        ),
    }

    model_results = {}
    best_model_name = None
    best_model = None
    best_metrics = None

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average="weighted", zero_division=0)
        recall = recall_score(y_test, predictions, average="weighted", zero_division=0)
        f1 = f1_score(y_test, predictions, average="weighted", zero_division=0)

        model_results[name] = {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
        }

        if best_model_name is None or f1 > best_metrics["f1_score"]:
            best_model_name = name
            best_model = model
            best_metrics = model_results[name]

    cm = confusion_matrix(y_test, best_model.predict(X_test), labels=CLASS_ORDER)
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, cmap="Blues")
    plt.xticks(range(len(CLASS_ORDER)), CLASS_ORDER)
    plt.yticks(range(len(CLASS_ORDER)), CLASS_ORDER)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix — {best_model_name}")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center", color="black")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "static" / "images" / "confusion_matrix.png", dpi=120)
    plt.close()

    joblib.dump(best_model, MODEL_DIR / "student_performance_model.pkl")
    joblib.dump(FEATURES, MODEL_DIR / "feature_order.pkl")

    metrics_payload = {
        "dataset_note": "Synthetic/demo dataset generated for the mini project.",
        "best_model": best_model_name,
        "accuracy": best_metrics["accuracy"],
        "precision": best_metrics["precision"],
        "recall": best_metrics["recall"],
        "f1_score": best_metrics["f1_score"],
        "model_results": model_results,
        "class_order": CLASS_ORDER,
    }
    with open(MODEL_DIR / "metrics.json", "w") as file:
        json.dump(metrics_payload, file, indent=2)

    print("=" * 60)
    print("MODEL EVALUATION FOR STUDENT PERFORMANCE PREDICTION")
    print("=" * 60)
    for name, result in model_results.items():
        print(f"{name:22s} Accuracy={result['accuracy']:.4f} Precision={result['precision']:.4f} Recall={result['recall']:.4f} F1={result['f1_score']:.4f}")
    print(f"\nSelected model: {best_model_name}")
    print(f"Final metrics: Accuracy={best_metrics['accuracy']:.4f}, Precision={best_metrics['precision']:.4f}, Recall={best_metrics['recall']:.4f}, F1={best_metrics['f1_score']:.4f}")
    print("Saved best model and metrics in models/")


if __name__ == "__main__":
    main()
