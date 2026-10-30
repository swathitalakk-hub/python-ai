import csv
import random

def generate_student_data(filename="students_data.csv", num_records=250):
    random.seed(42)
    
    first_names = [
        "Aarav", "Ananya", "Rohan", "Sneha", "Aditya", "Pooja", "Rahul", "Priya",
        "Karan", "Divya", "Vikram", "Neha", "Arjun", "Tanvi", "Siddharth", "Ishita",
        "Alex", "Emma", "Liam", "Olivia", "Noah", "Ava", "Lucas", "Sophia",
        "Ethan", "Mia", "James", "Isabella", "Benjamin", "Charlotte"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Gupta", "Mehta",
        "Singh", "Chopra", "Rao", "Joshi", "Bhat", "Kulkarni", "Deshmukh",
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"
    ]
    
    departments = ["Computer Science", "Data Science", "Electronics", "Mechanical", "Information Tech"]
    
    records = []
    
    for i in range(1, num_records + 1):
        student_id = f"STU{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        
        # Base academic aptitude factor (0.4 to 1.0)
        aptitude = random.uniform(0.45, 0.98)
        
        # Study hours per week (5 to 35 hours)
        study_hours = round(max(5.0, min(35.0, aptitude * 30 + random.gauss(0, 4))), 1)
        
        # Attendance percentage (50% to 100%)
        attendance = round(max(50.0, min(100.0, (aptitude * 50 + 45) + random.gauss(0, 6))), 1)
        
        # Previous Term GPA (scale 0-10)
        previous_gpa = round(max(4.0, min(10.0, (aptitude * 6 + 3.8) + random.gauss(0, 0.4))), 2)
        
        # Assignment Score (0 to 100)
        assignments = round(max(30.0, min(100.0, (attendance * 0.4 + study_hours * 1.5 + aptitude * 20) + random.gauss(0, 5))), 1)
        
        # Midterm Exam Score (0 to 100)
        midterm = round(max(25.0, min(100.0, (study_hours * 1.6 + previous_gpa * 4.5 + aptitude * 15) + random.gauss(0, 6))), 1)
        
        # Final Exam Score (target to analyze/predict)
        # Weighted combination of midterm, assignments, attendance, study hours
        raw_final = (midterm * 0.40) + (assignments * 0.25) + (attendance * 0.15) + (study_hours * 0.6) + random.gauss(0, 4)
        final_score = round(max(20.0, min(100.0, raw_final)), 1)
        
        # Grade classification
        if final_score >= 85:
            grade = "A"
        elif final_score >= 70:
            grade = "B"
        elif final_score >= 55:
            grade = "C"
        elif final_score >= 40:
            grade = "D"
        else:
            grade = "F"
            
        # Risk assessment
        status = "Pass" if final_score >= 40 else "Fail"
        risk_level = "High" if (final_score < 45 or attendance < 65) else ("Medium" if final_score < 60 else "Low")
        
        records.append({
            "StudentID": student_id,
            "Name": name,
            "Department": dept,
            "StudyHoursWeekly": study_hours,
            "AttendancePercentage": attendance,
            "PreviousGPA": previous_gpa,
            "AssignmentScore": assignments,
            "MidtermScore": midterm,
            "FinalExamScore": final_score,
            "Grade": grade,
            "Status": status,
            "RiskLevel": risk_level
        })
        
    fieldnames = [
        "StudentID", "Name", "Department", "StudyHoursWeekly", 
        "AttendancePercentage", "PreviousGPA", "AssignmentScore", 
        "MidtermScore", "FinalExamScore", "Grade", "Status", "RiskLevel"
    ]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"[OK] Successfully generated {num_records} student records -> {filename}")
    return filename

if __name__ == "__main__":
    generate_student_data()
