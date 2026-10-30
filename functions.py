"""
functions.py
Reusable calculation and processing functions for the
Student Performance Analytics System.
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# Configuration: grading rule and pass condition (change here only)
# ----------------------------------------------------------------------
SUBJECT_COLUMNS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
REQUIRED_COLUMNS = ["Student_ID", "Name", "Department"] + SUBJECT_COLUMNS + ["Attendance"]

MAX_MARKS = 100          # maximum marks in each subject
SUBJECT_PASS_MARK = 40   # minimum marks needed in EVERY subject
MIN_ATTENDANCE = 75      # minimum attendance percentage needed

# Grading rule based on the student's average marks (highest first)
GRADE_SCALE = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (40, "E"),
]
GRADE_ORDER = [grade for _, grade in GRADE_SCALE] + ["F"]


# ----------------------------------------------------------------------
# Step 2: loading and checking data
# ----------------------------------------------------------------------
def load_data(file_path):
    """Read the student CSV into a Pandas DataFrame and validate it."""
    df = pd.read_csv(file_path)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Dataset contains missing values. Please fix students.csv.")

    marks = df[SUBJECT_COLUMNS].to_numpy()
    if (marks < 0).any() or (marks > MAX_MARKS).any():
        raise ValueError(f"Marks must be between 0 and {MAX_MARKS}.")

    if df["Student_ID"].duplicated().any():
        raise ValueError("Duplicate Student_ID found in the dataset.")

    return df


def dataset_overview(df):
    """Return basic information about the dataset as a dictionary."""
    return {
        "records": len(df),
        "columns": list(df.columns),
        "departments": sorted(df["Department"].unique()),
        "subjects": SUBJECT_COLUMNS,
    }


# ----------------------------------------------------------------------
# Step 3: processing
# ----------------------------------------------------------------------
def calculate_total_and_average(df):
    """Add Total and Average columns using NumPy on the marks matrix."""
    result = df.copy()
    marks = result[SUBJECT_COLUMNS].to_numpy()          # 2-D NumPy array
    result["Total"] = np.sum(marks, axis=1)             # row-wise total
    result["Average"] = np.round(np.mean(marks, axis=1), 2)
    return result


def assign_grade(average, passed=True):
    """Return the grade for an average mark using GRADE_SCALE.
    A student who fails the pass condition receives grade 'F'."""
    if not passed:
        return "F"
    for minimum, grade in GRADE_SCALE:      # loop through the grading rule
        if average >= minimum:
            return grade
    return "F"


def check_result(marks, attendance):
    """Decide Pass/Fail for one student.
    Pass = every subject >= SUBJECT_PASS_MARK AND attendance >= MIN_ATTENDANCE.
    Returns (result, reason)."""
    reasons = []
    for subject, mark in zip(SUBJECT_COLUMNS, marks):   # loop over subjects
        if mark < SUBJECT_PASS_MARK:
            reasons.append(f"{subject} < {SUBJECT_PASS_MARK}")
    if attendance < MIN_ATTENDANCE:
        reasons.append(f"Attendance < {MIN_ATTENDANCE}%")

    if reasons:
        return "Fail", "; ".join(reasons)
    return "Pass", "-"


def add_results_and_grades(df):
    """Add Result, Fail_Reason, Grade and Rank columns (uses loops)."""
    result = df.copy()
    results, reasons, grades = [], [], []

    for _, row in result.iterrows():                    # loop over students
        outcome, reason = check_result(row[SUBJECT_COLUMNS].to_numpy(), row["Attendance"])
        results.append(outcome)
        reasons.append(reason)
        grades.append(assign_grade(row["Average"], outcome == "Pass"))

    result["Result"] = results
    result["Fail_Reason"] = reasons
    result["Grade"] = grades
    result["Rank"] = result["Average"].rank(method="min", ascending=False).astype(int)
    return result


def process_data(df):
    """Run the complete processing pipeline and return the final DataFrame."""
    df = calculate_total_and_average(df)
    df = add_results_and_grades(df)
    return df


# ----------------------------------------------------------------------
# Step 4: analysis
# ----------------------------------------------------------------------
def class_summary(df):
    """Overall class statistics: highest, lowest, average, pass/fail counts."""
    averages = df["Average"].to_numpy()
    best = df.loc[df["Average"].idxmax()]
    worst = df.loc[df["Average"].idxmin()]
    total_students = len(df)
    passed = int((df["Result"] == "Pass").sum())

    return {
        "total_students": total_students,
        "class_average": round(float(np.mean(averages)), 2),
        "class_median": round(float(np.median(averages)), 2),
        "std_deviation": round(float(np.std(averages)), 2),
        "highest_name": best["Name"],
        "highest_average": float(best["Average"]),
        "lowest_name": worst["Name"],
        "lowest_average": float(worst["Average"]),
        "passed": passed,
        "failed": total_students - passed,
        "pass_percentage": round(passed / total_students * 100, 2),
        "average_attendance": round(float(df["Attendance"].mean()), 2),
    }


def subject_analysis(df):
    """Subject-wise statistics (one row per subject, built with a loop)."""
    rows = []
    for subject in SUBJECT_COLUMNS:
        scores = df[subject].to_numpy()
        topper = df.loc[df[subject].idxmax(), "Name"]
        passed = int(np.sum(scores >= SUBJECT_PASS_MARK))
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Std_Dev": round(float(np.std(scores)), 2),
            "Pass_%": round(passed / len(scores) * 100, 1),
            "Topper": topper,
        })
    return pd.DataFrame(rows).sort_values("Average", ascending=False).reset_index(drop=True)


def top_performers(df, n=5):
    """Top n students ranked by average marks."""
    columns = ["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade"]
    return df.sort_values("Average", ascending=False).head(n)[columns].reset_index(drop=True)


def grade_distribution(df):
    """Count of students per grade, in grade order (including grades with zero)."""
    counts = df["Grade"].value_counts().reindex(GRADE_ORDER, fill_value=0)
    return counts.rename_axis("Grade").reset_index(name="Students")


def department_analysis(df):
    """Department-wise averages and pass statistics."""
    grouped = df.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Passed=("Result", lambda s: int((s == "Pass").sum())),
    )
    grouped["Pass_%"] = grouped["Passed"] / grouped["Students"] * 100
    return grouped.round(2).sort_values("Avg_Marks", ascending=False).reset_index()


def failed_students(df):
    """Students who failed, with the reason."""
    columns = ["Student_ID", "Name", "Department", "Average", "Attendance", "Fail_Reason"]
    return df[df["Result"] == "Fail"][columns].reset_index(drop=True)


def attendance_correlation(df):
    """Pearson correlation between attendance and average marks (NumPy)."""
    return round(float(np.corrcoef(df["Attendance"], df["Average"])[0, 1]), 3)
