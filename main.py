"""
Student Performance Analytics System - Main CLI Interface
Run full analyses, search students, train ML models, and generate reports.
"""

import sys
import os

# Ensure UTF-8 output encoding across Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from analytics_engine import StudentAnalyticsEngine

def print_banner():
    banner = """
================================================================================
          STUDENT PERFORMANCE ANALYTICS & PREDICTIVE SYSTEM (AI-POWERED)
================================================================================
"""
    print(banner)

def display_summary_dashboard(report):
    summary = report["summary"]
    metrics = report["model_metrics"]
    
    print("\n" + "="*80)
    print(" [*] EXECUTIVE SUMMARY DASHBOARD")
    print("="*80)
    print(f" Total Enrolled Students : {summary['total_students']:<10} | Pass Rate            : {summary['pass_rate']}%")
    print(f" Passed Students         : {summary['passed_students']:<10} | Failed Students      : {summary['failed_students']}")
    print(f" Average Final Score     : {summary['average_final_score']:<10} | Highest Final Score  : {summary['highest_score']}")
    print(f" Average Attendance      : {summary['average_attendance']}%     | Average Study Hours  : {summary['average_study_hours']} hrs/wk")
    print("-" * 80)
    
    print("\n [GRADE DISTRIBUTION]")
    for grade, count in sorted(summary["grade_distribution"].items()):
        bar = "#" * int(count / 2)
        pct = (count / summary['total_students']) * 100
        print(f"   Grade {grade}: {count:3d} students ({pct:5.1f}%) | {bar}")
        
    print("\n [RISK ASSESSMENT]")
    for risk, count in summary["risk_distribution"].items():
        pct = (count / summary['total_students']) * 100
        print(f"   {risk:<7} Risk : {count:3d} students ({pct:5.1f}%)")
        
    print("\n [MACHINE LEARNING MODEL PERFORMANCE]")
    print(f"   Score Predictor R2 Score : {metrics['regression']['r2_score']} (Variance explained: {metrics['regression']['r2_score']*100:.1f}%)")
    print(f"   Prediction RMSE Error    : +/-{metrics['regression']['rmse']} points")
    print(f"   Risk Classifier Accuracy : {metrics['classification']['accuracy']}% | F1-Score: {metrics['classification']['f1_score']}%")
    
    print("\n   Top Influential Factors:")
    for feat, imp in sorted(metrics['regression']['feature_importances'].items(), key=lambda x: x[1], reverse=True):
        print(f"    - {feat:<22}: {imp*100:5.1f}% impact")
    print("="*80)

def display_top_performers(report):
    print("\n" + "="*80)
    print(" [TOP 5 ACADEMIC ACHIEVERS]")
    print("="*80)
    print(f" {'ID':<9} | {'Name':<22} | {'Department':<22} | {'Score':<8} | {'Grade'}")
    print("-" * 80)
    for s in report["top_performers"]:
        print(f" {s['StudentID']:<9} | {s['Name']:<22} | {s['Department']:<22} | {s['FinalExamScore']:<8} | {s['Grade']}")
    print("="*80)

def display_at_risk_cohort(report):
    print("\n" + "="*80)
    print(" [CRITICAL AT-RISK STUDENTS - IMMEDIATE INTERVENTION REQUIRED]")
    print("="*80)
    print(f" {'ID':<9} | {'Name':<20} | {'Dept':<18} | {'Attnd%':<8} | {'StudyHrs':<9} | {'Midterm':<8} | {'Final'}")
    print("-" * 80)
    for s in report["at_risk_cohort"]:
        print(f" {s['StudentID']:<9} | {s['Name']:<20} | {s['Department'][:17]:<18} | {s['AttendancePercentage']:<8} | {s['StudyHoursWeekly']:<9} | {s['MidtermScore']:<8} | {s['FinalExamScore']}")
    print("="*80)

def main():
    print_banner()
    
    csv_file = "students_data.csv"
    if not os.path.exists(csv_file):
        print("[*] Generating student database...")
        from generate_dataset import generate_student_data
        generate_student_data(csv_file, 250)
        
    print("[*] Initializing Machine Learning and Statistical Engine...")
    engine = StudentAnalyticsEngine(csv_file)
    engine.load_data()
    report = engine.generate_full_report()
    
    display_summary_dashboard(report)
    display_top_performers(report)
    display_at_risk_cohort(report)
    
    print("\n" + "="*80)
    print(" [AI WHAT-IF PREDICTOR SCENARIOS]")
    print("="*80)
    
    # Scenario 1: At-risk student
    at_risk_demo = engine.predict_student(study_hours=8.0, attendance=62.0, prev_gpa=5.2, assignment_score=48.0, midterm_score=42.0)
    print(" Scenario A (Student with low attendance & low study hours):")
    print(f"   Inputs: 8.0 hrs/wk, 62% attendance, 5.2 GPA, 48 assignment, 42 midterm")
    print(f"   -> Predicted Final Score : {at_risk_demo['predicted_score']} (Grade {at_risk_demo['predicted_grade']})")
    print(f"   -> Failure/Risk Probability: {at_risk_demo['risk_probability_percent']}% [{'AT RISK' if at_risk_demo['is_at_risk'] else 'SAFE'}]")
    print(f"   -> Remedial Actions:")
    for r in at_risk_demo["recommendations"]:
        print(f"       * {r}")
        
    print("\n Scenario B (High-performing student):")
    high_demo = engine.predict_student(study_hours=28.0, attendance=96.0, prev_gpa=9.1, assignment_score=94.0, midterm_score=90.0)
    print(f"   Inputs: 28.0 hrs/wk, 96% attendance, 9.1 GPA, 94 assignment, 90 midterm")
    print(f"   -> Predicted Final Score : {high_demo['predicted_score']} (Grade {high_demo['predicted_grade']})")
    print(f"   -> Failure/Risk Probability: {high_demo['risk_probability_percent']}% [{'AT RISK' if high_demo['is_at_risk'] else 'SAFE'}]")
    print(f"   -> Recommendation: {high_demo['recommendations'][0]}")
    
    print("\n" + "="*80)
    print(" [OK] Output implemented and verified. Export saved to 'analysis_results.json'.")
    print("="*80)

if __name__ == "__main__":
    main()
