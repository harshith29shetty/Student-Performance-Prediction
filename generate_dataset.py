"""Generate the synthetic training dataset for the Student Performance Prediction mini project."""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 500

previous_cgpa = rng.uniform(4.0, 9.5, N).round(2)
attendance = rng.uniform(45, 98, N).round(2)
internal_marks = rng.uniform(35, 95, N).round(2)
assignment_completion = rng.uniform(40, 100, N).round(2)
lab_marks = rng.uniform(35, 98, N).round(2)
backlogs = rng.integers(0, 5, N)
study_hours = rng.uniform(1.0, 8.0, N).round(2)

score = (
    0.28 * previous_cgpa * 10
    + 0.20 * attendance
    + 0.18 * internal_marks
    + 0.14 * assignment_completion
    + 0.12 * lab_marks
    + 0.12 * study_hours * 10
    - 0.11 * backlogs * 10
)
score = score + rng.normal(0, 8, N)
score = np.clip(score, 0, 100).round(2)

performance = []
for value in score:
    if value >= 70:
        performance.append("GOOD")
    elif value >= 52:
        performance.append("AVERAGE")
    else:
        performance.append("AT RISK")

student_data = pd.DataFrame(
    {
        "student_id": [f"S{1001 + i}" for i in range(N)],
        "semester": rng.integers(1, 8, N),
        "previous_cgpa": previous_cgpa,
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_completion": assignment_completion,
        "lab_marks": lab_marks,
        "backlogs": backlogs,
        "study_hours": study_hours,
        "performance_category": performance,
    }
)

# Keep the synthetic dataset clearly marked as demo data for the project.
student_data.to_csv("data/student_data.csv", index=False)
print(f"Generated {len(student_data)} synthetic demo records in data/student_data.csv")
print(student_data.head(5).to_string(index=False))
print("\nLabel counts:")
print(student_data["performance_category"].value_counts().to_string())
