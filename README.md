<<<<<<< HEAD
# Student Performance Prediction System

This project follows the MCA mini project plan for a teacher-focused student performance prediction system.

## Main features

- Teacher dashboard with total students and category counts
- Add student record form
- Student list with view and prediction actions
- Student details page with update and delete options
- Prediction result page showing:
  - Predicted performance: GOOD / AVERAGE / AT RISK
  - Risk level: Low Risk / Medium Risk / High Risk
  - Areas to improve

## ML model

- Synthetic/demo academic dataset stored in `data/student_data.csv`
- Models compared: Logistic Regression, Decision Tree, Random Forest
- Evaluation metrics: Accuracy, Precision, Recall, F1-score
- Best model is saved in `models/student_performance_model.pkl`

## Project flow

Teacher -> Add Student -> View Student List -> Predict Performance -> Result

## Run the project

```bash
pip install -r requirements.txt
python generate_dataset.py
python train_model.py
python app.py
```

Open http://127.0.0.1:5000 in the browser.

## Notes

- The dataset is synthetic/demo data as required for an academic mini project.
- The app is intentionally simple and limited to the plan scope.
=======
# Student-Performance-Prediction
This project follows the MCA mini project plan for a teacher-focused student performance prediction system.
>>>>>>> eb1dc2e8b14e7ec2eba9fb459412e4878de32568
