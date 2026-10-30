# PROJECT DOCUMENTATION REPORT

# Student Performance Analytics System
**EWB Courses | Python with AI Project Assignment**

---

## 1. Project Overview & Metadata

| Field | Detail |
| :--- | :--- |
| **Project Title** | Student Performance Analytics System |
| **Student Name** | Swathi Talak |
| **Email Address** | swathitalak28@gmail.com |
| **Course** | Python with AI (EWB Courses) |
| **Programming Language** | Python 3.13 |
| **Primary Libraries** | NumPy, Pandas |
| **GitHub Repository** | [https://github.com/swathitalakk-hub/python-ai](https://github.com/swathitalakk-hub/python-ai) |
| **Operating System** | Windows 11 / Cross-Platform |

---

## 2. Abstract & Problem Statement

### 2.1 The Problem
In modern academic institutions, faculty members frequently manage large volumes of raw examination and attendance data across multiple courses and departments. Evaluating performance manually using conventional spreadsheets or hand calculations is time-consuming, prone to human calculation errors, and fails to provide instantaneous diagnostic insights such as:
- Which subject exhibits the lowest average score and requires syllabus review?
- How strongly does attendance correlate with student examination performance?
- What are the precise root causes behind individual student failures (e.g., subject-specific score deficit vs. attendance shortfall)?
- How do different academic departments compare in student pass percentage?

### 2.2 The Solution
The **Student Performance Analytics System** is a robust, modular Python analytics application powered by **NumPy** and **Pandas**. It automates the entire analytical lifecycle:
1. Validating and ingesting tabular student records from CSV.
2. Performing vectorized numerical computation of scores, totals, and averages.
3. Enforcing rigorous, transparent academic grading and pass/fail rules.
4. Generating rank orders and multi-dimensional academic statistics.
5. Exporting processed results to structured CSV tables and clean terminal reports.

---

## 3. System Architecture & Workflow

```
+-------------------------------------------------------------+
|                      students.csv                           |
|       (Student_ID, Name, Department, Marks, Attendance)     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                   functions.load_data()                     |
|  - Schema Verification                                      |
|  - Missing Value & Range Checks (0-100)                      |
|  - ID Uniqueness Validation                                 |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|               Numerical & Logic Processing                  |
|  - calculate_total_and_average() [NumPy 2D Array]           |
|  - check_result() [Marks >= 40 & Attendance >= 75%]         |
|  - assign_grade() [A+, A, B, C, D, E, F]                    |
|  - add_results_and_grades() [Pandas Ranking]                |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     Analytics Engine                        |
|  - class_summary()          - subject_analysis()            |
|  - department_analysis()    - top_performers()              |
|  - grade_distribution()     - attendance_correlation()      |
|  - failed_students()                                        |
+-------------------------------------------------------------+
                              |
               +--------------+--------------+
               |                             |
               v                             v
+------------------------------+  +---------------------------+
|    Console Dashboard Output  |  |    student_results.csv    |
|   (Formatted Sections 1-9)   |  |   (Exported Full Table)   |
+------------------------------+  +---------------------------+
```

---

## 4. Dataset Specification

The system processes `students.csv`, comprising **20 student records** equally partitioned across four academic departments: **Computer Science**, **Electronics**, **Mechanical**, and **Civil** (5 students per department).

### Schema Definition:
| Column | Data Type | Constraints / Description |
| :--- | :--- | :--- |
| `Student_ID` | String | Unique identifier format (`S001` - `S020`) |
| `Name` | String | Full student name |
| `Department` | Categorical | Academic department |
| `Maths` | Integer | Marks obtained out of 100 ($0 \le \text{Marks} \le 100$) |
| `Physics` | Integer | Marks obtained out of 100 ($0 \le \text{Marks} \le 100$) |
| `Chemistry` | Integer | Marks obtained out of 100 ($0 \le \text{Marks} \le 100$) |
| `English` | Integer | Marks obtained out of 100 ($0 \le \text{Marks} \le 100$) |
| `Computer_Science` | Integer | Marks obtained out of 100 ($0 \le \text{Marks} \le 100$) |
| `Attendance` | Integer | Attendance percentage ($0 \le \text{Attendance} \le 100$) |

---

## 5. Mathematical Formulations & Evaluation Criteria

### 5.1 Total Marks & Average Calculation
For each student $i$ across $n = 5$ subjects:

$$\text{Total}_i = \sum_{j=1}^{n} M_{i,j}$$

$$\text{Average}_i = \frac{\text{Total}_i}{n} = \frac{1}{n} \sum_{j=1}^{n} M_{i,j}$$

Computed efficiently using NumPy 2D array matrix operations (`axis=1`).

### 5.2 Pass / Fail Condition
A student is declared **Pass** if and only if both conditions are satisfied:
1. **Academic Competence**: $\min(M_{i,1}, M_{i,2}, \dots, M_{i,n}) \ge 40$
2. **Attendance Compliance**: $\text{Attendance}_i \ge 75\%$

If either condition fails, the result is **Fail**, and the specific cause is logged (e.g., `"Physics < 40; Attendance < 75%"`).

### 5.3 Grading Scale
Grading is derived from average marks, subject to passing status:

| Average Score Range | Letter Grade | Condition |
| :--- | :---: | :--- |
| $\text{Average} \ge 90$ | **A+** | Must Pass |
| $80 \le \text{Average} < 90$ | **A** | Must Pass |
| $70 \le \text{Average} < 80$ | **B** | Must Pass |
| $60 \le \text{Average} < 70$ | **C** | Must Pass |
| $50 \le \text{Average} < 60$ | **D** | Must Pass |
| $40 \le \text{Average} < 50$ | **E** | Must Pass |
| $\text{Average} < 40$ or Failed | **F** | Failed Result Override |

*Design Decision*: Any student who fails the pass condition receives Grade **F**, preventing contradictory records (e.g., failing yet holding an A grade).

### 5.4 Pearson Correlation Coefficient
Measures the linear relationship between student attendance and average marks:

$$r = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum (X_i - \bar{X})^2 \sum (Y_i - \bar{Y})^2}}$$

Implemented via `np.corrcoef()`.

---

## 6. Modular Implementation Details

The project source code is organized into two primary Python scripts:

### 6.1 `functions.py` (Core Logic Library)
- `load_data(file_path)`: Ingests the CSV file using Pandas; checks schema completeness, non-null values, integer/float ranges, and unique primary keys (`Student_ID`).
- `calculate_total_and_average(df)`: Converts subject columns into NumPy 2D array and computes totals and averages using vectorized vector operations.
- `check_result(row)`: Evaluates whether a student meets the minimum marks in every individual subject ($\ge 40$) and meets the minimum attendance threshold ($\ge 75\%$).
- `assign_grade(row)`: Applies the progressive grading scale and overrides the grade to 'F' if the student failed.
- `add_results_and_grades(df)`: Appends calculated columns and ranks students descending by average using `pd.Series.rank(method='min')`.
- `class_summary(df)`: Generates cohort-level aggregations (mean, median, standard deviation, pass rate).
- `subject_analysis(df)`: Computes subject-specific statistics (average, highest, lowest, std dev, pass percentage, subject topper).
- `department_analysis(df)`: Groups records by department to analyze inter-departmental performance metrics.
- `attendance_correlation(df)`: Computes Pearson correlation between attendance percentage and average score.
- `failed_students(df)`: Filters and extracts at-risk/failed students alongside their diagnosed failure reasons.
- `save_results(df, file_path)`: Exports the processed DataFrame to CSV.

### 6.2 `main.py` (Execution Controller)
Coordinates the workflow, handles potential file/schema exceptions gracefully, and formats output into nine structured console sections.

---

## 7. Key Findings & Analytics Results

### 7.1 Overall Cohort Summary
- **Total Students Evaluated**: 20
- **Overall Class Average**: 70.89 / 100
- **Class Median**: 72.50
- **Standard Deviation**: 15.01
- **Overall Pass Percentage**: **85.0%** (17 Passed, 3 Failed)
- **Average Attendance**: 85.80%
- **Attendance vs. Marks Correlation**: **0.973** (Extremely strong positive correlation)

### 7.2 Top 5 Academic Achievers
| Rank | Student ID | Name | Department | Total Marks | Average | Grade |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | `S008` | Meera Nair | Computer Science | 471 / 500 | 94.20% | A+ |
| **2** | `S016` | Pooja Joshi | Civil | 450 / 500 | 90.00% | A+ |
| **3** | `S004` | Ananya Iyer | Electronics | 446 / 500 | 89.20% | A |
| **4** | `S001` | Aarav Sharma | Computer Science | 440 / 500 | 88.00% | A |
| **5** | `S012` | Kavya Krishnan | Computer Science | 435 / 500 | 87.00% | A |

### 7.3 Subject-Wise Benchmark Comparison
| Subject | Average | Highest | Lowest | Std Dev | Pass Rate | Subject Topper |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **English** | **75.05** | 94 | 55 | 11.60 | 100.0% | Pooja Joshi (94) |
| **Computer Science** | **73.20** | 99 | 42 | 16.76 | 100.0% | Meera Nair (99) |
| **Maths** | **69.30** | 95 | 33 | 17.67 | 95.0% | Meera Nair (95) |
| **Chemistry** | **68.85** | 92 | 44 | 15.51 | 100.0% | Meera Nair (92) |
| **Physics** | **68.05** | 97 | 38 | 16.12 | 95.0% | Meera Nair (97) |

- **Strongest Subject**: English (Avg: 75.05)
- **Most Challenging Subject**: Physics (Avg: 68.05, 1 failure)

### 7.4 Department-Wise Performance Breakdown
| Department | Cohort Size | Average Marks | Average Attendance | Passed | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Computer Science** | 5 | **82.56** | 92.2% | 5 | **100.0%** |
| **Electronics** | 5 | **71.20** | 86.2% | 4 | **80.0%** |
| **Civil** | 5 | **66.92** | 83.2% | 4 | **80.0%** |
| **Mechanical** | 5 | **62.88** | 81.6% | 4 | **80.0%** |

### 7.5 Failure Diagnostics & Root Causes
| Student ID | Student Name | Department | Average | Attendance | Specific Failure Diagnosis |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `S005` | Karthik Naidu | Mechanical | 48.6 | 70% | Physics < 40 (38); Attendance < 75% |
| `S013` | Rahul Das | Civil | 45.6 | 68% | Maths < 40 (33); Attendance < 75% |
| `S018` | Lakshmi Prasad | Electronics | 52.4 | 73% | Attendance < 75% (Shortfall of 2%) |

*Key Takeaway*: In 100% of failed cases, inadequate attendance ($< 75\%$) was a contributing factor, substantiating the high correlation metric ($r = 0.973$).

---

## 8. Verification & Validation Testing

The integrity of calculations was systematically verified:
1. **Mathematical Validation**: Sample totals, means, and standard deviations were cross-verified against baseline manual calculations.
2. **Boundary Condition Checks**: Evaluated edge cases (e.g., student scoring $\ge 50$ average but attendance $< 75\%$) to verify that grade properly falls to 'F'.
3. **Data Ingestion Fault-Tolerance**: Tested handling for missing files, invalid ranges, and duplicate IDs with informative error messaging.

---

## 9. Execution Instructions

### Prerequisites
- Python 3.8 or higher installed
- `pip` package manager

### Steps
```bash
# 1. Clone repository
git clone https://github.com/swathitalakk-hub/python-ai.git
cd python-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute analytics system
python main.py
```

### Generated Files
Upon execution, the system creates:
- `student_results.csv`: Complete processed dataset with totals, averages, grades, ranks, results, and fail reasons.

---

## 10. Conclusion & Future Enhancements

The **Student Performance Analytics System** successfully fulfills all project requirements, providing automated, error-free analysis and actionable pedagogical insights.

### Potential Future Enhancements:
1. **Predictive Modeling**: Incorporating supervised regression/classification (e.g., Scikit-learn) to forecast final exam results from midterm assessments.
2. **Automated Report Card PDF Generation**: Generating individual personalized PDF report cards for students and guardians.
3. **Interactive Web Dashboard**: Hosting a web interface (Flask/Streamlit) for real-time instructor queries and visualizations.
