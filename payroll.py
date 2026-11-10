"""
payroll.py - Payroll Processing and Salary Calculation

This module handles payroll generation, salary calculation orchestration,
payslip generation, and payment processing.

Classes:
    SalaryBreakdown - Stores salary component details (Composition)
    Payroll         - Monthly payroll record for an employee
    PayrollManager  - Orchestrates all payroll operations

OOP Concepts Demonstrated:
    - Composition    : Payroll contains a SalaryBreakdown (part-of relationship)
    - Aggregation    : PayrollManager uses Employee objects (uses-a relationship)
    - Polymorphism   : PayrollManager calls calculate_salary() on any Employee
    - Encapsulation  : Complex payroll logic hidden behind simple methods
    - Exception Handling : Custom exceptions for payroll errors
"""

from datetime import datetime
from employee import Employee, create_employee_from_dict
from records import Payment
from file_manager import FileManager


# ============================================================
# Custom Exceptions
# ============================================================

class PayrollError(Exception):
    """Base exception for payroll-related errors."""
    pass


class DuplicatePayrollError(PayrollError):
    """Raised when payroll already exists for an employee in a given month."""
    pass


class PayrollNotFinalizedError(PayrollError):
    """Raised when trying to pay an unfinalised payroll."""
    pass


# ============================================================
# SalaryBreakdown Class (COMPOSITION with Payroll)
# ============================================================

class SalaryBreakdown:
    """
    Stores the detailed breakdown of an employee's salary.

    This class demonstrates COMPOSITION - a SalaryBreakdown is a
    PART OF a Payroll object. It cannot exist independently.
    When a Payroll is created, a SalaryBreakdown is created inside it.
    When the Payroll is deleted, the SalaryBreakdown goes with it.

    This is different from Association, where two objects can exist
    independently of each other.
    """

    def __init__(self, breakdown_data):
        """
        Initialize with salary component data.

        Args:
            breakdown_data (dict): Salary details from Employee.calculate_salary()
        """
        self._data = breakdown_data

    # Properties for accessing salary components

    @property
    def basic_salary(self):
        return self._data.get("basic_salary", 0)

    @property
    def hourly_rate(self):
        return self._data.get("hourly_rate", 0)

    @property
    def regular_hours(self):
        return self._data.get("regular_hours", 0)

    @property
    def regular_pay(self):
        return self._data.get("regular_pay", 0)

    @property
    def total_allowances(self):
        return self._data.get("total_allowances", 0)

    @property
    def performance_bonus(self):
        return self._data.get("performance_bonus", 0)

    @property
    def overtime_hours(self):
        return self._data.get("overtime_hours", 0)

    @property
    def overtime_pay(self):
        return self._data.get("overtime_pay", 0)

    @property
    def total_deductions(self):
        return self._data.get("total_deductions", 0)

    @property
    def gross_salary(self):
        return self._data.get("gross_salary", 0)

    @property
    def net_salary(self):
        return self._data.get("net_salary", 0)

    def to_dict(self):
        """Return the complete breakdown as a dictionary."""
        return self._data.copy()


# ============================================================
# Payroll Class (Contains SalaryBreakdown - COMPOSITION)
# ============================================================

class Payroll:
    """
    Represents a monthly payroll record for one employee.

    A Payroll object CONTAINS a SalaryBreakdown object. This is
    COMPOSITION - the SalaryBreakdown is created as part of the
    Payroll and cannot exist without it.

    Once finalized, the payroll preserves its original salary
    calculation so historical records don't change even if the
    employee's current salary is updated later.

    Lifecycle: Draft -> Finalized -> Paid
    """

    def __init__(self, payroll_id, employee_id, employee_name, department,
                 designation, employment_type, month, year,
                 attendance_summary, salary_breakdown_data, status="Draft"):
        """
        Initialize a payroll record.

        Creates a SalaryBreakdown object internally (COMPOSITION).
        """
        self._payroll_id = payroll_id
        self._employee_id = employee_id
        self._employee_name = employee_name
        self._department = department
        self._designation = designation
        self._employment_type = employment_type
        self._month = month
        self._year = year
        self._attendance_summary = attendance_summary

        # COMPOSITION: SalaryBreakdown is created as part of Payroll
        self._salary_breakdown = SalaryBreakdown(salary_breakdown_data)

        self._status = status               # "Draft" or "Finalized"
        self._payment_status = "Unpaid"      # "Unpaid" or "Paid"
        self._created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---- Properties ----

    @property
    def payroll_id(self):
        return self._payroll_id

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def employee_name(self):
        return self._employee_name

    @property
    def department(self):
        return self._department

    @property
    def designation(self):
        return self._designation

    @property
    def employment_type(self):
        return self._employment_type

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year

    @property
    def salary_breakdown(self):
        """Access the SalaryBreakdown object (COMPOSITION)."""
        return self._salary_breakdown

    @property
    def attendance_summary(self):
        return self._attendance_summary

    @property
    def status(self):
        return self._status

    @property
    def payment_status(self):
        return self._payment_status

    @payment_status.setter
    def payment_status(self, value):
        self._payment_status = value

    @property
    def net_salary(self):
        """Shortcut to get net salary from breakdown."""
        return self._salary_breakdown.net_salary

    # ---- Methods ----

    def finalize(self):
        """Mark payroll as finalized. Cannot be modified after this."""
        self._status = "Finalized"

    def to_dict(self):
        """Convert payroll to dictionary for JSON storage."""
        return {
            "payroll_id": self._payroll_id,
            "employee_id": self._employee_id,
            "employee_name": self._employee_name,
            "department": self._department,
            "designation": self._designation,
            "employment_type": self._employment_type,
            "month": self._month,
            "year": self._year,
            "attendance_summary": self._attendance_summary,
            "salary_breakdown": self._salary_breakdown.to_dict(),
            "status": self._status,
            "payment_status": self._payment_status,
            "created_date": self._created_date
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Payroll object from a dictionary (loaded from JSON)."""
        payroll = cls(
            payroll_id=data["payroll_id"],
            employee_id=data["employee_id"],
            employee_name=data["employee_name"],
            department=data.get("department", ""),
            designation=data.get("designation", ""),
            employment_type=data.get("employment_type", ""),
            month=data["month"],
            year=data["year"],
            attendance_summary=data.get("attendance_summary", {}),
            salary_breakdown_data=data.get("salary_breakdown", {}),
            status=data.get("status", "Draft")
        )
        payroll._payment_status = data.get("payment_status", "Unpaid")
        payroll._created_date = data.get("created_date", "")
        return payroll

    def __str__(self):
        return (f"Payroll({self._payroll_id}, {self._employee_id}, "
                f"{self._month}/{self._year}, Rs.{self.net_salary:,.2f})")


# ============================================================
# PayrollManager Class (Orchestrator)
# ============================================================

class PayrollManager:
    """
    Manages all payroll operations.

    This class demonstrates:
    - AGGREGATION: It uses Employee and FileManager objects but
      does not own them. They can exist independently.
    - POLYMORPHISM: When generating payroll, it calls
      employee.calculate_salary() without knowing whether the
      employee is Salaried or Hourly. Python calls the correct
      version based on the actual object type.
    - ENCAPSULATION: Complex payroll logic is hidden behind
      simple public methods like generate_payroll().

    Main responsibilities:
    1. Calculate attendance summaries
    2. Generate payroll for employees
    3. Finalize payroll records
    4. Generate payslips (text format)
    5. Record payments
    """

    ORGANIZATION_NAME = "TechCorp Solutions Pvt. Ltd."

    def __init__(self, file_manager):
        """
        Initialize PayrollManager.

        Args:
            file_manager (FileManager): The file manager for data access.
                                        This is AGGREGATION - PayrollManager
                                        uses FileManager but doesn't own it.
        """
        self._file_manager = file_manager

    # ---- Attendance Summary ----

    def get_attendance_summary(self, employee_id, month, year):
        """
        Calculate attendance summary for an employee for a specific month.

        Reads attendance records and counts different statuses.

        Args:
            employee_id: The employee's ID.
            month: Month number (1-12).
            year: Year number (e.g., 2026).

        Returns:
            dict: Summary with present_days, absent_days, half_days,
                  paid_leaves, unpaid_leaves, holidays,
                  total_working_hours, overtime_hours.
        """
        all_attendance = self._file_manager.read_data(FileManager.ATTENDANCE_FILE)

        # Filter for this employee and month (format: "2026-10")
        month_prefix = f"{year}-{month:02d}"
        records = []
        for record in all_attendance:
            if (record["employee_id"] == employee_id and
                    record["date"].startswith(month_prefix)):
                records.append(record)

        # Count each type of attendance
        present_days = 0
        absent_days = 0
        half_days = 0
        paid_leaves = 0
        unpaid_leaves = 0
        holidays = 0
        total_working_hours = 0
        overtime_hours = 0

        for record in records:
            status = record.get("status", "Present")
            hours = record.get("total_working_hours", 0)

            if status == "Present":
                present_days += 1
                total_working_hours += hours
                # Overtime = hours worked beyond the standard day (8 hours)
                if hours > Employee.STANDARD_WORKING_HOURS_PER_DAY:
                    daily_ot = hours - Employee.STANDARD_WORKING_HOURS_PER_DAY
                    overtime_hours += round(daily_ot, 2)

            elif status == "Absent":
                absent_days += 1

            elif status == "Half-day":
                half_days += 1
                total_working_hours += hours

            elif status == "Paid Leave":
                paid_leaves += 1

            elif status == "Unpaid Leave":
                unpaid_leaves += 1

            elif status == "Holiday":
                holidays += 1

        return {
            "present_days": present_days,
            "absent_days": absent_days,
            "half_days": half_days,
            "paid_leaves": paid_leaves,
            "unpaid_leaves": unpaid_leaves,
            "holidays": holidays,
            "total_working_hours": round(total_working_hours, 2),
            "overtime_hours": round(overtime_hours, 2),
            "total_records": len(records)
        }

    # ---- Compensation ----

    def get_compensation(self, employee_id):
        """
        Get compensation components for an employee.

        Returns default (zero) values if no compensation is configured.
        """
        comp_data = self._file_manager.read_data(FileManager.COMPENSATION_FILE)

        for comp in comp_data:
            if comp["employee_id"] == employee_id:
                return comp

        # Return default compensation if not configured
        return {
            "employee_id": employee_id,
            "hra": 0,
            "transport_allowance": 0,
            "medical_allowance": 0,
            "other_allowances": 0,
            "performance_bonus": 0,
            "other_deductions": 0
        }

    # ---- Payroll ID Generation ----

    def _generate_payroll_id(self):
        """Generate the next unique payroll ID (e.g., PAY001, PAY002)."""
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        if not payroll_data:
            return "PAY001"

        # Find the highest existing ID number
        max_num = 0
        for record in payroll_data:
            pay_id = record.get("payroll_id", "PAY000")
            try:
                num = int(pay_id.replace("PAY", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                continue

        return f"PAY{max_num + 1:03d}"

    # ---- Duplicate Check ----

    def check_duplicate_payroll(self, employee_id, month, year):
        """Check if payroll already exists for this employee and month."""
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        for record in payroll_data:
            if (record["employee_id"] == employee_id and
                    record["month"] == month and
                    record["year"] == year):
                return True

        return False

    # ---- Main Payroll Generation ----

    def generate_payroll(self, employee, month, year):
        """
        Generate payroll for a single employee.

        **This method demonstrates POLYMORPHISM:**
        It accepts any Employee object (could be SalariedEmployee
        or HourlyEmployee) and calls employee.calculate_salary().
        Python automatically runs the correct version based on the
        actual type of the employee object. We NEVER check the type!

        Args:
            employee: An Employee object (any subclass).
            month: Month number (1-12).
            year: Year number.

        Returns:
            Payroll: A new Payroll object with calculated salary.

        Raises:
            DuplicatePayrollError: If payroll already exists for this month.
        """
        # Check for duplicate payroll
        if self.check_duplicate_payroll(employee.employee_id, month, year):
            raise DuplicatePayrollError(
                f"Payroll already exists for {employee.name} "
                f"for {month}/{year}.")

        # Step 1: Get attendance summary for the month
        attendance_summary = self.get_attendance_summary(
            employee.employee_id, month, year)

        # Step 2: Get compensation components
        compensation = self.get_compensation(employee.employee_id)

        # Step 3: POLYMORPHISM - call calculate_salary()
        # The correct method runs based on the employee's actual type.
        # We don't check if it's Salaried or Hourly - we just call it!
        salary_breakdown = employee.calculate_salary(
            attendance_summary, compensation)

        # Step 4: Generate unique payroll ID
        payroll_id = self._generate_payroll_id()

        # Step 5: Create Payroll object (with SalaryBreakdown - COMPOSITION)
        payroll = Payroll(
            payroll_id=payroll_id,
            employee_id=employee.employee_id,
            employee_name=employee.name,
            department=employee.department,
            designation=employee.designation,
            employment_type=employee.employment_type,
            month=month,
            year=year,
            attendance_summary=attendance_summary,
            salary_breakdown_data=salary_breakdown,
            status="Draft"
        )

        # Step 6: Save to file
        self._file_manager.add_record(
            FileManager.PAYROLL_FILE, payroll.to_dict())

        return payroll

    # ---- Finalize Payroll ----

    def finalize_payroll(self, payroll_id):
        """
        Finalize a payroll record.

        Once finalized, the record is locked and preserves its
        original salary calculation permanently.

        Raises:
            PayrollError: If payroll not found or already finalized.
        """
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        for record in payroll_data:
            if record["payroll_id"] == payroll_id:
                if record["status"] == "Finalized":
                    raise PayrollError("This payroll is already finalized.")
                record["status"] = "Finalized"
                self._file_manager.write_data(
                    FileManager.PAYROLL_FILE, payroll_data)
                return True

        raise PayrollError(f"Payroll {payroll_id} not found.")

    # ---- Payslip Generation ----

    def generate_payslip_text(self, payroll_dict):
        """
        Generate a formatted payslip as plain text.

        Creates a professional-looking payslip string that can be
        displayed in the GUI or saved as a .txt file.

        Args:
            payroll_dict: Payroll record as a dictionary.

        Returns:
            str: Formatted payslip text.
        """
        breakdown = payroll_dict.get("salary_breakdown", {})
        attendance = payroll_dict.get("attendance_summary", {})
        emp_type = payroll_dict.get("employment_type", "Salaried")

        # Get month name (e.g., "October 2026")
        month_name = datetime(
            payroll_dict["year"], payroll_dict["month"], 1
        ).strftime("%B %Y")

        # Build payslip line by line
        lines = []
        lines.append("=" * 60)
        lines.append(f"{'PAYSLIP':^60}")
        lines.append(f"{self.ORGANIZATION_NAME:^60}")
        lines.append("=" * 60)
        lines.append("")

        # --- Employee Information ---
        lines.append(f"  Employee ID     : {payroll_dict['employee_id']}")
        lines.append(f"  Employee Name   : {payroll_dict['employee_name']}")
        lines.append(f"  Department      : {payroll_dict.get('department', '-')}")
        lines.append(f"  Designation     : {payroll_dict.get('designation', '-')}")
        lines.append(f"  Employment Type : {emp_type}")
        lines.append(f"  Payroll Month   : {month_name}")
        lines.append(f"  Payroll ID      : {payroll_dict['payroll_id']}")
        lines.append("")
        lines.append("-" * 60)

        # --- Attendance Summary ---
        lines.append("  ATTENDANCE SUMMARY")
        lines.append("-" * 60)
        lines.append(f"  Present Days        : {attendance.get('present_days', 0)}")
        lines.append(f"  Absent Days         : {attendance.get('absent_days', 0)}")
        lines.append(f"  Half Days           : {attendance.get('half_days', 0)}")
        lines.append(f"  Paid Leaves         : {attendance.get('paid_leaves', 0)}")
        lines.append(f"  Unpaid Leaves       : {attendance.get('unpaid_leaves', 0)}")
        lines.append(f"  Holidays            : {attendance.get('holidays', 0)}")
        lines.append(f"  Total Working Hours : {attendance.get('total_working_hours', 0)}")
        lines.append(f"  Overtime Hours      : {attendance.get('overtime_hours', 0)}")
        lines.append("")
        lines.append("-" * 60)

        # --- Earnings ---
        lines.append("  EARNINGS")
        lines.append("-" * 60)

        if emp_type == "Salaried":
            lines.append(f"  Basic Salary        : Rs. {breakdown.get('basic_salary', 0):>12,.2f}")
        else:
            lines.append(f"  Hourly Rate         : Rs. {breakdown.get('hourly_rate', 0):>12,.2f}")
            lines.append(f"  Regular Hours       :     {breakdown.get('regular_hours', 0):>12}")
            lines.append(f"  Regular Pay         : Rs. {breakdown.get('regular_pay', 0):>12,.2f}")

        lines.append(f"  HRA                 : Rs. {breakdown.get('hra', 0):>12,.2f}")
        lines.append(f"  Transport Allowance : Rs. {breakdown.get('transport_allowance', 0):>12,.2f}")
        lines.append(f"  Medical Allowance   : Rs. {breakdown.get('medical_allowance', 0):>12,.2f}")
        lines.append(f"  Other Allowances    : Rs. {breakdown.get('other_allowances', 0):>12,.2f}")
        lines.append(f"  Performance Bonus   : Rs. {breakdown.get('performance_bonus', 0):>12,.2f}")
        lines.append(f"  Overtime Pay        : Rs. {breakdown.get('overtime_pay', 0):>12,.2f}")
        lines.append(f"                        {'':->32}")
        lines.append(f"  GROSS SALARY        : Rs. {breakdown.get('gross_salary', 0):>12,.2f}")
        lines.append("")
        lines.append("-" * 60)

        # --- Deductions ---
        lines.append("  DEDUCTIONS")
        lines.append("-" * 60)

        if emp_type == "Salaried":
            lines.append(f"  Unpaid Leave Ded.   : Rs. {breakdown.get('unpaid_leave_deduction', 0):>12,.2f}")
            lines.append(f"  Absence Deduction   : Rs. {breakdown.get('absence_deduction', 0):>12,.2f}")

        lines.append(f"  Other Deductions    : Rs. {breakdown.get('other_deductions', 0):>12,.2f}")
        lines.append(f"                        {'':->32}")
        lines.append(f"  TOTAL DEDUCTIONS    : Rs. {breakdown.get('total_deductions', 0):>12,.2f}")
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"  NET SALARY          : Rs. {breakdown.get('net_salary', 0):>12,.2f}")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"  Payment Status : {payroll_dict.get('payment_status', 'Unpaid')}")
        lines.append(f"  Payroll Status : {payroll_dict.get('status', 'Draft')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("  This is a system-generated payslip.")
        lines.append(f"  Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-" * 60)

        return "\n".join(lines)

    def save_payslip(self, payroll_dict):
        """
        Generate and save a payslip as a .txt file.

        Returns:
            str: File path of the saved payslip.
        """
        content = self.generate_payslip_text(payroll_dict)

        filename = (f"payslip_{payroll_dict['employee_id']}_"
                    f"{payroll_dict['month']:02d}_{payroll_dict['year']}.txt")

        return self._file_manager.save_payslip(filename, content)

    # ---- Payment Processing ----

    def record_payment(self, payroll_id, payment_method, transaction_ref=""):
        """
        Record a payment for a finalized payroll.

        Creates a Payment record and updates the payroll status to 'Paid'.

        Raises:
            PayrollNotFinalizedError: If payroll is not finalized.
            PayrollError: If payroll not found or already paid.
        """
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        # Find the payroll record
        payroll_record = None
        for record in payroll_data:
            if record["payroll_id"] == payroll_id:
                payroll_record = record
                break

        if payroll_record is None:
            raise PayrollError(f"Payroll {payroll_id} not found.")

        if payroll_record["status"] != "Finalized":
            raise PayrollNotFinalizedError(
                "Payroll must be finalized before recording payment.")

        if payroll_record["payment_status"] == "Paid":
            raise PayrollError("This payroll has already been paid.")

        # Generate unique payment ID
        payments = self._file_manager.read_data(FileManager.PAYMENTS_FILE)
        if payments:
            max_num = 0
            for p in payments:
                try:
                    num = int(p["payment_id"].replace("PMT", ""))
                    if num > max_num:
                        max_num = num
                except (ValueError, KeyError):
                    continue
            payment_id = f"PMT{max_num + 1:03d}"
        else:
            payment_id = "PMT001"

        # Create payment record
        payment = Payment(
            payment_id=payment_id,
            payroll_id=payroll_id,
            employee_id=payroll_record["employee_id"],
            amount=payroll_record["salary_breakdown"]["net_salary"],
            payment_date=datetime.now().strftime("%Y-%m-%d"),
            payment_method=payment_method,
            transaction_ref=transaction_ref
        )

        # Save payment record
        self._file_manager.add_record(
            FileManager.PAYMENTS_FILE, payment.to_dict())

        # Update payroll payment status to "Paid"
        payroll_record["payment_status"] = "Paid"
        self._file_manager.write_data(FileManager.PAYROLL_FILE, payroll_data)

        return payment

    # ---- Query Methods ----

    def get_payroll_summary(self, month, year):
        """Get all payroll records for a specific month and year."""
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        results = []
        for record in payroll_data:
            if record["month"] == month and record["year"] == year:
                results.append(record)
        return results

    def get_employee_payroll_history(self, employee_id):
        """Get all payroll records for a specific employee."""
        return self._file_manager.find_records(
            FileManager.PAYROLL_FILE, "employee_id", employee_id)

    def get_employee_payment_history(self, employee_id):
        """Get all payment records for a specific employee."""
        return self._file_manager.find_records(
            FileManager.PAYMENTS_FILE, "employee_id", employee_id)

    def get_pending_payments(self):
        """Get all finalized but unpaid payroll records."""
        payroll_data = self._file_manager.read_data(FileManager.PAYROLL_FILE)

        pending = []
        for record in payroll_data:
            if (record["status"] == "Finalized" and
                    record["payment_status"] == "Unpaid"):
                pending.append(record)
        return pending

    def get_completed_payments(self):
        """Get all payment records (completed payments)."""
        return self._file_manager.read_data(FileManager.PAYMENTS_FILE)
