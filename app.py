"""
app.py
Flask web app for the Student Performance Prediction mini project.

Routes:
  /                     Input form (name + attendance, marks, study hours, etc.)
  /predict              Handles the manual-entry form POST, shows results
  /students             Searchable directory of students already in the dataset
  /student/<student_id> Looks up one specific student and predicts for them
  /dashboard            Shows EDA charts, feature importance, and model comparison

Run: python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RECORDS_PATH = DATA_DIR / "student_records.csv"
MODEL_PATH = BASE_DIR / "models" / "student_performance_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "feature_order.pkl"
METRICS_PATH = BASE_DIR / "models" / "metrics.json"

FEATURES = [
    "previous_cgpa",
    "attendance",
    "internal_marks",
    "assignment_completion",
    "lab_marks",
    "backlogs",
    "study_hours",
]

RISK_LEVEL = {
    "GOOD": "Low Risk",
    "AVERAGE": "Medium Risk",
    "AT RISK": "High Risk",
}


def ensure_records_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not RECORDS_PATH.exists():
        df = pd.DataFrame(
            columns=[
                "student_id",
                "student_name",
                "semester",
                "previous_cgpa",
                "attendance",
                "internal_marks",
                "assignment_completion",
                "lab_marks",
                "backlogs",
                "study_hours",
                "prediction",
            ]
        )
        df.to_csv(RECORDS_PATH, index=False)


def load_records():
    ensure_records_file()
    df = pd.read_csv(RECORDS_PATH)
    if df.empty:
        return pd.DataFrame(columns=[
            "student_id",
            "student_name",
            "semester",
            "previous_cgpa",
            "attendance",
            "internal_marks",
            "assignment_completion",
            "lab_marks",
            "backlogs",
            "study_hours",
            "prediction",
        ])
    return df


with open(METRICS_PATH) as file:
    model_metrics = json.load(file)

model = joblib.load(MODEL_PATH)
feature_order = joblib.load(FEATURES_PATH)


def build_prediction(student_row):
    input_values = {feature: float(student_row.get(feature, 0)) for feature in feature_order}
    input_frame = pd.DataFrame([input_values], columns=feature_order)
    prediction = model.predict(input_frame)[0]
    probabilities = model.predict_proba(input_frame)[0]
    confidence = float(max(probabilities) * 100)
    risk_level = RISK_LEVEL.get(prediction, "Medium Risk")
    areas = identify_areas(student_row, prediction)

    return {
        "performance": prediction,
        "risk_level": risk_level,
        "confidence": round(confidence, 1),
        "areas": areas,
    }


def identify_areas(student_row, prediction):
    issues = []
    if float(student_row.get("attendance", 0)) < 75:
        issues.append("Attendance")
    if float(student_row.get("internal_marks", 0)) < 60:
        issues.append("Internal Marks")
    if float(student_row.get("assignment_completion", 0)) < 70:
        issues.append("Assignments")
    if float(student_row.get("lab_marks", 0)) < 70:
        issues.append("Lab Marks")
    if float(student_row.get("study_hours", 0)) < 3:
        issues.append("Study Hours")
    if int(student_row.get("backlogs", 0)) > 0:
        issues.append("Backlogs")
    if float(student_row.get("previous_cgpa", 0)) < 6.0:
        issues.append("Previous CGPA")

    if not issues:
        return ["None / Minor improvement recommended"] if prediction == "GOOD" else ["Minor improvement recommended"]
    return issues


@app.route("/")
def dashboard():
    records = load_records()
    total_students = len(records)
    distribution = {label: int((records["prediction"] == label).sum()) if "prediction" in records.columns else 0 for label in ["GOOD", "AVERAGE", "AT RISK"]}
    return render_template(
        "dashboard.html",
        total_students=total_students,
        distribution=distribution,
        metrics=model_metrics,
    )


@app.route("/students/new", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        if not student_id:
            return render_template("add_student.html", error="Student ID is required.")

        records = load_records()
        if student_id in records["student_id"].astype(str).tolist():
            return render_template("add_student.html", error="This student ID already exists.")

        student_row = {
            "student_id": student_id,
            "student_name": request.form.get("student_name", "").strip(),
            "semester": request.form.get("semester", "").strip(),
            "previous_cgpa": request.form.get("previous_cgpa", "0"),
            "attendance": request.form.get("attendance", "0"),
            "internal_marks": request.form.get("internal_marks", "0"),
            "assignment_completion": request.form.get("assignment_completion", "0"),
            "lab_marks": request.form.get("lab_marks", "0"),
            "backlogs": request.form.get("backlogs", "0"),
            "study_hours": request.form.get("study_hours", "0"),
            "prediction": "",
        }

        new_df = pd.DataFrame([student_row])
        records = pd.concat([records, new_df], ignore_index=True)
        records.to_csv(RECORDS_PATH, index=False)
        return redirect(url_for("student_detail", student_id=student_id))

    return render_template("add_student.html")


@app.route("/students")
def students():
    records = load_records()
    return render_template("students.html", students=records.to_dict(orient="records"))


@app.route("/students/<student_id>", methods=["GET", "POST"])
def student_detail(student_id):
    records = load_records()
    student = records[records["student_id"].astype(str) == student_id]
    if student.empty:
        abort(404)

    row = student.iloc[0].to_dict()
    if request.method == "POST":
        updated = {
            "student_id": student_id,
            "student_name": request.form.get("student_name", row.get("student_name", "")).strip(),
            "semester": request.form.get("semester", row.get("semester", "")),
            "previous_cgpa": request.form.get("previous_cgpa", row.get("previous_cgpa", 0)),
            "attendance": request.form.get("attendance", row.get("attendance", 0)),
            "internal_marks": request.form.get("internal_marks", row.get("internal_marks", 0)),
            "assignment_completion": request.form.get("assignment_completion", row.get("assignment_completion", 0)),
            "lab_marks": request.form.get("lab_marks", row.get("lab_marks", 0)),
            "backlogs": request.form.get("backlogs", row.get("backlogs", 0)),
            "study_hours": request.form.get("study_hours", row.get("study_hours", 0)),
            "prediction": row.get("prediction", ""),
        }
        records.loc[records["student_id"].astype(str) == student_id] = updated
        records.to_csv(RECORDS_PATH, index=False)
        return redirect(url_for("student_detail", student_id=student_id))

    return render_template("student_detail.html", student=row)


@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    records = load_records()
    records = records[records["student_id"].astype(str) != student_id]
    records.to_csv(RECORDS_PATH, index=False)
    return redirect(url_for("students"))


@app.route("/students/<student_id>/predict")
def predict_student(student_id):
    records = load_records()
    student = records[records["student_id"].astype(str) == student_id]
    if student.empty:
        abort(404)

    row = student.iloc[0].to_dict()
    prediction = build_prediction(row)
    row["prediction"] = prediction["performance"]
    records.loc[records["student_id"].astype(str) == student_id, "prediction"] = prediction["performance"]
    records.to_csv(RECORDS_PATH, index=False)

    return render_template("result.html", student=row, prediction=prediction)


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
