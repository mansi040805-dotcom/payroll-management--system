"""
main.py - Application Entry Point

This is the starting point of the Payroll Management System.
It loads sample data (if no data exists yet) and launches the GUI.

Usage:
    python main.py
"""

import tkinter as tk
from file_manager import FileManager
from gui import PayrollApp


# ============================================================
# Sample Data Creation
# ============================================================

def create_sample_data():
    """
    Create sample data for demonstration purposes.

    This function runs when the application starts. It only creates
    sample data if no employees exist yet (first run).

    Sample data includes:
    - 2 salaried employees and 2 hourly employees
    - Attendance records for October 2026 (22 working days)
    - Compensation components for each employee
    - Leave records demonstrating different scenarios
    """
    file_manager = FileManager()

    # Only create sample data if no employees exist
    existing_employees = file_manager.read_data(FileManager.EMPLOYEES_FILE)
    if existing_employees:
        return  # Data already exists, don't overwrite

    print("First run detected. Loading sample data...")

    # ---- Sample Employees ----
    sample_employees = [
        {
            "employee_id": "EMP001",
            "name": "Rahul Sharma",
            "email": "rahul.sharma@techcorp.com",
            "contact": "9876543210",
            "department": "IT",
            "designation": "Software Developer",
            "joining_date": "2024-01-15",
            "employment_type": "Salaried",
            "basic_salary": 50000,
            "status": "Active"
        },
        {
            "employee_id": "EMP002",
            "name": "Priya Patel",
            "email": "priya.patel@techcorp.com",
            "contact": "9876543211",
            "department": "Finance",
            "designation": "Senior Accountant",
            "joining_date": "2023-06-01",
            "employment_type": "Salaried",
            "basic_salary": 60000,
            "status": "Active"
        },
        {
            "employee_id": "EMP003",
            "name": "Amit Kumar",
            "email": "amit.kumar@techcorp.com",
            "contact": "9876543212",
            "department": "Operations",
            "designation": "Technician",
            "joining_date": "2024-03-10",
            "employment_type": "Hourly",
            "hourly_rate": 300,
            "status": "Active"
        },
        {
            "employee_id": "EMP004",
            "name": "Neha Singh",
            "email": "neha.singh@techcorp.com",
            "contact": "9876543213",
            "department": "Support",
            "designation": "Help Desk Executive",
            "joining_date": "2025-01-20",
            "employment_type": "Hourly",
            "hourly_rate": 250,
            "status": "Active"
        }
    ]

    # ---- Sample Attendance for October 2026 ----
    # October 2026 has 22 weekdays (working days):
    working_days = [
        "2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06",
        "2026-10-07", "2026-10-08", "2026-10-09", "2026-10-12",
        "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16",
        "2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22",
        "2026-10-23", "2026-10-26", "2026-10-27", "2026-10-28",
        "2026-10-29", "2026-10-30"
    ]

    attendance_records = []

    # EMP001 - Rahul: Full attendance, 2 days with overtime
    for day in working_days:
        if day in ["2026-10-29", "2026-10-30"]:
            # Overtime days: worked 10 hours (2 hours extra)
            attendance_records.append({
                "employee_id": "EMP001", "date": day,
                "check_in": "09:00", "check_out": "20:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 10.0
            })
        else:
            # Normal days: worked standard 8 hours
            attendance_records.append({
                "employee_id": "EMP001", "date": day,
                "check_in": "09:00", "check_out": "18:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 8.0
            })

    # EMP002 - Priya: 18 present, 2 paid leave, 1 unpaid leave, 1 absent
    for day in working_days:
        if day in ["2026-10-15", "2026-10-16"]:
            # Paid leave days
            attendance_records.append({
                "employee_id": "EMP002", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Paid Leave",
                "total_working_hours": 0
            })
        elif day == "2026-10-22":
            # Unpaid leave
            attendance_records.append({
                "employee_id": "EMP002", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Unpaid Leave",
                "total_working_hours": 0
            })
        elif day == "2026-10-29":
            # Absent
            attendance_records.append({
                "employee_id": "EMP002", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Absent",
                "total_working_hours": 0
            })
        else:
            # Normal present day
            attendance_records.append({
                "employee_id": "EMP002", "date": day,
                "check_in": "09:00", "check_out": "18:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 8.0
            })

    # EMP003 - Amit: 20 present (5 with overtime), 2 absent
    for day in working_days:
        if day in ["2026-10-08", "2026-10-09"]:
            # Absent days
            attendance_records.append({
                "employee_id": "EMP003", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Absent",
                "total_working_hours": 0
            })
        elif day in ["2026-10-26", "2026-10-27", "2026-10-28",
                      "2026-10-29", "2026-10-30"]:
            # Overtime days: worked 10 hours (2 hours extra)
            attendance_records.append({
                "employee_id": "EMP003", "date": day,
                "check_in": "08:00", "check_out": "19:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 10.0
            })
        else:
            # Normal days
            attendance_records.append({
                "employee_id": "EMP003", "date": day,
                "check_in": "08:00", "check_out": "17:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 8.0
            })

    # EMP004 - Neha: 17 present, 2 half-day, 1 absent, 2 holiday
    for day in working_days:
        if day in ["2026-10-01", "2026-10-02"]:
            # Holiday
            attendance_records.append({
                "employee_id": "EMP004", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Holiday",
                "total_working_hours": 0
            })
        elif day in ["2026-10-20", "2026-10-21"]:
            # Half-day: worked 4 hours
            attendance_records.append({
                "employee_id": "EMP004", "date": day,
                "check_in": "09:00", "check_out": "13:30",
                "break_duration": 0.5, "status": "Half-day",
                "total_working_hours": 4.0
            })
        elif day == "2026-10-22":
            # Absent
            attendance_records.append({
                "employee_id": "EMP004", "date": day,
                "check_in": "", "check_out": "",
                "break_duration": 0, "status": "Absent",
                "total_working_hours": 0
            })
        else:
            # Normal present day
            attendance_records.append({
                "employee_id": "EMP004", "date": day,
                "check_in": "09:00", "check_out": "18:00",
                "break_duration": 1, "status": "Present",
                "total_working_hours": 8.0
            })

    # ---- Sample Compensation ----
    sample_compensation = [
        {
            "employee_id": "EMP001",
            "hra": 5000,
            "transport_allowance": 2000,
            "medical_allowance": 1500,
            "other_allowances": 0,
            "performance_bonus": 0,
            "other_deductions": 0
        },
        {
            "employee_id": "EMP002",
            "hra": 8000,
            "transport_allowance": 3000,
            "medical_allowance": 2000,
            "other_allowances": 1000,
            "performance_bonus": 5000,
            "other_deductions": 0
        },
        {
            "employee_id": "EMP003",
            "hra": 0,
            "transport_allowance": 1500,
            "medical_allowance": 0,
            "other_allowances": 0,
            "performance_bonus": 0,
            "other_deductions": 0
        },
        {
            "employee_id": "EMP004",
            "hra": 0,
            "transport_allowance": 1000,
            "medical_allowance": 0,
            "other_allowances": 0,
            "performance_bonus": 0,
            "other_deductions": 500
        }
    ]

    # ---- Sample Leaves ----
    sample_leaves = [
        {
            "leave_id": "LV001",
            "employee_id": "EMP002",
            "start_date": "2026-10-15",
            "end_date": "2026-10-16",
            "leave_type": "Paid Leave",
            "reason": "Family function",
            "status": "Approved"
        },
        {
            "leave_id": "LV002",
            "employee_id": "EMP002",
            "start_date": "2026-10-22",
            "end_date": "2026-10-22",
            "leave_type": "Unpaid Leave",
            "reason": "Personal work",
            "status": "Approved"
        },
        {
            "leave_id": "LV003",
            "employee_id": "EMP004",
            "start_date": "2026-10-22",
            "end_date": "2026-10-22",
            "leave_type": "Unpaid Leave",
            "reason": "Doctor appointment",
            "status": "Rejected"
        }
    ]

    # ---- Save all sample data ----
    file_manager.write_data(FileManager.EMPLOYEES_FILE, sample_employees)
    file_manager.write_data(FileManager.ATTENDANCE_FILE, attendance_records)
    file_manager.write_data(FileManager.COMPENSATION_FILE, sample_compensation)
    file_manager.write_data(FileManager.LEAVES_FILE, sample_leaves)
    file_manager.write_data(FileManager.PAYROLL_FILE, [])
    file_manager.write_data(FileManager.PAYMENTS_FILE, [])

    print("Sample data loaded successfully!")
    print("  - 4 employees (2 salaried, 2 hourly)")
    print("  - Attendance records for October 2026")
    print("  - Compensation components")
    print("  - Leave records")


# ============================================================
# Application Entry Point
# ============================================================

def main():
    """Start the Payroll Management System application."""
    # Load sample data on first run
    create_sample_data()

    # Create the main Tkinter window
    root = tk.Tk()

    # Create and run the application
    app = PayrollApp(root)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
