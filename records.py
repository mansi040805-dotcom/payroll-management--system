"""
records.py - Attendance, Leave, and Payment Record Classes

This module defines classes for managing employee records.

Classes:
    Attendance - Tracks daily attendance with check-in/out times
    Leave      - Manages leave requests and approvals
    Payment    - Records payment transactions for finalized payroll

OOP Concepts Demonstrated:
    - Classes and Objects  : Each record type is a separate class
    - Encapsulation        : Private attributes with validation
    - Association          : Records link to employees via employee_id
    - Exception Handling   : Custom exceptions for invalid data
"""

from datetime import datetime


# ============================================================
# Custom Exceptions
# ============================================================

class RecordError(Exception):
    """Base exception for record-related errors."""
    pass


class DuplicateAttendanceError(RecordError):
    """Raised when attendance already exists for an employee on a date."""
    pass


class InvalidAttendanceError(RecordError):
    """Raised when attendance data is invalid."""
    pass


class InvalidLeaveError(RecordError):
    """Raised when leave data is invalid."""
    pass


# ============================================================
# Attendance Class
# ============================================================

class Attendance:
    """
    Represents a single day's attendance record for an employee.

    Each Attendance object is ASSOCIATED with an Employee through
    the employee_id field. This demonstrates ASSOCIATION - an employee
    HAS attendance records, but they are separate objects.

    Attributes:
        _employee_id        : ID of the employee this record belongs to
        _date               : Date of attendance (YYYY-MM-DD format)
        _check_in           : Check-in time (HH:MM format)
        _check_out          : Check-out time (HH:MM format)
        _break_duration     : Break duration in hours (e.g., 1.0)
        _status             : Attendance status (Present, Absent, etc.)
        _total_working_hours: Calculated working hours for the day
    """

    # Valid attendance statuses
    VALID_STATUSES = [
        "Present", "Absent", "Half-day",
        "Paid Leave", "Unpaid Leave", "Holiday"
    ]

    def __init__(self, employee_id, date, check_in="", check_out="",
                 break_duration=0, status="Present"):
        """
        Initialize an attendance record.

        Working hours are automatically calculated from check-in,
        check-out, and break duration.

        Raises:
            InvalidAttendanceError: If required fields are missing or
                                    status is not valid.
        """
        if not employee_id:
            raise InvalidAttendanceError("Employee ID is required.")
        if not date:
            raise InvalidAttendanceError("Date is required.")
        if status not in self.VALID_STATUSES:
            raise InvalidAttendanceError(
                f"Invalid status '{status}'. "
                f"Must be one of: {', '.join(self.VALID_STATUSES)}")

        self._employee_id = employee_id
        self._date = date
        self._check_in = check_in
        self._check_out = check_out
        self._break_duration = break_duration   # In hours
        self._status = status
        # Auto-calculate working hours based on times
        self._total_working_hours = self.calculate_working_hours()

    # ---- Properties ----

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def date(self):
        return self._date

    @property
    def check_in(self):
        return self._check_in

    @property
    def check_out(self):
        return self._check_out

    @property
    def break_duration(self):
        return self._break_duration

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise InvalidAttendanceError(
                f"Invalid status. Must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value

    @property
    def total_working_hours(self):
        return self._total_working_hours

    # ---- Methods ----

    def calculate_working_hours(self):
        """
        Calculate total working hours from check-in and check-out times.

        Formula: Working Hours = (Check-out - Check-in) - Break Duration

        Returns 0 for non-working statuses (Absent, Leave, Holiday).
        """
        # No working hours for these statuses
        if self._status in ["Absent", "Paid Leave", "Unpaid Leave", "Holiday"]:
            return 0.0

        # If times are missing, return 0
        if not self._check_in or not self._check_out:
            return 0.0

        try:
            check_in_time = datetime.strptime(self._check_in, "%H:%M")
            check_out_time = datetime.strptime(self._check_out, "%H:%M")

            # Calculate difference in hours
            difference_seconds = (check_out_time - check_in_time).total_seconds()
            difference_hours = difference_seconds / 3600

            # Subtract break duration
            working_hours = difference_hours - self._break_duration

            # Working hours cannot be negative
            return round(max(0, working_hours), 2)
        except ValueError:
            return 0.0

    def to_dict(self):
        """Convert attendance record to dictionary for JSON storage."""
        return {
            "employee_id": self._employee_id,
            "date": self._date,
            "check_in": self._check_in,
            "check_out": self._check_out,
            "break_duration": self._break_duration,
            "status": self._status,
            "total_working_hours": self._total_working_hours
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Attendance object from a dictionary (loaded from JSON)."""
        return cls(
            employee_id=data["employee_id"],
            date=data["date"],
            check_in=data.get("check_in", ""),
            check_out=data.get("check_out", ""),
            break_duration=data.get("break_duration", 0),
            status=data.get("status", "Present")
        )

    def __str__(self):
        return (f"Attendance({self._employee_id}, {self._date}, "
                f"{self._status}, {self._total_working_hours}hrs)")


# ============================================================
# Leave Class
# ============================================================

class Leave:
    """
    Represents a leave request for an employee.

    Leave records track requests separately from daily attendance.
    When a leave is approved, the corresponding attendance records
    should be marked as 'Paid Leave' or 'Unpaid Leave'.

    Demonstrates: Encapsulation, Association with Employee
    """

    VALID_TYPES = ["Paid Leave", "Unpaid Leave"]
    VALID_STATUSES = ["Pending", "Approved", "Rejected"]

    def __init__(self, leave_id, employee_id, start_date, end_date,
                 leave_type, reason="", status="Pending"):
        """
        Initialize a leave record.

        Raises:
            InvalidLeaveError: If leave_type or status is invalid.
        """
        if leave_type not in self.VALID_TYPES:
            raise InvalidLeaveError(
                f"Leave type must be one of: {', '.join(self.VALID_TYPES)}")
        if status not in self.VALID_STATUSES:
            raise InvalidLeaveError(
                f"Status must be one of: {', '.join(self.VALID_STATUSES)}")

        self._leave_id = leave_id
        self._employee_id = employee_id
        self._start_date = start_date
        self._end_date = end_date
        self._leave_type = leave_type
        self._reason = reason
        self._status = status

    # ---- Properties ----

    @property
    def leave_id(self):
        return self._leave_id

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def leave_type(self):
        return self._leave_type

    @property
    def reason(self):
        return self._reason

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise InvalidLeaveError(
                f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value

    # ---- Methods ----

    def get_number_of_days(self):
        """Calculate the number of leave days (inclusive of start and end)."""
        try:
            start = datetime.strptime(self._start_date, "%Y-%m-%d")
            end = datetime.strptime(self._end_date, "%Y-%m-%d")
            return (end - start).days + 1
        except ValueError:
            return 0

    def to_dict(self):
        """Convert leave record to dictionary for JSON storage."""
        return {
            "leave_id": self._leave_id,
            "employee_id": self._employee_id,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "leave_type": self._leave_type,
            "reason": self._reason,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Leave object from a dictionary."""
        return cls(
            leave_id=data["leave_id"],
            employee_id=data["employee_id"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            leave_type=data["leave_type"],
            reason=data.get("reason", ""),
            status=data.get("status", "Pending")
        )

    def __str__(self):
        return (f"Leave({self._leave_id}, {self._employee_id}, "
                f"{self._leave_type}, {self._status})")


# ============================================================
# Payment Class
# ============================================================

class Payment:
    """
    Represents a payment record linked to a finalized payroll.

    Demonstrates: Association (linked to both Employee and Payroll)

    A Payment is created when an administrator marks a finalized
    payroll as 'Paid'. It records the payment details like method,
    date, and transaction reference.
    """

    VALID_METHODS = ["UPI", "Bank Transfer", "Cash", "Cheque"]

    def __init__(self, payment_id, payroll_id, employee_id, amount,
                 payment_date, payment_method, transaction_ref=""):
        """Initialize a payment record."""
        self._payment_id = payment_id
        self._payroll_id = payroll_id
        self._employee_id = employee_id
        self._amount = amount
        self._payment_date = payment_date
        self._payment_method = payment_method
        self._transaction_ref = transaction_ref

    # ---- Properties ----

    @property
    def payment_id(self):
        return self._payment_id

    @property
    def payroll_id(self):
        return self._payroll_id

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def amount(self):
        return self._amount

    @property
    def payment_date(self):
        return self._payment_date

    @property
    def payment_method(self):
        return self._payment_method

    @property
    def transaction_ref(self):
        return self._transaction_ref

    # ---- Methods ----

    def to_dict(self):
        """Convert payment record to dictionary for JSON storage."""
        return {
            "payment_id": self._payment_id,
            "payroll_id": self._payroll_id,
            "employee_id": self._employee_id,
            "amount": self._amount,
            "payment_date": self._payment_date,
            "payment_method": self._payment_method,
            "transaction_ref": self._transaction_ref
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Payment object from a dictionary."""
        return cls(
            payment_id=data["payment_id"],
            payroll_id=data["payroll_id"],
            employee_id=data["employee_id"],
            amount=data["amount"],
            payment_date=data["payment_date"],
            payment_method=data["payment_method"],
            transaction_ref=data.get("transaction_ref", "")
        )

    def __str__(self):
        return (f"Payment({self._payment_id}, {self._employee_id}, "
                f"Rs.{self._amount:,.2f}, {self._payment_method})")
