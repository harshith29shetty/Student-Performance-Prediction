# Product Requirements Document (PRD)

## 1. Product Name
Student Performance Prediction System

## 2. Product Goal
Create a simple, teacher-focused mini project that allows a teacher to enter student academic details, run a prediction using a machine learning model, and review the student's performance category and risk indicators.

The system must be easy to understand, small in scope, and suitable for an MCA mini project demonstration.

## 3. Target User
Primary user:
- Teacher

No student login or admin role is required.

## 4. Core Features

### 4.1 Teacher Dashboard
The teacher should be able to view a simple dashboard showing:
- Total number of students
- Count of students in GOOD category
- Count of students in AVERAGE category
- Count of students in AT RISK category

This dashboard should remain simple and not become a college management system.

### 4.2 Add Student
The teacher should be able to add a student record with the following data:
- Student ID
- Student Name
- Semester
- Previous Semester CGPA
- Attendance Percentage
- Internal Marks Percentage
- Assignment Completion Percentage
- Lab Marks Percentage
- Number of Backlogs
- Average Study Hours per Day

### 4.3 Student List
The teacher should be able to view a list of saved students with basic summary columns such as:
- Student ID
- Name
- Semester
- CGPA
- Attendance
- Prediction status

### 4.4 Student Details
The teacher should be able to:
- View a student's saved details
- Update student information
- Delete a student record

### 4.5 Prediction Result
When the teacher predicts a student's performance, the system must display:
- Predicted category: GOOD / AVERAGE / AT RISK
- Risk Level: Low Risk / Medium Risk / High Risk
- Areas to Improve

The result should be easy to read and suitable for teacher review.

## 5. Machine Learning Requirements
The project must include a synthetic/demo dataset containing the required academic fields:
- Previous CGPA
- Attendance
- Internal Marks
- Assignment Completion %
- Lab Marks %
- Backlogs
- Study Hours
- Performance Category

The application must compare a small number of suitable models and use the best-performing model for prediction.

The evaluated metrics must include:
- Accuracy
- Precision
- Recall
- F1-score

The dataset must be clearly identified as synthetic/demo data.

## 6. Functional Flow
1. Teacher opens the dashboard.
2. Teacher adds a student record.
3. Teacher views the student list.
4. Teacher selects a student.
5. Teacher runs prediction.
6. Model predicts GOOD / AVERAGE / AT RISK.
7. System shows risk level and improvement areas.
8. Teacher reviews the output.

## 7. Output Example
The result page should show a format similar to:

--------------------------------
Student Performance Result
--------------------------------

Name: Rahul
Semester: 3

Previous CGPA: 7.2
Attendance: 78%
Internal Marks: 68%
Assignment: 80%
Lab Marks: 72%
Backlogs: 0
Study Hours: 3

--------------------------------

Predicted Performance:
GOOD

Risk Level:
LOW

Areas to Improve:
None / Minor improvement recommended
--------------------------------

## 8. Non-Functional Requirements
- Simple and clean UI
- Easy to understand for a mini project demo
- Focused only on three core areas:
  1. Student data
  2. ML prediction
  3. Teacher view
- No unnecessary features like payments, attendance management, admin screens, authentication, or large analytics dashboards

## 9. Technology Requirements
- Python
- Flask web framework
- pandas and NumPy for data handling
- scikit-learn for ML models
- HTML/CSS templates for UI
- joblib for model persistence

## 10. Scope Boundaries
The following are out of scope:
- Multiple user roles
- Student login
- Admin login
- Email or message alerts
- Payment integration
- Mobile app
- Large reporting system
- College management module
- Chatbot or advanced AI features

## 11. Acceptance Criteria 
The project is acceptable if all of the following are true:
- Teacher can add student details.
- Teacher can view saved student records.
- Teacher can update and delete student records.
- Teacher can run a prediction.
- System shows one of GOOD / AVERAGE / AT RISK.
- System shows Low Risk / Medium Risk / High Risk.
- System shows improvement areas for review.
- Simple dashboard displays category totals.
- ML model is trained using synthetic/demo data and evaluated using required metrics.
- Application remains small and understandable.

## 12. Success Measurement
The project is successful if it can be run locally, demonstrated in a short presentation, and clearly communicates the complete flow from student entry to prediction result without unnecessary complexity.
