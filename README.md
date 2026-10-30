# Student Performance Analytics System

*EWB Courses | Python with AI | Python Project Assignment*

---

## 1. Project Title

**Student Performance Analytics System**

| Detail | Value |
|---|---|
| Student Name | `<Your Name>` |
| Email | sp6520138@gmail.com |
| Course | Python with AI, EWB Courses |
| Submission Deadline | 15 October 2026 |

---

## 2. Objective

Teachers often have raw marks in a table but need quick answers: who is topping the class, which subject is weakest, how many students passed, and which students need help. Working these out by hand is slow and error-prone.

This project reads student records from a CSV file, processes them with **NumPy** and **Pandas**, and produces a clear report covering totals, averages, grades, pass/fail status, subject-wise performance, department-wise performance and top performers.

---

## 3. Technologies Used

| Tool | Used for |
|---|---|
| Python 3 | Core language: variables, data types, loops, conditions, functions |
| NumPy | Row-wise totals and averages on the marks matrix, mean/median/std/min/max, correlation |
| Pandas | Loading the CSV, DataFrame operations, sorting, filtering, groupby, ranking |

No machine learning or extra libraries are used.

---

## 4. Dataset Description

File: `students.csv`, with **20 student records** across 4 departments (Computer Science, Electronics, Mechanical, Civil), 5 students each.

| Column | Description |
|---|---|
| `Student_ID` | Unique ID (S001 to S020) |
| `Name` | Student name |
| `Department` | Computer Science / Electronics / Mechanical / Civil |
| `Maths`, `Physics`, `Chemistry`, `English`, `Computer_Science` | Marks out of 100 |
| `Attendance` | Attendance percentage |

The dataset is intentionally varied: it contains toppers, average students, and students who fail because of low marks, low attendance, or both.

---

## 5. Implementation

The project has two Python files: `main.py` (runs and displays everything) and `functions.py` (reusable logic).

**Step 1: Load and validate the data** (`load_data`)
Reads `students.csv` with `pd.read_csv()`. It checks that all required columns exist, there are no missing values, marks are between 0 and 100, and Student IDs are unique. If something is wrong, a clear error message is shown instead of a crash.

**Step 2: Total and average** (`calculate_total_and_average`)
The marks columns are converted to a 2-D NumPy array. `np.sum(axis=1)` and `np.mean(axis=1)` give each student's total and average.

**Step 3: Pass/fail** (`check_result`)
A student passes only if they score **at least 40 in every subject** and have **at least 75% attendance**. A loop checks each subject and records the reason for any failure.

**Step 4: Grading** (`assign_grade`)
A loop walks through the grading scale, based on the average marks:

| Average | Grade |
|---|---|
| 90 and above | A+ |
| 80 to 89.99 | A |
| 70 to 79.99 | B |
| 60 to 69.99 | C |
| 50 to 59.99 | D |
| 40 to 49.99 | E |
| Below 40, or failed the pass condition | F |

**Step 5: Ranking** (`add_results_and_grades`)
Students are ranked by average marks using Pandas `rank()`.

**Step 6: Analysis**
`class_summary`, `subject_analysis`, `top_performers`, `grade_distribution`, `department_analysis`, `failed_students` and `attendance_correlation` answer the practical questions from the assignment.

**Step 7: Output**
`main.py` prints nine clearly labelled sections and saves the full processed table to `student_results.csv`.

All thresholds (pass mark, minimum attendance, grade scale) are defined once at the top of `functions.py`, so the rules can be changed in one place.

---

## 6. Key Features

- CSV loading with data validation and friendly error handling
- Total and average marks per student (NumPy)
- Grade assignment using a clearly defined grading rule
- Pass/fail detection with the exact reason for failure
- Student ranking
- Highest, lowest, average, median and standard deviation of performance
- Subject-wise analysis (average, highest, lowest, pass %, subject topper)
- Top 5 performers
- Grade distribution with a text bar chart
- Department-wise comparison
- Attendance vs marks correlation (NumPy `corrcoef`)
- Results exported to `student_results.csv`

---

## 7. Output / Screenshots

Full output is in [`sample_output.txt`](sample_output.txt). Key results:

**Overall class summary**

```
Total students        : 20
Class average         : 70.89
Highest average       : 94.2  (Meera Nair)
Lowest average        : 45.6  (Rahul Das)
Students passed       : 17
Students failed       : 3
Pass percentage       : 85.0%
Attendance vs marks correlation: 0.973
```

**Subject-wise performance**

```
         Subject  Average  Highest  Lowest  Std_Dev  Pass_%      Topper
         English    75.05       94      55    11.60   100.0 Pooja Joshi
Computer_Science    73.20       99      42    16.76   100.0  Meera Nair
           Maths    69.30       95      33    17.67    95.0  Meera Nair
       Chemistry    68.85       92      44    15.51   100.0  Meera Nair
         Physics    68.05       97      38    16.12    95.0  Meera Nair
```

**Top 5 performers**

```
 Rank Student_ID           Name       Department  Total  Average Grade
    1       S008     Meera Nair Computer Science    471     94.2    A+
    2       S016    Pooja Joshi            Civil    450     90.0    A+
    3       S004    Ananya Iyer      Electronics    446     89.2     A
    4       S001   Aarav Sharma Computer Science    440     88.0     A
    5       S012 Kavya Krishnan Computer Science    435     87.0     A
```

> You can add screenshots of your own terminal run here, for example `![Output](screenshots/output.png)`.

---

## 8. Final Outcome

The system runs without errors and answers the questions from the assignment:

| Question | Answer |
|---|---|
| Which student has the highest average? | Meera Nair (94.2) |
| Which subject has the best average? | English (75.05) |
| Which subject is weakest? | Physics (68.05) |
| How many students passed? | 17 of 20 (85%) |
| What is the overall class average? | 70.89 |
| Best department? | Computer Science (average 82.56) |

Three students failed (Karthik Naidu, Rahul Das, Lakshmi Prasad). In every case low attendance was a reason, and the data shows a strong link between attendance and marks (correlation 0.973).

The results were cross-checked with a separate plain-Python calculation, and every total, average, grade and pass/fail result matched.

---

## 9. Challenges & Learning

| Challenge | How it was solved |
|---|---|
| Deciding a fair pass condition | Used a two-part rule (40+ in every subject and 75%+ attendance) and stored the reason for failure so results are explainable |
| A student with a good average but low attendance still fails | Grade is set to `F` for any student who fails the pass condition, so grade and result never contradict each other |
| Keeping the code reusable | Moved all logic into functions and kept the settings at the top of `functions.py` |
| Running from any folder | Used `os.path` so `main.py` finds `students.csv` no matter where it is launched |
| Bad or missing data | Added validation in `load_data` with clear error messages |

**What I learned:** how NumPy handles row-wise calculations on a whole marks matrix, how Pandas `groupby`, `rank` and `agg` simplify analysis, how loops and functions keep code readable, and how to test results against an independent calculation.

---

## 10. GitHub Repository

**Repository link:** `https://github.com/<your-username>/student-performance-analytics`

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/student-performance-analytics.git
cd student-performance-analytics

# 2. Install the requirements
pip install -r requirements.txt

# 3. Run the project
python main.py
```

## Project Structure

```
student-performance-analytics/
├── main.py               # Runs the project and displays the analysis
├── functions.py          # Reusable calculation and processing functions
├── students.csv          # Dataset (20 student records)
├── student_results.csv   # Processed results (generated by main.py)
├── sample_output.txt     # Full program output
├── requirements.txt      # numpy, pandas
├── .gitignore
└── README.md             # Project documentation
```
