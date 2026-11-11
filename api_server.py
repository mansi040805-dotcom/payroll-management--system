"""
api_server.py - REST API Backend for PaySphere Payroll Management System

Connects the modern React frontend to the existing Python OOP domain logic
(FileManager, PayrollManager, Employee subclasses, Attendance, Leave).

Usage:
    python api_server.py
"""

import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

# Import existing backend modules
from file_manager import FileManager, FileError
from payroll import (
    PayrollManager,
    DuplicatePayrollError,
    PayrollError,
    PayrollNotFinalizedError
)
from employee import (
    SalariedEmployee,
    HourlyEmployee,
    create_employee_from_dict,
    EmployeeError,
    InvalidSalaryError,
    InvalidEmployeeDataError
)
from records import (
    Attendance,
    Leave,
    DuplicateAttendanceError,
    InvalidAttendanceError,
    InvalidLeaveError
)
from main import create_sample_data

# Ensure data is initialized
create_sample_data()

# Locate frontend build directory if it exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

app = Flask(__name__, static_folder=FRONTEND_DIST if os.path.exists(FRONTEND_DIST) else None)

file_manager = FileManager()
payroll_manager = PayrollManager(file_manager)


# ============================================================
# CORS Handling
# ============================================================
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.route("/api/<path:dummy>", methods=["OPTIONS"])
def handle_options(dummy):
    return "", 200


# ============================================================
# 1. Health & Dashboard Stats
# ============================================================
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "service": "PaySphere Python OOP Backend",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    try:
        employees = file_manager.read_data(FileManager.EMPLOYEES_FILE)
        active_employees = [e for e in employees if e.get("status") == "Active"]
        active_count = len(active_employees)
        total_count = len(employees)

        payrolls = file_manager.read_data(FileManager.PAYROLL_FILE)
        latest_payroll_net = 0.0
        latest_period = "None"
        if payrolls:
            latest_month = payrolls[-1].get("month")
            latest_year = payrolls[-1].get("year")
            latest_period = f"{latest_month:02d}/{latest_year}"
            month_payrolls = [
                p for p in payrolls
                if p.get("month") == latest_month and p.get("year") == latest_year
            ]
            latest_payroll_net = sum(
                p.get("salary_breakdown", {}).get("net_salary", 0)
                for p in month_payrolls
            )

        pending_payments = payroll_manager.get_pending_payments()
        completed_payments = payroll_manager.get_completed_payments()

        # Department breakdown
        dept_counts = {}
        for e in employees:
            dept = e.get("department", "Other")
            dept_counts[dept] = dept_counts.get(dept, 0) + 1

        # Type breakdown
        salaried_count = sum(1 for e in employees if e.get("employment_type") == "Salaried")
        hourly_count = sum(1 for e in employees if e.get("employment_type") == "Hourly")

        # Total attendance entries
        attendance = file_manager.read_data(FileManager.ATTENDANCE_FILE)
        leaves = file_manager.read_data(FileManager.LEAVES_FILE)

        return jsonify({
            "total_employees": total_count,
            "active_employees": active_count,
            "latest_payroll_net": latest_payroll_net,
            "latest_payroll_period": latest_period,
            "pending_payments_count": len(pending_payments),
            "completed_payments_count": len(completed_payments),
            "department_breakdown": dept_counts,
            "employment_type_breakdown": {
                "Salaried": salaried_count,
                "Hourly": hourly_count
            },
            "total_attendance_logs": len(attendance),
            "total_leave_requests": len(leaves)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 2. Employee Management Endpoints
# ============================================================
@app.route("/api/employees", methods=["GET"])
def get_employees():
    try:
        employees = file_manager.read_data(FileManager.EMPLOYEES_FILE)
        search = request.args.get("search", "").strip().lower()
        dept = request.args.get("department", "").strip()

        if search:
            employees = [
                e for e in employees
                if search in e.get("employee_id", "").lower()
                or search in e.get("name", "").lower()
                or search in e.get("email", "").lower()
                or search in e.get("designation", "").lower()
            ]

        if dept and dept != "All":
            employees = [e for e in employees if e.get("department") == dept]

        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/employees", methods=["POST"])
def add_employee():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()

        # Auto-generate next employee ID if empty
        if not emp_id:
            existing = file_manager.read_data(FileManager.EMPLOYEES_FILE)
            max_num = 0
            for emp in existing:
                try:
                    num = int(emp["employee_id"].replace("EMP", ""))
                    if num > max_num:
                        max_num = num
                except ValueError:
                    continue
            emp_id = f"EMP{max_num + 1:03d}"

        # Check uniqueness
        if file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id):
            return jsonify({"error": f"Employee ID '{emp_id}' already exists."}), 400

        emp_type = data.get("employment_type", "Salaried")
        emp_dict = {
            "employee_id": emp_id,
            "name": data.get("name", "").strip(),
            "email": data.get("email", "").strip(),
            "contact": data.get("contact", "").strip(),
            "department": data.get("department", "IT").strip(),
            "designation": data.get("designation", "").strip(),
            "joining_date": data.get("joining_date", datetime.now().strftime("%Y-%m-%d")).strip(),
            "employment_type": emp_type,
            "status": data.get("status", "Active").strip()
        }

        if emp_type == "Salaried":
            emp_dict["basic_salary"] = float(data.get("basic_salary", 50000))
        else:
            emp_dict["hourly_rate"] = float(data.get("hourly_rate", 300))

        # Validate through OOP factory
        emp_obj = create_employee_from_dict(emp_dict)
        file_manager.add_record(FileManager.EMPLOYEES_FILE, emp_obj.to_dict())

        # Create default compensation record if not exists
        comp = file_manager.find_record(FileManager.COMPENSATION_FILE, "employee_id", emp_id)
        if not comp:
            file_manager.add_record(FileManager.COMPENSATION_FILE, {
                "employee_id": emp_id,
                "hra": 0,
                "transport_allowance": 0,
                "medical_allowance": 0,
                "other_allowances": 0,
                "performance_bonus": 0,
                "other_deductions": 0
            })

        return jsonify({
            "message": f"Employee '{emp_id}' added successfully.",
            "employee": emp_obj.to_dict()
        }), 201
    except (EmployeeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/employees/<emp_id>", methods=["PUT"])
def update_employee(emp_id):
    try:
        emp_id = emp_id.strip().upper()
        existing = file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
        if not existing:
            return jsonify({"error": f"Employee '{emp_id}' not found."}), 404

        data = request.json or {}
        emp_type = data.get("employment_type", existing.get("employment_type", "Salaried"))
        emp_dict = {
            "employee_id": emp_id,
            "name": data.get("name", existing.get("name", "")).strip(),
            "email": data.get("email", existing.get("email", "")).strip(),
            "contact": data.get("contact", existing.get("contact", "")).strip(),
            "department": data.get("department", existing.get("department", "IT")).strip(),
            "designation": data.get("designation", existing.get("designation", "")).strip(),
            "joining_date": data.get("joining_date", existing.get("joining_date", "")).strip(),
            "employment_type": emp_type,
            "status": data.get("status", existing.get("status", "Active")).strip()
        }

        if emp_type == "Salaried":
            emp_dict["basic_salary"] = float(data.get("basic_salary", existing.get("basic_salary", 50000)))
        else:
            emp_dict["hourly_rate"] = float(data.get("hourly_rate", existing.get("hourly_rate", 300)))

        emp_obj = create_employee_from_dict(emp_dict)
        file_manager.update_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id, emp_obj.to_dict())

        return jsonify({
            "message": f"Employee '{emp_id}' updated successfully.",
            "employee": emp_obj.to_dict()
        })
    except (EmployeeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/employees/<emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    try:
        emp_id = emp_id.strip().upper()
        deleted = file_manager.delete_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
        if not deleted:
            return jsonify({"error": f"Employee '{emp_id}' not found."}), 404

        # Clean up compensation record
        file_manager.delete_record(FileManager.COMPENSATION_FILE, "employee_id", emp_id)
        return jsonify({"message": f"Employee '{emp_id}' deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 3. Attendance Management Endpoints
# ============================================================
@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    try:
        records = file_manager.read_data(FileManager.ATTENDANCE_FILE)
        emp_id = request.args.get("employee_id", "").strip().upper()
        month = request.args.get("month")
        year = request.args.get("year")

        if emp_id and emp_id != "ALL":
            records = [r for r in records if r.get("employee_id") == emp_id]

        if month and year:
            try:
                m_int = int(month)
                y_int = int(year)
                filtered = []
                for r in records:
                    date_val = r.get("date", "")
                    if date_val:
                        dt = datetime.strptime(date_val, "%Y-%m-%d")
                        if dt.month == m_int and dt.year == y_int:
                            filtered.append(r)
                records = filtered
            except ValueError:
                pass

        # Sort descending by date
        records.sort(key=lambda x: x.get("date", ""), reverse=True)
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/attendance", methods=["POST"])
def add_attendance():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()
        date_str = data.get("date", "").strip()
        check_in = data.get("check_in", "").strip()
        check_out = data.get("check_out", "").strip()
        break_duration = float(data.get("break_duration", 0))
        status = data.get("status", "Present").strip()

        # Validate employee exists
        if not file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id):
            return jsonify({"error": f"Employee '{emp_id}' does not exist."}), 404

        # Check duplicate for same employee and date
        records = file_manager.read_data(FileManager.ATTENDANCE_FILE)
        for r in records:
            if r.get("employee_id") == emp_id and r.get("date") == date_str:
                return jsonify({"error": f"Attendance record for {emp_id} on {date_str} already exists."}), 400

        # Construct and validate with OOP Attendance class
        att = Attendance(emp_id, date_str, check_in, check_out, break_duration, status)
        file_manager.add_record(FileManager.ATTENDANCE_FILE, att.to_dict())

        return jsonify({
            "message": "Attendance recorded successfully.",
            "record": att.to_dict()
        }), 201
    except (InvalidAttendanceError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/attendance", methods=["PUT"])
def update_attendance():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()
        date_str = data.get("date", "").strip()

        records = file_manager.read_data(FileManager.ATTENDANCE_FILE)
        found_idx = None
        for i, r in enumerate(records):
            if r.get("employee_id") == emp_id and r.get("date") == date_str:
                found_idx = i
                break

        if found_idx is None:
            return jsonify({"error": "Attendance record not found."}), 404

        check_in = data.get("check_in", "").strip()
        check_out = data.get("check_out", "").strip()
        break_duration = float(data.get("break_duration", 0))
        status = data.get("status", "Present").strip()

        att = Attendance(emp_id, date_str, check_in, check_out, break_duration, status)
        records[found_idx] = att.to_dict()
        file_manager.write_data(FileManager.ATTENDANCE_FILE, records)

        return jsonify({
            "message": "Attendance updated successfully.",
            "record": att.to_dict()
        })
    except (InvalidAttendanceError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/attendance", methods=["DELETE"])
def delete_attendance():
    try:
        emp_id = request.args.get("employee_id", "").strip().upper()
        date_str = request.args.get("date", "").strip()

        records = file_manager.read_data(FileManager.ATTENDANCE_FILE)
        initial_len = len(records)
        records = [
            r for r in records
            if not (r.get("employee_id") == emp_id and r.get("date") == date_str)
        ]

        if len(records) == initial_len:
            return jsonify({"error": "Attendance record not found."}), 404

        file_manager.write_data(FileManager.ATTENDANCE_FILE, records)
        return jsonify({"message": "Attendance record deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 4. Leave Management Endpoints
# ============================================================
@app.route("/api/leaves", methods=["GET"])
def get_leaves():
    try:
        leaves = file_manager.read_data(FileManager.LEAVES_FILE)
        employees = {e["employee_id"]: e for e in file_manager.read_data(FileManager.EMPLOYEES_FILE)}

        # Enrich with employee info
        for lv in leaves:
            emp = employees.get(lv.get("employee_id"), {})
            lv["employee_name"] = emp.get("name", "Unknown")
            lv["department"] = emp.get("department", "Unknown")

        return jsonify(leaves)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaves", methods=["POST"])
def apply_leave():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()
        start_date = data.get("start_date", "").strip()
        end_date = data.get("end_date", "").strip()
        leave_type = data.get("leave_type", "Paid Leave").strip()
        reason = data.get("reason", "").strip()

        if not file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id):
            return jsonify({"error": f"Employee '{emp_id}' does not exist."}), 404

        # Generate next leave ID
        leaves = file_manager.read_data(FileManager.LEAVES_FILE)
        max_num = 0
        for l in leaves:
            try:
                num = int(l.get("leave_id", "").replace("LV", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
        leave_id = f"LV{max_num + 1:03d}"

        leave_obj = Leave(leave_id, emp_id, start_date, end_date, leave_type, reason, "Pending")
        file_manager.add_record(FileManager.LEAVES_FILE, leave_obj.to_dict())

        return jsonify({
            "message": f"Leave application '{leave_id}' submitted successfully.",
            "leave": leave_obj.to_dict()
        }), 201
    except (InvalidLeaveError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaves/<leave_id>/decision", methods=["POST"])
def decide_leave(leave_id):
    try:
        data = request.json or {}
        status = data.get("status", "").strip()
        if status not in ["Approved", "Rejected"]:
            return jsonify({"error": "Status must be 'Approved' or 'Rejected'."}), 400

        updated = file_manager.update_record(FileManager.LEAVES_FILE, "leave_id", leave_id, {"status": status})
        if not updated:
            return jsonify({"error": f"Leave '{leave_id}' not found."}), 404

        return jsonify({"message": f"Leave '{leave_id}' marked as {status}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaves/<leave_id>", methods=["DELETE"])
def delete_leave(leave_id):
    try:
        deleted = file_manager.delete_record(FileManager.LEAVES_FILE, "leave_id", leave_id)
        if not deleted:
            return jsonify({"error": f"Leave '{leave_id}' not found."}), 404
        return jsonify({"message": f"Leave '{leave_id}' removed."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 5. Compensation Management Endpoints
# ============================================================
@app.route("/api/compensation", methods=["GET"])
def get_compensation_list():
    try:
        compensations = file_manager.read_data(FileManager.COMPENSATION_FILE)
        employees = {e["employee_id"]: e for e in file_manager.read_data(FileManager.EMPLOYEES_FILE)}

        results = []
        for c in compensations:
            emp_id = c.get("employee_id")
            emp = employees.get(emp_id, {})
            merged = {**c}
            merged["employee_name"] = emp.get("name", "Unknown")
            merged["department"] = emp.get("department", "Unknown")
            merged["designation"] = emp.get("designation", "Unknown")
            merged["employment_type"] = emp.get("employment_type", "Salaried")
            merged["base_pay"] = emp.get("basic_salary") if emp.get("employment_type") == "Salaried" else emp.get("hourly_rate")
            results.append(merged)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compensation/<emp_id>", methods=["GET"])
def get_employee_compensation(emp_id):
    try:
        emp_id = emp_id.strip().upper()
        comp = file_manager.find_record(FileManager.COMPENSATION_FILE, "employee_id", emp_id)
        if not comp:
            comp = {
                "employee_id": emp_id,
                "hra": 0, "transport_allowance": 0, "medical_allowance": 0,
                "other_allowances": 0, "performance_bonus": 0, "other_deductions": 0
            }
        return jsonify(comp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compensation", methods=["POST"])
def update_compensation():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()
        if not emp_id:
            return jsonify({"error": "Employee ID is required."}), 400

        comp_data = {
            "employee_id": emp_id,
            "hra": float(data.get("hra", 0)),
            "transport_allowance": float(data.get("transport_allowance", 0)),
            "medical_allowance": float(data.get("medical_allowance", 0)),
            "other_allowances": float(data.get("other_allowances", 0)),
            "performance_bonus": float(data.get("performance_bonus", 0)),
            "other_deductions": float(data.get("other_deductions", 0))
        }

        existing = file_manager.find_record(FileManager.COMPENSATION_FILE, "employee_id", emp_id)
        if existing:
            file_manager.update_record(FileManager.COMPENSATION_FILE, "employee_id", emp_id, comp_data)
        else:
            file_manager.add_record(FileManager.COMPENSATION_FILE, comp_data)

        return jsonify({
            "message": f"Compensation updated for {emp_id}.",
            "compensation": comp_data
        })
    except ValueError:
        return jsonify({"error": "All compensation fields must be valid numeric values."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 6. Payroll Processing Endpoints
# ============================================================
@app.route("/api/payroll", methods=["GET"])
def get_payroll():
    try:
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)

        if month and year:
            records = payroll_manager.get_payroll_summary(month, year)
        else:
            records = file_manager.read_data(FileManager.PAYROLL_FILE)

        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payroll/generate", methods=["POST"])
def generate_payroll_batch():
    try:
        data = request.json or {}
        month = int(data.get("month", 10))
        year = int(data.get("year", 2026))

        employees = file_manager.read_data(FileManager.EMPLOYEES_FILE)
        active_employees = [e for e in employees if e.get("status") == "Active"]

        if not active_employees:
            return jsonify({"error": "No active employees found to generate payroll."}), 400

        generated_list = []
        skipped_list = []

        for emp_data in active_employees:
            try:
                emp_obj = create_employee_from_dict(emp_data)
                # Polymorphic payroll generation
                p = payroll_manager.generate_payroll(emp_obj, month, year)
                generated_list.append(p.to_dict())
            except DuplicatePayrollError:
                skipped_list.append(emp_data.get("employee_id"))
            except Exception as ex:
                return jsonify({"error": f"Error for {emp_data.get('employee_id')}: {str(ex)}"}), 500

        all_current = payroll_manager.get_payroll_summary(month, year)
        return jsonify({
            "message": f"Payroll processing complete for {month:02d}/{year}.",
            "generated_count": len(generated_list),
            "skipped_count": len(skipped_list),
            "skipped_employees": skipped_list,
            "records": all_current
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payroll/finalize/<payroll_id>", methods=["POST"])
def finalize_payroll(payroll_id):
    try:
        payroll_id = payroll_id.strip()
        payroll_manager.finalize_payroll(payroll_id)
        return jsonify({"message": f"Payroll '{payroll_id}' finalized and locked successfully."})
    except PayrollError as pe:
        return jsonify({"error": str(pe)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payroll/finalize-all", methods=["POST"])
def finalize_all_drafts():
    try:
        data = request.json or {}
        month = int(data.get("month", 10))
        year = int(data.get("year", 2026))

        records = payroll_manager.get_payroll_summary(month, year)
        count = 0
        for rec in records:
            if rec.get("status") == "Draft":
                payroll_manager.finalize_payroll(rec["payroll_id"])
                count += 1

        return jsonify({
            "message": f"Finalized {count} draft payroll record(s) for {month:02d}/{year}.",
            "count": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payroll/breakdown/<payroll_id>", methods=["GET"])
def get_payroll_breakdown(payroll_id):
    try:
        rec = file_manager.find_record(FileManager.PAYROLL_FILE, "payroll_id", payroll_id)
        if not rec:
            return jsonify({"error": f"Payroll '{payroll_id}' not found."}), 404

        text = payroll_manager.generate_payslip_text(rec)
        return jsonify({
            "payroll": rec,
            "payslip_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 7. Payslips Endpoints
# ============================================================
@app.route("/api/payslips/preview", methods=["GET"])
def preview_payslip():
    try:
        emp_id = request.args.get("employee_id", "").strip().upper()
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)

        if not emp_id or not month or not year:
            return jsonify({"error": "employee_id, month, and year are required."}), 400

        payrolls = file_manager.read_data(FileManager.PAYROLL_FILE)
        matched = None
        for p in payrolls:
            if p.get("employee_id") == emp_id and p.get("month") == month and p.get("year") == year:
                matched = p
                break

        if not matched:
            return jsonify({
                "error": f"No payroll record found for employee '{emp_id}' for {month:02d}/{year}. Please generate payroll in the 'Payroll Processing' tab first."
            }), 404

        text = payroll_manager.generate_payslip_text(matched)
        return jsonify({
            "payroll": matched,
            "payslip_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payslips/download", methods=["POST"])
def download_payslip():
    try:
        data = request.json or {}
        emp_id = data.get("employee_id", "").strip().upper()
        month = int(data.get("month", 10))
        year = int(data.get("year", 2026))

        payrolls = file_manager.read_data(FileManager.PAYROLL_FILE)
        matched = None
        for p in payrolls:
            if p.get("employee_id") == emp_id and p.get("month") == month and p.get("year") == year:
                matched = p
                break

        if not matched:
            return jsonify({"error": "Payroll record not found."}), 404

        text = payroll_manager.generate_payslip_text(matched)
        saved_path = ""
        try:
            saved_path = payroll_manager.save_payslip(matched)
        except Exception:
            pass

        filename = f"payslip_{emp_id}_{month:02d}_{year}.txt"
        return jsonify({
            "filename": filename,
            "content": text,
            "saved_path": saved_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 8. Payment History & Disbursement Endpoints
# ============================================================
@app.route("/api/payments/pending", methods=["GET"])
def get_pending_payments():
    try:
        pending = payroll_manager.get_pending_payments()
        return jsonify(pending)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payments/history", methods=["GET"])
def get_payment_history():
    try:
        completed = payroll_manager.get_completed_payments()
        completed.sort(key=lambda x: x.get("payment_date", ""), reverse=True)
        return jsonify(completed)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/payments/disburse", methods=["POST"])
def disburse_payment():
    try:
        data = request.json or {}
        payroll_id = data.get("payroll_id", "").strip()
        method = data.get("payment_method", "Bank Transfer").strip()
        ref = data.get("transaction_ref", "").strip()

        if not payroll_id:
            return jsonify({"error": "Payroll ID is required."}), 400
        if not ref:
            return jsonify({"error": "Transaction / Reference No. is required."}), 400

        payment_obj = payroll_manager.record_payment(payroll_id, method, ref)
        return jsonify({
            "message": f"Payment successfully recorded for {payroll_id} via {method}.",
            "payment": payment_obj.to_dict()
        })
    except PayrollError as pe:
        return jsonify({"error": str(pe)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# Static Files & Catch-all (for serving frontend from Flask)
# ============================================================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if FRONTEND_DIST and os.path.exists(FRONTEND_DIST):
        target_file = os.path.join(FRONTEND_DIST, path)
        if path and os.path.exists(target_file):
            return send_from_directory(FRONTEND_DIST, path)
        return send_from_directory(FRONTEND_DIST, "index.html")
    return jsonify({
        "message": "PaySphere REST API Server is running. Frontend dist not built or running via Vite dev server."
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting PaySphere API Server on http://127.0.0.1:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=True)
