"""
employee.py - Employee Class Hierarchy

This module defines the Employee class hierarchy for the Payroll System.

Classes:
    Employee         - Abstract base class for all employees (Abstraction)
    SalariedEmployee - Employee with fixed monthly salary (Inheritance)
    HourlyEmployee   - Employee paid per hour worked (Inheritance)

OOP Concepts Demonstrated:
    - Abstraction    : Employee is abstract; cannot be instantiated directly
    - Inheritance    : SalariedEmployee and HourlyEmployee extend Employee
    - Polymorphism   : Both subclasses override calculate_salary() differently
    - Encapsulation  : Private attributes with property-based access
    - Constructors   : __init__ with super() calls
"""

from abc import ABC, abstractmethod


# ============================================================
# Custom Exceptions
# ============================================================

class EmployeeError(Exception):
    """Base exception for employee-related errors."""
    pass


class InvalidSalaryError(EmployeeError):
    """Raised when salary or hourly rate is invalid."""
    pass


class InvalidEmployeeDataError(EmployeeError):
    """Raised when employee data is incomplete or invalid."""
    pass


# ============================================================
# Employee Base Class (Abstract)
# ============================================================

class Employee(ABC):
    """
    Abstract base class representing a generic employee.

    This class cannot be instantiated directly. You must create
    either a SalariedEmployee or an HourlyEmployee.

    This demonstrates ABSTRACTION - we define what every employee
    can do (calculate_salary), without specifying how each type does it.

    Attributes:
        _employee_id   : Unique identifier (e.g., "EMP001")
        _name          : Full name of the employee
        _email         : Email address
        _contact       : Contact number
        _department    : Department name
        _designation   : Job title
        _joining_date  : Date of joining (YYYY-MM-DD)
        _employment_type : "Salaried" or "Hourly"
        _status        : "Active" or "Inactive"
    """

    # Configuration constants used in salary calculations
    STANDARD_WORKING_HOURS_PER_DAY = 8
    STANDARD_WORKING_DAYS_PER_MONTH = 22
    OVERTIME_MULTIPLIER = 1.5

    def __init__(self, employee_id, name, email, contact, department,
                 designation, joining_date, employment_type, status="Active"):
        """
        Initialize common employee attributes.

        Demonstrates: Constructor, Encapsulation (private attributes)

        Raises:
            InvalidEmployeeDataError: If required fields are missing.
        """
        if not employee_id or not name:
            raise InvalidEmployeeDataError("Employee ID and Name are required.")

        self._employee_id = employee_id
        self._name = name
        self._email = email
        self._contact = contact
        self._department = department
        self._designation = designation
        self._joining_date = joining_date
        self._employment_type = employment_type   # "Salaried" or "Hourly"
        self._status = status                     # "Active" or "Inactive"

    # ---- Properties (Encapsulation - controlled access) ----

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise InvalidEmployeeDataError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = value

    @property
    def designation(self):
        return self._designation

    @designation.setter
    def designation(self, value):
        self._designation = value

    @property
    def joining_date(self):
        return self._joining_date

    @property
    def employment_type(self):
        return self._employment_type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ("Active", "Inactive"):
            raise InvalidEmployeeDataError("Status must be 'Active' or 'Inactive'.")
        self._status = value

    # ---- Abstract Methods (must be implemented by subclasses) ----

    @abstractmethod
    def calculate_salary(self, attendance_summary, compensation):
        """
        Calculate the monthly salary for this employee.

        This is an ABSTRACT METHOD. Each employee type provides its
        own implementation. This is the foundation for POLYMORPHISM.

        Args:
            attendance_summary (dict): Monthly attendance data with keys:
                present_days, absent_days, half_days, paid_leaves,
                unpaid_leaves, holidays, total_working_hours, overtime_hours
            compensation (dict): Compensation components with keys:
                hra, transport_allowance, medical_allowance,
                other_allowances, performance_bonus, other_deductions

        Returns:
            dict: Complete salary breakdown with all components.
        """
        pass

    @abstractmethod
    def get_base_pay_info(self):
        """Return a string describing the base pay (salary or hourly rate)."""
        pass

    # ---- Common Methods ----

    def to_dict(self):
        """Convert employee to a dictionary for JSON storage."""
        return {
            "employee_id": self._employee_id,
            "name": self._name,
            "email": self._email,
            "contact": self._contact,
            "department": self._department,
            "designation": self._designation,
            "joining_date": self._joining_date,
            "employment_type": self._employment_type,
            "status": self._status
        }

    def __str__(self):
        return f"{self._employee_id} - {self._name} ({self._employment_type})"


# ============================================================
# SalariedEmployee (Inherits from Employee)
# ============================================================

class SalariedEmployee(Employee):
    """
    An employee who receives a fixed monthly salary.

    Inherits all common attributes from Employee and adds basic_salary.
    Overrides calculate_salary() with salaried-specific logic.

    Demonstrates: Inheritance, Method Overriding, super() usage

    Salary Formula:
        Gross  = Basic Salary + Allowances + Bonus + Overtime Pay
        Deductions = Unpaid Leave Ded. + Absence Ded. + Other Ded.
        Net    = Gross - Deductions
    """

    def __init__(self, employee_id, name, email, contact, department,
                 designation, joining_date, basic_salary, status="Active"):
        """
        Initialize a SalariedEmployee.

        Calls the parent constructor using super() for common attributes,
        then sets the basic_salary specific to salaried employees.

        Raises:
            InvalidSalaryError: If basic_salary is negative.
        """
        # Call parent constructor (demonstrates super())
        super().__init__(
            employee_id, name, email, contact, department,
            designation, joining_date, "Salaried", status
        )

        if basic_salary < 0:
            raise InvalidSalaryError("Basic salary cannot be negative.")
        self.__basic_salary = basic_salary  # Name-mangled private attribute

    # ---- Properties ----

    @property
    def basic_salary(self):
        """Get the basic monthly salary."""
        return self.__basic_salary

    @basic_salary.setter
    def basic_salary(self, value):
        """Set the basic salary with validation."""
        if value < 0:
            raise InvalidSalaryError("Basic salary cannot be negative.")
        self.__basic_salary = value

    def get_base_pay_info(self):
        """Return base pay description for display."""
        return f"Monthly Salary: Rs.{self.__basic_salary:,.2f}"

    # ---- Salary Calculation Helper Methods ----
    # Each step is a separate method for clarity and easy explanation.

    def _calculate_daily_rate(self):
        """Daily Rate = Basic Salary / Standard Working Days per Month."""
        return round(self.__basic_salary / self.STANDARD_WORKING_DAYS_PER_MONTH, 2)

    def _calculate_hourly_rate(self):
        """Hourly Rate = Basic Salary / (Working Days × Hours per Day)."""
        total_monthly_hours = (self.STANDARD_WORKING_DAYS_PER_MONTH *
                               self.STANDARD_WORKING_HOURS_PER_DAY)
        return round(self.__basic_salary / total_monthly_hours, 2)

    def _calculate_unpaid_leave_deduction(self, unpaid_leave_days):
        """Deduction = Daily Rate × Number of Unpaid Leave Days."""
        daily_rate = self._calculate_daily_rate()
        return round(daily_rate * unpaid_leave_days, 2)

    def _calculate_absence_deduction(self, absent_days, half_days):
        """
        Deduction for absences and half-days.
        Absent days get full daily rate deduction.
        Half-days get half daily rate deduction.
        """
        daily_rate = self._calculate_daily_rate()
        return round(daily_rate * (absent_days + half_days * 0.5), 2)

    def _calculate_overtime_pay(self, overtime_hours):
        """Overtime Pay = OT Hours × Hourly Rate × OT Multiplier (1.5x)."""
        hourly_rate = self._calculate_hourly_rate()
        return round(overtime_hours * hourly_rate * self.OVERTIME_MULTIPLIER, 2)

    # ---- Main Salary Calculation (POLYMORPHISM) ----

    def calculate_salary(self, attendance_summary, compensation):
        """
        Calculate monthly salary for a SALARIED employee.

        This OVERRIDES the abstract method from the Employee base class.
        When PayrollManager calls employee.calculate_salary(), Python
        automatically runs THIS version for SalariedEmployee objects.
        This is RUNTIME POLYMORPHISM.

        Returns:
            dict: Complete salary breakdown.
        """
        # --- Extract attendance data ---
        unpaid_leaves = attendance_summary.get("unpaid_leaves", 0)
        absent_days = attendance_summary.get("absent_days", 0)
        half_days = attendance_summary.get("half_days", 0)
        overtime_hours = attendance_summary.get("overtime_hours", 0)

        # --- Extract compensation components ---
        hra = compensation.get("hra", 0)
        transport_allowance = compensation.get("transport_allowance", 0)
        medical_allowance = compensation.get("medical_allowance", 0)
        other_allowances = compensation.get("other_allowances", 0)
        performance_bonus = compensation.get("performance_bonus", 0)
        other_deductions = compensation.get("other_deductions", 0)

        # --- Calculate each component separately ---
        total_allowances = round(hra + transport_allowance +
                                 medical_allowance + other_allowances, 2)
        overtime_pay = self._calculate_overtime_pay(overtime_hours)
        unpaid_leave_deduction = self._calculate_unpaid_leave_deduction(unpaid_leaves)
        absence_deduction = self._calculate_absence_deduction(absent_days, half_days)

        # --- Calculate gross and net salary ---
        gross_salary = round(self.__basic_salary + total_allowances +
                             performance_bonus + overtime_pay, 2)
        total_deductions = round(unpaid_leave_deduction + absence_deduction +
                                 other_deductions, 2)
        net_salary = round(gross_salary - total_deductions, 2)

        # --- Return complete breakdown ---
        # This dictionary becomes part of the Payroll object (COMPOSITION)
        return {
            "basic_salary": self.__basic_salary,
            "hra": hra,
            "transport_allowance": transport_allowance,
            "medical_allowance": medical_allowance,
            "other_allowances": other_allowances,
            "total_allowances": total_allowances,
            "performance_bonus": performance_bonus,
            "overtime_hours": overtime_hours,
            "overtime_pay": overtime_pay,
            "unpaid_leave_deduction": unpaid_leave_deduction,
            "absence_deduction": absence_deduction,
            "other_deductions": other_deductions,
            "total_deductions": total_deductions,
            "gross_salary": gross_salary,
            "net_salary": net_salary
        }

    def to_dict(self):
        """Convert to dictionary, adding basic_salary to common fields."""
        data = super().to_dict()
        data["basic_salary"] = self.__basic_salary
        return data

    def __str__(self):
        return (f"{self._employee_id} - {self._name} "
                f"(Salaried: Rs.{self.__basic_salary:,.2f}/month)")


# ============================================================
# HourlyEmployee (Inherits from Employee)
# ============================================================

class HourlyEmployee(Employee):
    """
    An employee who is paid based on hours worked.

    Inherits all common attributes from Employee and adds hourly_rate.
    Overrides calculate_salary() with hourly-specific logic.

    Demonstrates: Inheritance, Method Overriding, super() usage

    Salary Formula:
        Regular Pay  = Regular Hours × Hourly Rate
        Overtime Pay = OT Hours × Hourly Rate × OT Multiplier
        Net = Regular Pay + OT Pay + Allowances + Bonus - Deductions
    """

    def __init__(self, employee_id, name, email, contact, department,
                 designation, joining_date, hourly_rate, status="Active"):
        """
        Initialize an HourlyEmployee.

        Calls the parent constructor using super() for common attributes,
        then sets the hourly_rate specific to hourly employees.

        Raises:
            InvalidSalaryError: If hourly_rate is negative.
        """
        super().__init__(
            employee_id, name, email, contact, department,
            designation, joining_date, "Hourly", status
        )

        if hourly_rate < 0:
            raise InvalidSalaryError("Hourly rate cannot be negative.")
        self.__hourly_rate = hourly_rate

    # ---- Properties ----

    @property
    def hourly_rate(self):
        """Get the hourly rate."""
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        """Set the hourly rate with validation."""
        if value < 0:
            raise InvalidSalaryError("Hourly rate cannot be negative.")
        self.__hourly_rate = value

    def get_base_pay_info(self):
        """Return base pay description for display."""
        return f"Hourly Rate: Rs.{self.__hourly_rate:,.2f}/hour"

    # ---- Salary Calculation Helper Methods ----

    def _calculate_regular_pay(self, regular_hours):
        """Regular Pay = Regular Working Hours × Hourly Rate."""
        return round(regular_hours * self.__hourly_rate, 2)

    def _calculate_overtime_pay(self, overtime_hours):
        """Overtime Pay = OT Hours × Hourly Rate × OT Multiplier (1.5x)."""
        return round(overtime_hours * self.__hourly_rate * self.OVERTIME_MULTIPLIER, 2)

    # ---- Main Salary Calculation (POLYMORPHISM) ----

    def calculate_salary(self, attendance_summary, compensation):
        """
        Calculate monthly salary for an HOURLY employee.

        This OVERRIDES the abstract method from the Employee base class.
        Different calculation logic compared to SalariedEmployee.
        This is POLYMORPHISM - same method name, different behavior.

        Hourly employees are paid for actual hours worked.
        They do not get unpaid leave or absence deductions because
        they simply don't get paid for hours they didn't work.

        Returns:
            dict: Complete salary breakdown.
        """
        # --- Extract attendance data ---
        total_working_hours = attendance_summary.get("total_working_hours", 0)
        overtime_hours = attendance_summary.get("overtime_hours", 0)

        # Regular hours = total hours worked minus overtime hours
        regular_hours = total_working_hours - overtime_hours

        # --- Extract compensation components ---
        hra = compensation.get("hra", 0)
        transport_allowance = compensation.get("transport_allowance", 0)
        medical_allowance = compensation.get("medical_allowance", 0)
        other_allowances = compensation.get("other_allowances", 0)
        performance_bonus = compensation.get("performance_bonus", 0)
        other_deductions = compensation.get("other_deductions", 0)

        # --- Calculate each component ---
        regular_pay = self._calculate_regular_pay(regular_hours)
        overtime_pay = self._calculate_overtime_pay(overtime_hours)
        total_allowances = round(hra + transport_allowance +
                                 medical_allowance + other_allowances, 2)

        # --- Calculate gross and net ---
        gross_salary = round(regular_pay + overtime_pay +
                             total_allowances + performance_bonus, 2)
        net_salary = round(gross_salary - other_deductions, 2)

        # --- Return complete breakdown ---
        return {
            "hourly_rate": self.__hourly_rate,
            "regular_hours": regular_hours,
            "regular_pay": regular_pay,
            "hra": hra,
            "transport_allowance": transport_allowance,
            "medical_allowance": medical_allowance,
            "other_allowances": other_allowances,
            "total_allowances": total_allowances,
            "performance_bonus": performance_bonus,
            "overtime_hours": overtime_hours,
            "overtime_pay": overtime_pay,
            "other_deductions": other_deductions,
            "total_deductions": other_deductions,
            "gross_salary": gross_salary,
            "net_salary": net_salary
        }

    def to_dict(self):
        """Convert to dictionary, adding hourly_rate to common fields."""
        data = super().to_dict()
        data["hourly_rate"] = self.__hourly_rate
        return data

    def __str__(self):
        return (f"{self._employee_id} - {self._name} "
                f"(Hourly: Rs.{self.__hourly_rate:,.2f}/hr)")


# ============================================================
# Factory Function - Creates the right Employee type from data
# ============================================================

def create_employee_from_dict(data):
    """
    Create the correct Employee subclass from a dictionary.

    Used when loading employee data from JSON files.
    Based on the 'employment_type' field, it creates either
    a SalariedEmployee or HourlyEmployee object.

    Args:
        data (dict): Employee data loaded from JSON.

    Returns:
        Employee: A SalariedEmployee or HourlyEmployee object.

    Raises:
        InvalidEmployeeDataError: If employment_type is unknown.
    """
    emp_type = data.get("employment_type", "Salaried")

    if emp_type == "Salaried":
        return SalariedEmployee(
            employee_id=data["employee_id"],
            name=data["name"],
            email=data.get("email", ""),
            contact=data.get("contact", ""),
            department=data.get("department", ""),
            designation=data.get("designation", ""),
            joining_date=data.get("joining_date", ""),
            basic_salary=data.get("basic_salary", 0),
            status=data.get("status", "Active")
        )
    elif emp_type == "Hourly":
        return HourlyEmployee(
            employee_id=data["employee_id"],
            name=data["name"],
            email=data.get("email", ""),
            contact=data.get("contact", ""),
            department=data.get("department", ""),
            designation=data.get("designation", ""),
            joining_date=data.get("joining_date", ""),
            hourly_rate=data.get("hourly_rate", 0),
            status=data.get("status", "Active")
        )
    else:
        raise InvalidEmployeeDataError(f"Unknown employment type: {emp_type}")
