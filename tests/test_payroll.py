"""
tests/test_payroll.py - Comprehensive Unit Tests for Payroll & Compensation System

Tests covered:
- Employee Hierarchy (SalariedEmployee, HourlyEmployee, validation, properties)
- Salary Calculations (Salaried vs Hourly, Overtime, Deductions, Allowances)
- Attendance Record & Working Hours Computation
- Leave Application & Days Computation
- FileManager JSON Persistence (CRUD operations, isolated in temporary directory)
- PayrollManager Operations (Generation, Duplicate prevention, Finalization, Payments, Payslips)
"""

import unittest
import os
import tempfile
import shutil
from datetime import datetime

from employee import (
    Employee,
    SalariedEmployee,
    HourlyEmployee,
    create_employee_from_dict,
    InvalidSalaryError,
    InvalidEmployeeDataError
)
from records import (
    Attendance,
    Leave,
    Payment,
    InvalidAttendanceError,
    InvalidLeaveError
)
from file_manager import FileManager
from payroll import (
    Payroll,
    SalaryBreakdown,
    PayrollManager,
    DuplicatePayrollError,
    PayrollError,
    PayrollNotFinalizedError
)


class TestEmployeeHierarchy(unittest.TestCase):
    """Unit tests for the Employee base class and subclasses."""

    def test_create_salaried_employee(self):
        emp = SalariedEmployee("EMP001", "Alice", "alice@corp.com", "1234567890",
                               "IT", "Dev", "2024-01-01", 50000)
        self.assertEqual(emp.employee_id, "EMP001")
        self.assertEqual(emp.name, "Alice")
        self.assertEqual(emp.employment_type, "Salaried")
        self.assertEqual(emp.basic_salary, 50000)
        self.assertIn("50,000.00", emp.get_base_pay_info())

    def test_create_hourly_employee(self):
        emp = HourlyEmployee("EMP002", "Bob", "bob@corp.com", "9876543210",
                             "Ops", "Tech", "2024-02-01", 300)
        self.assertEqual(emp.employee_id, "EMP002")
        self.assertEqual(emp.name, "Bob")
        self.assertEqual(emp.employment_type, "Hourly")
        self.assertEqual(emp.hourly_rate, 300)
        self.assertIn("300.00", emp.get_base_pay_info())

    def test_invalid_negative_salary(self):
        with self.assertRaises(InvalidSalaryError):
            SalariedEmployee("EMP003", "Charlie", "c@corp.com", "123", "IT", "Dev", "2024-01-01", -1000)

        with self.assertRaises(InvalidSalaryError):
            HourlyEmployee("EMP004", "David", "d@corp.com", "123", "IT", "Dev", "2024-01-01", -50)

    def test_empty_employee_name_or_id(self):
        with self.assertRaises(InvalidEmployeeDataError):
            SalariedEmployee("", "NoID", "e@corp.com", "123", "IT", "Dev", "2024-01-01", 30000)
        with self.assertRaises(InvalidEmployeeDataError):
            SalariedEmployee("EMP005", "", "e@corp.com", "123", "IT", "Dev", "2024-01-01", 30000)

    def test_employee_properties_and_setters(self):
        emp = SalariedEmployee("EMP006", "Eve", "e@corp.com", "123", "HR", "Mgr", "2024-01-01", 40000)
        emp.name = "Eve Adams"
        emp.department = "Finance"
        emp.basic_salary = 45000
        emp.status = "Inactive"

        self.assertEqual(emp.name, "Eve Adams")
        self.assertEqual(emp.department, "Finance")
        self.assertEqual(emp.basic_salary, 45000)
        self.assertEqual(emp.status, "Inactive")

        with self.assertRaises(InvalidEmployeeDataError):
            emp.status = "Suspended"  # Invalid status

    def test_employee_serialization_and_factory(self):
        salaried = SalariedEmployee("EMP007", "Frank", "f@corp.com", "123", "Sales", "Rep", "2024-01-01", 35000)
        data = salaried.to_dict()
        recreated = create_employee_from_dict(data)
        self.assertIsInstance(recreated, SalariedEmployee)
        self.assertEqual(recreated.basic_salary, 35000)

        hourly = HourlyEmployee("EMP008", "Grace", "g@corp.com", "123", "Support", "Exec", "2024-01-01", 250)
        h_data = hourly.to_dict()
        h_recreated = create_employee_from_dict(h_data)
        self.assertIsInstance(h_recreated, HourlyEmployee)
        self.assertEqual(h_recreated.hourly_rate, 250)


class TestSalaryCalculations(unittest.TestCase):
    """Unit tests for polymorphic salary calculations."""

    def setUp(self):
        self.salaried = SalariedEmployee("EMP001", "Salaried Test", "s@corp.com", "123", "IT", "Dev", "2024-01-01", 44000)
        # Daily rate = 44000 / 22 = 2000.00
        # Hourly rate = 44000 / (22 * 8) = 250.00
        self.hourly = HourlyEmployee("EMP002", "Hourly Test", "h@corp.com", "123", "Ops", "Tech", "2024-01-01", 200)

    def test_salaried_full_attendance_no_allowance(self):
        att = {"present_days": 22, "absent_days": 0, "half_days": 0, "paid_leaves": 0, "unpaid_leaves": 0, "overtime_hours": 0}
        comp = {"hra": 0, "transport_allowance": 0, "medical_allowance": 0, "other_allowances": 0, "performance_bonus": 0, "other_deductions": 0}

        calc = self.salaried.calculate_salary(att, comp)
        self.assertEqual(calc["gross_salary"], 44000)
        self.assertEqual(calc["total_deductions"], 0)
        self.assertEqual(calc["net_salary"], 44000)

    def test_salaried_unpaid_leave_and_absence(self):
        # 1 unpaid leave (deduct 2000), 1 absent (deduct 2000), 1 half-day (deduct 1000) = total deduct 5000
        att = {"present_days": 19, "absent_days": 1, "half_days": 1, "paid_leaves": 1, "unpaid_leaves": 1, "overtime_hours": 0}
        comp = {"hra": 0, "transport_allowance": 0, "medical_allowance": 0, "other_allowances": 0, "performance_bonus": 0, "other_deductions": 0}

        calc = self.salaried.calculate_salary(att, comp)
        self.assertEqual(calc["unpaid_leave_deduction"], 2000.0)
        self.assertEqual(calc["absence_deduction"], 3000.0)  # 1 absent (2000) + 1 half day (1000)
        self.assertEqual(calc["total_deductions"], 5000.0)
        self.assertEqual(calc["net_salary"], 39000.0)

    def test_salaried_overtime_and_allowances(self):
        # 4 overtime hours: 4 * 250 * 1.5 = 1500.0
        # Allowances: HRA 5000 + Transport 2000 = 7000. Bonus 3000. Gross = 44000 + 7000 + 3000 + 1500 = 55500
        att = {"present_days": 22, "absent_days": 0, "half_days": 0, "paid_leaves": 0, "unpaid_leaves": 0, "overtime_hours": 4}
        comp = {"hra": 5000, "transport_allowance": 2000, "medical_allowance": 0, "other_allowances": 0, "performance_bonus": 3000, "other_deductions": 500}

        calc = self.salaried.calculate_salary(att, comp)
        self.assertEqual(calc["overtime_pay"], 1500.0)
        self.assertEqual(calc["total_allowances"], 7000.0)
        self.assertEqual(calc["gross_salary"], 55500.0)
        self.assertEqual(calc["other_deductions"], 500.0)
        self.assertEqual(calc["net_salary"], 55000.0)

    def test_hourly_regular_pay(self):
        # 160 total hours, 0 overtime -> regular hours = 160. Rate = 200 -> Regular pay = 32000
        att = {"total_working_hours": 160.0, "overtime_hours": 0}
        comp = {"hra": 0, "transport_allowance": 0, "medical_allowance": 0, "other_allowances": 0, "performance_bonus": 0, "other_deductions": 0}

        calc = self.hourly.calculate_salary(att, comp)
        self.assertEqual(calc["regular_hours"], 160.0)
        self.assertEqual(calc["regular_pay"], 32000.0)
        self.assertEqual(calc["net_salary"], 32000.0)

    def test_hourly_with_overtime_and_deductions(self):
        # Total working hours = 170, OT hours = 10 -> Regular hours = 160
        # Regular pay = 160 * 200 = 32000
        # OT pay = 10 * 200 * 1.5 = 3000
        # Allowance = 1000, Deduction = 400
        # Gross = 32000 + 3000 + 1000 = 36000. Net = 36000 - 400 = 35600
        att = {"total_working_hours": 170.0, "overtime_hours": 10.0}
        comp = {"hra": 0, "transport_allowance": 1000, "medical_allowance": 0, "other_allowances": 0, "performance_bonus": 0, "other_deductions": 400}

        calc = self.hourly.calculate_salary(att, comp)
        self.assertEqual(calc["regular_pay"], 32000.0)
        self.assertEqual(calc["overtime_pay"], 3000.0)
        self.assertEqual(calc["gross_salary"], 36000.0)
        self.assertEqual(calc["net_salary"], 35600.0)


class TestAttendanceRecord(unittest.TestCase):
    """Unit tests for Attendance calculations and validations."""

    def test_calculate_standard_working_hours(self):
        att = Attendance("EMP001", "2026-10-01", check_in="09:00", check_out="18:00", break_duration=1.0, status="Present")
        # 9 hours total - 1 break = 8 hours
        self.assertEqual(att.total_working_hours, 8.0)

    def test_overtime_hours_calculation(self):
        att = Attendance("EMP001", "2026-10-02", check_in="09:00", check_out="20:00", break_duration=1.0, status="Present")
        # 11 hours - 1 break = 10 hours
        self.assertEqual(att.total_working_hours, 10.0)

    def test_zero_hours_for_absent_and_leave(self):
        att_absent = Attendance("EMP001", "2026-10-03", status="Absent")
        self.assertEqual(att_absent.total_working_hours, 0.0)

        att_leave = Attendance("EMP001", "2026-10-04", status="Paid Leave")
        self.assertEqual(att_leave.total_working_hours, 0.0)

    def test_invalid_status_exception(self):
        with self.assertRaises(InvalidAttendanceError):
            Attendance("EMP001", "2026-10-05", status="NotAValidStatus")

    def test_attendance_dict_serialization(self):
        att = Attendance("EMP001", "2026-10-01", check_in="09:00", check_out="17:00", break_duration=1.0, status="Present")
        d = att.to_dict()
        recreated = Attendance.from_dict(d)
        self.assertEqual(recreated.total_working_hours, 7.0)


class TestLeaveRecord(unittest.TestCase):
    """Unit tests for Leave entity."""

    def test_leave_day_count(self):
        lv = Leave("LV001", "EMP001", "2026-10-10", "2026-10-12", "Paid Leave", "Family event")
        # 10, 11, 12 = 3 days
        self.assertEqual(lv.get_number_of_days(), 3)

    def test_invalid_leave_type(self):
        with self.assertRaises(InvalidLeaveError):
            Leave("LV002", "EMP001", "2026-10-10", "2026-10-11", "Sabbatical")

    def test_leave_status_update(self):
        lv = Leave("LV003", "EMP001", "2026-10-10", "2026-10-10", "Unpaid Leave")
        self.assertEqual(lv.status, "Pending")
        lv.status = "Approved"
        self.assertEqual(lv.status, "Approved")


class TestFileManagerOperations(unittest.TestCase):
    """Unit tests for FileManager with isolated temp directory."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_path=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read_missing_file_returns_empty_list(self):
        data = self.fm.read_data("non_existent.json")
        self.assertEqual(data, [])

    def test_write_and_read_records(self):
        test_records = [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]
        self.fm.write_data("test.json", test_records)

        loaded = self.fm.read_data("test.json")
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["name"], "Item A")

    def test_add_record(self):
        self.fm.add_record("items.json", {"id": "ITM01", "val": 100})
        self.fm.add_record("items.json", {"id": "ITM02", "val": 200})

        loaded = self.fm.read_data("items.json")
        self.assertEqual(len(loaded), 2)

    def test_update_record(self):
        self.fm.add_record("items.json", {"id": "ITM01", "val": 100})
        updated = self.fm.update_record("items.json", "id", "ITM01", {"id": "ITM01", "val": 999})
        self.assertTrue(updated)

        rec = self.fm.find_record("items.json", "id", "ITM01")
        self.assertEqual(rec["val"], 999)

    def test_delete_record(self):
        self.fm.add_record("items.json", {"id": "ITM01", "val": 100})
        self.fm.add_record("items.json", {"id": "ITM02", "val": 200})

        deleted = self.fm.delete_record("items.json", "id", "ITM01")
        self.assertTrue(deleted)
        self.assertIsNone(self.fm.find_record("items.json", "id", "ITM01"))
        self.assertIsNotNone(self.fm.find_record("items.json", "id", "ITM02"))


class TestPayrollManagerFlow(unittest.TestCase):
    """End-to-end unit tests for PayrollManager generation, finalization and payment."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_path=self.test_dir)
        self.pm = PayrollManager(self.fm)

        # Setup test employee
        self.employee = SalariedEmployee("EMP001", "Test Emp", "t@c.com", "123", "IT", "Dev", "2024-01-01", 50000)
        self.fm.add_record(FileManager.EMPLOYEES_FILE, self.employee.to_dict())

        # Setup attendance (20 days present, 2 days unpaid leave)
        for d in range(1, 21):
            date_str = f"2026-10-{d:02d}"
            att = Attendance("EMP001", date_str, "09:00", "18:00", 1.0, "Present")
            self.fm.add_record(FileManager.ATTENDANCE_FILE, att.to_dict())

        for d in [21, 22]:
            date_str = f"2026-10-{d:02d}"
            att = Attendance("EMP001", date_str, status="Unpaid Leave")
            self.fm.add_record(FileManager.ATTENDANCE_FILE, att.to_dict())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_attendance_summary(self):
        summary = self.pm.get_attendance_summary("EMP001", 10, 2026)
        self.assertEqual(summary["present_days"], 20)
        self.assertEqual(summary["unpaid_leaves"], 2)
        self.assertEqual(summary["total_working_hours"], 160.0)

    def test_generate_payroll_and_duplicate_prevention(self):
        payroll = self.pm.generate_payroll(self.employee, 10, 2026)
        self.assertIsNotNone(payroll)
        self.assertEqual(payroll.status, "Draft")
        self.assertEqual(payroll.payment_status, "Unpaid")

        # Attempting duplicate generation must raise DuplicatePayrollError
        with self.assertRaises(DuplicatePayrollError):
            self.pm.generate_payroll(self.employee, 10, 2026)

    def test_finalize_payroll(self):
        payroll = self.pm.generate_payroll(self.employee, 10, 2026)
        success = self.pm.finalize_payroll(payroll.payroll_id)
        self.assertTrue(success)

        # Check in storage
        record = self.fm.find_record(FileManager.PAYROLL_FILE, "payroll_id", payroll.payroll_id)
        self.assertEqual(record["status"], "Finalized")

        # Attempting to re-finalize raises PayrollError
        with self.assertRaises(PayrollError):
            self.pm.finalize_payroll(payroll.payroll_id)

    def test_cannot_pay_unfinalized_payroll(self):
        payroll = self.pm.generate_payroll(self.employee, 10, 2026)
        with self.assertRaises(PayrollNotFinalizedError):
            self.pm.record_payment(payroll.payroll_id, "UPI", "TXN1234")

    def test_successful_payment_recording(self):
        payroll = self.pm.generate_payroll(self.employee, 10, 2026)
        self.pm.finalize_payroll(payroll.payroll_id)

        payment = self.pm.record_payment(payroll.payroll_id, "Bank Transfer", "TXN9999")
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_method, "Bank Transfer")
        self.assertEqual(payment.transaction_ref, "TXN9999")

        # Verify payroll updated to Paid
        pay_rec = self.fm.find_record(FileManager.PAYROLL_FILE, "payroll_id", payroll.payroll_id)
        self.assertEqual(pay_rec["payment_status"], "Paid")

        # Paying again should raise PayrollError
        with self.assertRaises(PayrollError):
            self.pm.record_payment(payroll.payroll_id, "Bank Transfer", "TXN9999")

    def test_payslip_generation(self):
        payroll = self.pm.generate_payroll(self.employee, 10, 2026)
        payslip_txt = self.pm.generate_payslip_text(payroll.to_dict())
        self.assertIn("PAYSLIP", payslip_txt)
        self.assertIn("EMP001", payslip_txt)
        self.assertIn("TechCorp Solutions", payslip_txt)

        file_path = self.pm.save_payslip(payroll.to_dict())
        self.assertTrue(os.path.exists(file_path))


if __name__ == "__main__":
    unittest.main()
