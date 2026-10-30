"""
Student Performance Analytics Engine
Comprehensive statistical analysis, predictive machine learning, and intervention engine.
"""

import json
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score


class StudentAnalyticsEngine:
    def __init__(self, data_path="students_data.csv"):
        self.data_path = data_path
        self.df = None
        self.regression_model = None
        self.risk_classifier = None
        self.feature_columns = ["StudyHoursWeekly", "AttendancePercentage", "PreviousGPA", "AssignmentScore", "MidtermScore"]
        self.target_regression = "FinalExamScore"
        self.metrics = {}
        
    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file '{self.data_path}' not found. Please run generate_dataset.py first.")
        self.df = pd.read_csv(self.data_path)
        return self.df

    def compute_summary_statistics(self):
        """Calculates descriptive analytics across student cohorts."""
        if self.df is None:
            self.load_data()
            
        total_students = len(self.df)
        passed_count = int((self.df["Status"] == "Pass").sum())
        failed_count = int((self.df["Status"] == "Fail").sum())
        pass_rate = round((passed_count / total_students) * 100, 2)
        
        grade_dist = self.df["Grade"].value_counts().to_dict()
        dept_dist = self.df.groupby("Department")["FinalExamScore"].agg(["count", "mean", "std", "max", "min"]).round(2).to_dict(orient="index")
        
        stats = {
            "total_students": total_students,
            "pass_rate": pass_rate,
            "passed_students": passed_count,
            "failed_students": failed_count,
            "average_final_score": round(float(self.df["FinalExamScore"].mean()), 2),
            "median_final_score": round(float(self.df["FinalExamScore"].median()), 2),
            "std_final_score": round(float(self.df["FinalExamScore"].std()), 2),
            "highest_score": round(float(self.df["FinalExamScore"].max()), 2),
            "lowest_score": round(float(self.df["FinalExamScore"].min()), 2),
            "average_attendance": round(float(self.df["AttendancePercentage"].mean()), 2),
            "average_study_hours": round(float(self.df["StudyHoursWeekly"].mean()), 2),
            "grade_distribution": grade_dist,
            "department_breakdown": dept_dist,
            "risk_distribution": self.df["RiskLevel"].value_counts().to_dict()
        }
        return stats

    def compute_correlations(self):
        """Calculates correlation matrix between input metrics and outcomes."""
        numeric_cols = self.feature_columns + ["FinalExamScore"]
        corr_matrix = self.df[numeric_cols].corr().round(3).to_dict()
        return corr_matrix

    def train_predictive_models(self):
        """Trains ML models for Score Prediction (Regression) and Risk Detection (Classification)."""
        if self.df is None:
            self.load_data()
            
        X = self.df[self.feature_columns]
        y_reg = self.df[self.target_regression]
        
        # Binary target: 1 = At Risk / Needs Intervention (Score < 50 or Attendance < 65), 0 = Safe
        y_risk = ((self.df["FinalExamScore"] < 50) | (self.df["AttendancePercentage"] < 65)).astype(int)
        
        X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
        _, _, y_train_risk, y_test_risk = train_test_split(X, y_risk, test_size=0.2, random_state=42)
        
        # 1. Regression Model (Random Forest & Linear Regression)
        self.regression_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.regression_model.fit(X_train, y_train_reg)
        y_pred_reg = self.regression_model.predict(X_test)
        
        r2 = round(r2_score(y_test_reg, y_pred_reg), 4)
        mse = round(mean_squared_error(y_test_reg, y_pred_reg), 4)
        rmse = round(float(np.sqrt(mse)), 4)
        
        # Feature Importance
        feature_importances = dict(zip(self.feature_columns, [round(float(x), 4) for x in self.regression_model.feature_importances_]))
        
        # 2. Risk Classifier (Random Forest Classifier)
        self.risk_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_classifier.fit(X_train, y_train_risk)
        y_pred_risk = self.risk_classifier.predict(X_test)
        
        acc = round(accuracy_score(y_test_risk, y_pred_risk) * 100, 2)
        prec = round(precision_score(y_test_risk, y_pred_risk, zero_division=0) * 100, 2)
        rec = round(recall_score(y_test_risk, y_pred_risk, zero_division=0) * 100, 2)
        f1 = round(f1_score(y_test_risk, y_pred_risk, zero_division=0) * 100, 2)
        
        self.metrics = {
            "regression": {
                "r2_score": r2,
                "rmse": rmse,
                "mse": mse,
                "feature_importances": feature_importances
            },
            "classification": {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1_score": f1
            }
        }
        return self.metrics

    def predict_student(self, study_hours, attendance, prev_gpa, assignment_score, midterm_score):
        """Predicts expected final score and risk warning for a specific student profile."""
        if self.regression_model is None or self.risk_classifier is None:
            self.train_predictive_models()
            
        features = pd.DataFrame([[study_hours, attendance, prev_gpa, assignment_score, midterm_score]], columns=self.feature_columns)
        predicted_score = round(float(self.regression_model.predict(features)[0]), 1)
        predicted_score = max(0.0, min(100.0, predicted_score))
        
        risk_prob = round(float(self.risk_classifier.predict_proba(features)[0][1]) * 100, 1)
        
        if predicted_score >= 85:
            predicted_grade = "A"
        elif predicted_score >= 70:
            predicted_grade = "B"
        elif predicted_score >= 55:
            predicted_grade = "C"
        elif predicted_score >= 40:
            predicted_grade = "D"
        else:
            predicted_grade = "F"
            
        recommendations = []
        if attendance < 75:
            recommendations.append("Attendance is critical (<75%). Target at least 80% to avoid academic warning.")
        if study_hours < 15:
            recommendations.append("Study hours are below recommended baseline. Increase to 18-20 hrs/week.")
        if midterm_score < 50:
            recommendations.append("Midterm score was deficient. Recommend enrolling in peer tutoring program.")
        if not recommendations:
            recommendations.append("Student on track for distinction. Encourage advanced project participation.")
            
        return {
            "predicted_score": predicted_score,
            "predicted_grade": predicted_grade,
            "risk_probability_percent": risk_prob,
            "is_at_risk": bool(risk_prob > 40),
            "recommendations": recommendations
        }

    def generate_full_report(self, export_path="analysis_results.json"):
        """Generates comprehensive analytics snapshot for CLI and web visualization."""
        summary = self.compute_summary_statistics()
        correlations = self.compute_correlations()
        metrics = self.train_predictive_models()
        
        # Identify top 5 performers and top 5 critical at-risk students
        top_performers = self.df.sort_values(by="FinalExamScore", ascending=False).head(5)[
            ["StudentID", "Name", "Department", "FinalExamScore", "Grade"]
        ].to_dict(orient="records")
        
        at_risk_cohort = self.df[self.df["RiskLevel"] == "High"].sort_values(by="FinalExamScore").head(10)[
            ["StudentID", "Name", "Department", "AttendancePercentage", "StudyHoursWeekly", "MidtermScore", "FinalExamScore"]
        ].to_dict(orient="records")
        
        report = {
            "summary": summary,
            "correlations": correlations,
            "model_metrics": metrics,
            "top_performers": top_performers,
            "at_risk_cohort": at_risk_cohort
        }
        
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        return report


if __name__ == "__main__":
    engine = StudentAnalyticsEngine()
    engine.load_data()
    report = engine.generate_full_report()
    print("[OK] Analytics Engine run complete. Report exported to analysis_results.json")
    print(f"Total Students: {report['summary']['total_students']}")
    print(f"Pass Rate: {report['summary']['pass_rate']}%")
    print(f"Model R2 Score: {report['model_metrics']['regression']['r2_score']}")
    print(f"Model Accuracy: {report['model_metrics']['classification']['accuracy']}%")
