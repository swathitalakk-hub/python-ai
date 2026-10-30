"""
main.py
Student Performance Analytics System
Runs the full project: load data -> process -> analyse -> display results.

Usage:  python main.py
"""

import os
import pandas as pd

import functions as fn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "students.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "student_results.csv")

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def print_header(title):
    """Print a clear section heading."""
    print("\n" + "=" * 80)
    print(title.upper())
    print("=" * 80)


def main():
    print("=" * 80)
    print("STUDENT PERFORMANCE ANALYTICS SYSTEM".center(80))
    print("EWB Courses | Python with AI".center(80))
    print("=" * 80)

    # ---------------- Step 2: Read the data ----------------
    try:
        raw_df = fn.load_data(DATA_FILE)
    except (FileNotFoundError, ValueError) as error:
        print(f"\nERROR: {error}")
        return

    overview = fn.dataset_overview(raw_df)
    print_header("1. Dataset Overview")
    print(f"Number of records : {overview['records']}")
    print(f"Columns           : {', '.join(overview['columns'])}")
    print(f"Departments       : {', '.join(overview['departments'])}")
    print("\nFirst 5 records:")
    print(raw_df.head().to_string(index=False))

    # ---------------- Step 3: Process the data ----------------
    df = fn.process_data(raw_df)

    print_header("2. Rules Used")
    print("Grading rule (based on average marks):")
    for minimum, grade in fn.GRADE_SCALE:
        print(f"   Average >= {minimum:<3} -> Grade {grade}")
    print("   Failed students                -> Grade F")
    print(f"Pass condition: marks >= {fn.SUBJECT_PASS_MARK} in EVERY subject "
          f"AND attendance >= {fn.MIN_ATTENDANCE}%")

    print_header("3. Student Report Card (sorted by rank)")
    report_columns = ["Rank", "Student_ID", "Name", "Department", "Total",
                      "Average", "Attendance", "Grade", "Result"]
    print(df.sort_values("Rank")[report_columns].to_string(index=False))

    # ---------------- Step 4: Analysis ----------------
    summary = fn.class_summary(df)
    print_header("4. Overall Class Summary")
    print(f"Total students        : {summary['total_students']}")
    print(f"Class average         : {summary['class_average']}")
    print(f"Class median          : {summary['class_median']}")
    print(f"Standard deviation    : {summary['std_deviation']}")
    print(f"Highest average       : {summary['highest_average']}  ({summary['highest_name']})")
    print(f"Lowest average        : {summary['lowest_average']}  ({summary['lowest_name']})")
    print(f"Students passed       : {summary['passed']}")
    print(f"Students failed       : {summary['failed']}")
    print(f"Pass percentage       : {summary['pass_percentage']}%")
    print(f"Average attendance    : {summary['average_attendance']}%")
    print(f"Attendance vs marks correlation: {fn.attendance_correlation(df)}")

    print_header("5. Subject-wise Performance")
    subject_df = fn.subject_analysis(df)
    print(subject_df.to_string(index=False))
    print(f"\nBest subject  : {subject_df.iloc[0]['Subject']} (average {subject_df.iloc[0]['Average']})")
    print(f"Weakest subject: {subject_df.iloc[-1]['Subject']} (average {subject_df.iloc[-1]['Average']})")

    print_header("6. Top 5 Performers")
    print(fn.top_performers(df, 5).to_string(index=False))

    print_header("7. Grade Distribution")
    grade_df = fn.grade_distribution(df)
    for _, row in grade_df.iterrows():
        print(f"   {row['Grade']:<3} | {'#' * int(row['Students']):<10} {row['Students']}")

    print_header("8. Department-wise Performance")
    print(fn.department_analysis(df).to_string(index=False))

    print_header("9. Students Who Failed")
    failed_df = fn.failed_students(df)
    if failed_df.empty:
        print("No student failed.")
    else:
        print(failed_df.to_string(index=False))

    # ---------------- Step 5: Save and finish ----------------
    df.sort_values("Rank").to_csv(OUTPUT_FILE, index=False)
    print_header("Done")
    print(f"Full results saved to: {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
