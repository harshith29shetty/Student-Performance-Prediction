# Student Performance Prediction System Architecture

## 1. System Overview

The Student Performance Prediction System is a small Flask-based web application for teachers. It stores student academic records, uses a trained machine learning classification model to predict performance, and presents the prediction with a simple risk indicator and improvement areas.

The system intentionally supports only the planned mini-project scope:

- Student academic data management
- Machine learning prediction
- Teacher dashboard and result viewing

No student login, admin role, authentication, notifications, or college-management features are included.

## 2. High-Level Architecture

```text
┌──────────────────────┐
│       Teacher        │
└──────────┬───────────┘
           │ Browser
           ▼
┌──────────────────────┐
│ Flask Web Application │
│       app.py          │
└───────┬───────┬──────┘
        │       │
        │       └─────────────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐             ┌──────────────────┐
│ Student Records│             │ Trained ML Model │
│ CSV Storage    │             │ Joblib Artifact  │
└───────────────┘             └──────────────────┘
        ▲                             ▲
        │                             │
        └──────────────┬──────────────┘
                       │
              ┌────────┴────────┐
              │ Training Pipeline│
              │ generate_dataset │
              │ train_model.py   │
              └──────────────────┘
```

## 3. Main Components

### 3.1 Teacher Interface

The teacher uses the browser interface to:

1. Open the dashboard.
2. Add a student.
3. View saved students.
4. Open student details.
5. Update or delete a student record.
6. Run a performance prediction.
7. Review the prediction result, risk level, and areas to improve.

The interface is implemented with Jinja2 templates and Bootstrap-compatible HTML/CSS.

### 3.2 Flask Application

The Flask application is implemented in `app.py`. It is responsible for:

- Serving the dashboard and student pages
- Receiving student form submissions
- Reading and writing student records
- Loading the trained model
- Preparing model input features
- Running predictions
- Calculating risk levels
- Identifying academic areas that may need improvement

### 3.3 Student Record Storage

Student records are stored in:

```text
data/student_records.csv
```

The record contains:

| Field | Description |
|---|---|
| `student_id` | Unique student identifier |
| `student_name` | Student name |
| `semester` | Current semester |
| `previous_cgpa` | Previous semester CGPA |
| `attendance` | Attendance percentage |
| `internal_marks` | Internal marks percentage |
| `assignment_completion` | Assignment completion percentage |
| `lab_marks` | Lab marks percentage |
| `backlogs` | Number of backlogs |
| `study_hours` | Average study hours per day |
| `prediction` | Latest predicted category |

CSV storage is used because the project is intentionally small and suitable for a mini-project demonstration.

### 3.4 Machine Learning Pipeline

The machine learning workflow has two scripts:

- `generate_dataset.py`: creates reproducible synthetic/demo student data.
- `train_model.py`: trains, evaluates, compares, and saves classification models.

The input features are:

```text
previous_cgpa
attendance
internal_marks
assignment_completion
lab_marks
backlogs
study_hours
```

The target classes are:

```text
GOOD
AVERAGE
AT RISK
```

The training script compares:

- Logistic Regression
- Decision Tree
- Random Forest

The model with the best weighted F1-score is saved as the final model.

## 4. Model Artifacts

The training process creates the following files:

```text
models/
├── student_performance_model.pkl
├── feature_order.pkl
└── metrics.json
```

### `student_performance_model.pkl`

The selected scikit-learn classification model used by the Flask application.

### `feature_order.pkl`

The exact feature order required when constructing prediction input data. This prevents the web application from sending model features in an incorrect order.

### `metrics.json`

Stores:

- Selected model name
- Accuracy
- Precision
- Recall
- F1-score
- Results for all compared models
- Dataset note identifying the data as synthetic/demo data

## 5. Application Pages and Routes

| Page | Route | Purpose |
|---|---|---|
| Teacher Dashboard | `/` | Shows total students and GOOD, AVERAGE, and AT RISK counts |
| Add Student | `/students/new` | Saves a new student record |
| Student List | `/students` | Displays all saved students |
| Student Details | `/students/<student_id>` | Shows, updates, or deletes one student |
| Prediction Result | `/students/<student_id>/predict` | Runs and displays the ML prediction |

## 6. Prediction Flow

```text
Teacher opens a student record
              │
              ▼
Teacher selects "Predict Performance"
              │
              ▼
app.py reads the student's academic fields
              │
              ▼
Fields are arranged using feature_order.pkl
              │
              ▼
student_performance_model.pkl predicts a category
              │
              ▼
Application calculates:
  - Risk level
  - Confidence
  - Areas to improve
              │
              ▼
Prediction is saved to the student record
              │
              ▼
Teacher views the Prediction Result page
```

## 7. Risk and Improvement Indicators

The prediction category is mapped to a simple risk level:

| Prediction | Risk Level |
|---|---|
| `GOOD` | Low Risk |
| `AVERAGE` | Medium Risk |
| `AT RISK` | High Risk |

The application checks academic thresholds to identify possible improvement areas, such as:

- Attendance
- Internal marks
- Assignment completion
- Lab marks
- Study hours
- Backlogs
- Previous CGPA

These are indicators for teacher review and are not definitive judgments about a student.

## 8. End-to-End Project Flow

```text
1. Generate synthetic/demo dataset
   └── python generate_dataset.py

2. Train and evaluate classification models
   └── python train_model.py

3. Start the Flask application
   └── python app.py

4. Teacher adds or selects a student

5. Teacher runs prediction

6. Application loads the trained model

7. Application displays:
   ├── GOOD / AVERAGE / AT RISK
   ├── Low / Medium / High Risk
   └── Areas to Improve
```

## 9. Directory Structure

```text
Mini project/
├── app.py
├── generate_dataset.py
├── train_model.py
├── requirements.txt
├── README.md
├── architecture.md
├── data/
│   ├── student_data.csv
│   └── student_records.csv
├── models/
│   ├── student_performance_model.pkl
│   ├── feature_order.pkl
│   └── metrics.json
├── static/
│   ├── style.css
│   └── images/
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── add_student.html
    ├── students.html
    ├── student_detail.html
    ├── result.html
    └── not_found.html
```

## 10. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, Jinja2 templates, Bootstrap CDN, CSS |
| Backend | Python, Flask |
| Data processing | pandas, NumPy |
| Machine learning | scikit-learn |
| Model persistence | joblib |
| Record storage | CSV files |
| Evaluation visualization | Matplotlib |

## 11. Limitations and Scope

- The training dataset is synthetic/demo data and should not be treated as real institutional evidence.
- CSV storage is appropriate for this small project but is not intended for concurrent production use.
- Predictions support teacher review and early identification of possible risk; they do not replace teacher judgment.
- The application has no authentication because the project plan requires only one teacher user and a simple demonstration workflow.
