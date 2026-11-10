"""
gui.py - Tkinter Graphical User Interface for Payroll Management System

This module provides the desktop user interface using Tkinter and ttk.
It contains 8 main functional tabs:
1. Dashboard
2. Employee Management
3. Attendance Management
4. Leave Management
5. Compensation Management
6. Payroll Processing
7. Payslips
8. Payment History

OOP Concepts Demonstrated:
- Separation of Concerns: GUI coordinates user events with backend classes
- Exception Handling: Validates user input and catches domain errors cleanly
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from file_manager import FileManager
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


class PayrollApp:
    """
    Main Application GUI Class for Payroll & Compensation Management System.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Payroll & Compensation Management System")
        self.root.geometry("1200x720")
        self.root.minsize(1050, 650)

        # Initialize Backend Managers
        self.file_manager = FileManager()
        self.payroll_manager = PayrollManager(self.file_manager)

        # Center the window
        self._center_window(1200, 720)

        # Create Top Title Banner
        self._create_header()

        # Create Notebook Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Build each tab
        self._build_dashboard_tab()
        self._build_employee_tab()
        self._build_attendance_tab()
        self._build_leave_tab()
        self._build_compensation_tab()
        self._build_payroll_tab()
        self._build_payslips_tab()
        self._build_payment_tab()

        # Initial data refresh across tabs
        self.refresh_all_data()

    def _center_window(self, width, height):
        """Center the main window on screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_header(self):
        """Header Banner for the application."""
        header_frame = tk.Frame(self.root, bg="#1E3A8A", height=50)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="TechCorp Payroll & Compensation Management System",
            fg="white",
            bg="#1E3A8A",
            font=("Segoe UI", 15, "bold")
        )
        title_lbl.pack(side=tk.LEFT, padx=15, pady=8)

        subtitle_lbl = tk.Label(
            header_frame,
            text="OOP Semester Project",
            fg="#93C5FD",
            bg="#1E3A8A",
            font=("Segoe UI", 10, "italic")
        )
        subtitle_lbl.pack(side=tk.RIGHT, padx=15, pady=8)

    def refresh_all_data(self):
        """Refreshes common data sources across tabs."""
        self._populate_employee_combos()
        self._refresh_dashboard_stats()

    def _get_active_employee_ids(self):
        """Helper to get list of active employee IDs."""
        employees = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        return [emp["employee_id"] for emp in employees if emp.get("status") == "Active"]

    def _get_all_employee_ids(self):
        """Helper to get all employee IDs regardless of status."""
        employees = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        return [emp["employee_id"] for emp in employees]

    def _get_employee_name(self, employee_id):
        """Lookup employee name by ID."""
        emp = self.file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", employee_id)
        return emp["name"] if emp else "Unknown"

    def _populate_employee_combos(self):
        """Update employee ID combo boxes in all relevant tabs."""
        active_ids = self._get_active_employee_ids()
        all_ids = self._get_all_employee_ids()

        if hasattr(self, "att_emp_combo"):
            self.att_emp_combo["values"] = active_ids
            self.att_filter_emp_combo["values"] = ["All"] + all_ids
        if hasattr(self, "leave_emp_combo"):
            self.leave_emp_combo["values"] = active_ids
        if hasattr(self, "comp_emp_combo"):
            self.comp_emp_combo["values"] = active_ids
        if hasattr(self, "ps_emp_combo"):
            self.ps_emp_combo["values"] = all_ids
        if hasattr(self, "pmt_filter_emp_combo"):
            self.pmt_filter_emp_combo["values"] = ["All"] + all_ids

    # ============================================================
    # 1. DASHBOARD TAB
    # ============================================================
    def _build_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Dashboard ")

        # Top controls
        top_bar = ttk.Frame(tab, padding=10)
        top_bar.pack(fill=tk.X)

        ttk.Label(top_bar, text="Overview & Operational Metrics", font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(top_bar, text="Refresh Dashboard", command=self._refresh_dashboard_stats).pack(side=tk.RIGHT)

        # Card Container
        cards_frame = ttk.Frame(tab, padding=15)
        cards_frame.pack(fill=tk.X)

        self.card_emp_val = tk.StringVar(value="0")
        self.card_payroll_val = tk.StringVar(value="Rs. 0.00")
        self.card_pending_val = tk.StringVar(value="0")
        self.card_completed_val = tk.StringVar(value="0")

        self._create_stat_card(cards_frame, "Total Active Employees", self.card_emp_val, "#2563EB", 0)
        self._create_stat_card(cards_frame, "Latest Month Payroll", self.card_payroll_val, "#059669", 1)
        self._create_stat_card(cards_frame, "Pending Payments", self.card_pending_val, "#DC2626", 2)
        self._create_stat_card(cards_frame, "Completed Payments", self.card_completed_val, "#7C3AED", 3)

        # Information & Guide Section
        info_frame = ttk.LabelFrame(tab, text="Quick Academic Project Guide & Demonstration Flow", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        guide_text = (
            "Welcome to the Payroll & Compensation Management System (OOP Semester Project)!\n\n"
            "Key OOP Concepts Demonstrated in this System:\n"
            "• Inheritance & Polymorphism: SalariedEmployee and HourlyEmployee derive from Employee and implement calculate_salary().\n"
            "• Composition: Each Payroll instance owns its SalaryBreakdown object.\n"
            "• Association & Aggregation: Attendance & Payment associate with Employee via employee_id; PayrollManager uses FileManager.\n"
            "• Encapsulation: Attributes use protected/private conventions (_attr, __attr) with validation properties.\n"
            "• File Handling & Persistence: All state is maintained in JSON records under the data/ directory.\n\n"
            "Recommended Viva Demonstration Flow:\n"
            "1. Employee Management: View sample salaried & hourly employees, or add a new one.\n"
            "2. Attendance Management: Check daily attendance records with overtime & leave statuses.\n"
            "3. Leave Management: View or approve/reject leave requests.\n"
            "4. Compensation Management: Customize allowances and performance bonuses.\n"
            "5. Payroll Processing: Select 10 / 2026, click 'Generate Payroll' -> observe polymorphic calculation.\n"
            "6. Payslips: Preview and export formatted payslips as text files.\n"
            "7. Payment History: Mark finalized payroll as Paid (UPI, Bank Transfer, etc.) and view history."
        )

        lbl = tk.Label(info_frame, text=guide_text, justify=tk.LEFT, anchor="nw", font=("Segoe UI", 10), padx=5, pady=5)
        lbl.pack(fill=tk.BOTH, expand=True)

    def _create_stat_card(self, parent, title, var, color, col_idx):
        card = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=2, padx=15, pady=15)
        card.grid(row=0, column=col_idx, padx=10, pady=5, sticky="nsew")
        parent.grid_columnconfigure(col_idx, weight=1)

        t_lbl = tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#4B5563", bg="white")
        t_lbl.pack(anchor="w")

        v_lbl = tk.Label(card, textvariable=var, font=("Segoe UI", 16, "bold"), fg=color, bg="white")
        v_lbl.pack(anchor="w", pady=(8, 0))

    def _refresh_dashboard_stats(self):
        """Update metrics shown on the dashboard."""
        employees = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        active_count = sum(1 for e in employees if e.get("status") == "Active")
        self.card_emp_val.set(str(active_count))

        payrolls = self.file_manager.read_data(FileManager.PAYROLL_FILE)
        if payrolls:
            # Sum up net salary of the last batch of payroll records
            latest_month = payrolls[-1].get("month")
            latest_year = payrolls[-1].get("year")
            month_payrolls = [p for p in payrolls if p.get("month") == latest_month and p.get("year") == latest_year]
            total_net = sum(p.get("salary_breakdown", {}).get("net_salary", 0) for p in month_payrolls)
            self.card_payroll_val.set(f"Rs. {total_net:,.2f} ({latest_month:02d}/{latest_year})")
        else:
            self.card_payroll_val.set("Rs. 0.00")

        pending = self.payroll_manager.get_pending_payments()
        self.card_pending_val.set(str(len(pending)))

        completed = self.payroll_manager.get_completed_payments()
        self.card_completed_val.set(str(len(completed)))

    # ============================================================
    # 2. EMPLOYEE MANAGEMENT TAB
    # ============================================================
    def _build_employee_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Employee Management ")

        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Form Frame
        form_frame = ttk.LabelFrame(paned, text="Employee Details Form", padding=12)
        paned.add(form_frame, weight=1)

        # Form Variables
        self.emp_id_var = tk.StringVar()
        self.emp_name_var = tk.StringVar()
        self.emp_email_var = tk.StringVar()
        self.emp_contact_var = tk.StringVar()
        self.emp_dept_var = tk.StringVar(value="IT")
        self.emp_desig_var = tk.StringVar()
        self.emp_join_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.emp_type_var = tk.StringVar(value="Salaried")
        self.emp_rate_var = tk.StringVar(value="50000")
        self.emp_status_var = tk.StringVar(value="Active")
        self.emp_search_var = tk.StringVar()

        r = 0
        ttk.Label(form_frame, text="Employee ID:").grid(row=r, column=0, sticky="w", pady=3)
        self.emp_id_entry = ttk.Entry(form_frame, textvariable=self.emp_id_var, width=22)
        self.emp_id_entry.grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Full Name:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_name_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Email:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_email_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Contact No:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_contact_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Department:").grid(row=r, column=0, sticky="w", pady=3)
        dept_combo = ttk.Combobox(form_frame, textvariable=self.emp_dept_var, width=20, state="readonly")
        dept_combo["values"] = ["IT", "Finance", "HR", "Operations", "Support", "Marketing", "Admin"]
        dept_combo.grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Designation:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_desig_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Joining Date:").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_join_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Employment Type:").grid(row=r, column=0, sticky="w", pady=3)
        type_combo = ttk.Combobox(form_frame, textvariable=self.emp_type_var, width=20, state="readonly")
        type_combo["values"] = ["Salaried", "Hourly"]
        type_combo.grid(row=r, column=1, sticky="w", pady=3)
        type_combo.bind("<<ComboboxSelected>>", self._on_emp_type_changed)

        r += 1
        self.emp_rate_label = ttk.Label(form_frame, text="Basic Salary (Rs.):")
        self.emp_rate_label.grid(row=r, column=0, sticky="w", pady=3)
        ttk.Entry(form_frame, textvariable=self.emp_rate_var, width=22).grid(row=r, column=1, sticky="w", pady=3)

        r += 1
        ttk.Label(form_frame, text="Status:").grid(row=r, column=0, sticky="w", pady=3)
        status_combo = ttk.Combobox(form_frame, textvariable=self.emp_status_var, width=20, state="readonly")
        status_combo["values"] = ["Active", "Inactive"]
        status_combo.grid(row=r, column=1, sticky="w", pady=3)

        # Form Action Buttons
        r += 1
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=r, column=0, columnspan=2, pady=12, sticky="ew")

        ttk.Button(btn_frame, text="Add", command=self._add_employee, width=7).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update", command=self._update_employee, width=7).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self._delete_employee, width=7).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self._clear_emp_form, width=7).pack(side=tk.LEFT, padx=2)

        # Right Table Frame
        table_frame = ttk.LabelFrame(paned, text="Employee Directory", padding=10)
        paned.add(table_frame, weight=3)

        # Search Bar
        search_bar = ttk.Frame(table_frame)
        search_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(search_bar, text="Search (ID/Name):").pack(side=tk.LEFT, padx=4)
        ttk.Entry(search_bar, textvariable=self.emp_search_var, width=22).pack(side=tk.LEFT, padx=4)
        ttk.Button(search_bar, text="Search", command=self._search_employees).pack(side=tk.LEFT, padx=4)
        ttk.Button(search_bar, text="Reset", command=self._load_employee_table).pack(side=tk.LEFT, padx=4)

        # Employee Treeview
        cols = ("ID", "Name", "Department", "Designation", "Type", "Base Pay", "Status")
        self.emp_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.emp_tree.heading(col, text=col)

        self.emp_tree.column("ID", width=70, anchor="center")
        self.emp_tree.column("Name", width=130)
        self.emp_tree.column("Department", width=90)
        self.emp_tree.column("Designation", width=120)
        self.emp_tree.column("Type", width=75, anchor="center")
        self.emp_tree.column("Base Pay", width=100, anchor="e")
        self.emp_tree.column("Status", width=65, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scroll_y.set)

        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.emp_tree.bind("<<TreeviewSelect>>", self._on_emp_tree_select)
        self._load_employee_table()
        self._auto_fill_next_emp_id()

    def _on_emp_type_changed(self, event=None):
        if self.emp_type_var.get() == "Hourly":
            self.emp_rate_label.config(text="Hourly Rate (Rs.):")
        else:
            self.emp_rate_label.config(text="Basic Salary (Rs.):")

    def _auto_fill_next_emp_id(self):
        employees = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        max_num = 0
        for emp in employees:
            try:
                num = int(emp["employee_id"].replace("EMP", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
        self.emp_id_var.set(f"EMP{max_num + 1:03d}")

    def _clear_emp_form(self):
        self._auto_fill_next_emp_id()
        self.emp_name_var.set("")
        self.emp_email_var.set("")
        self.emp_contact_var.set("")
        self.emp_dept_var.set("IT")
        self.emp_desig_var.set("")
        self.emp_join_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.emp_type_var.set("Salaried")
        self.emp_rate_var.set("50000")
        self.emp_status_var.set("Active")
        self._on_emp_type_changed()
        if self.emp_tree.selection():
            self.emp_tree.selection_remove(self.emp_tree.selection())

    def _load_employee_table(self, records=None):
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)

        if records is None:
            records = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)

        for emp in records:
            emp_type = emp.get("employment_type", "Salaried")
            if emp_type == "Salaried":
                base_pay = f"Rs. {emp.get('basic_salary', 0):,.2f}"
            else:
                base_pay = f"Rs. {emp.get('hourly_rate', 0):,.2f}/hr"

            self.emp_tree.insert("", tk.END, values=(
                emp.get("employee_id"),
                emp.get("name"),
                emp.get("department"),
                emp.get("designation"),
                emp_type,
                base_pay,
                emp.get("status")
            ))

    def _on_emp_tree_select(self, event):
        selected = self.emp_tree.selection()
        if not selected:
            return
        item = self.emp_tree.item(selected[0])
        emp_id = item["values"][0]

        emp = self.file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
        if not emp:
            return

        self.emp_id_var.set(emp.get("employee_id", ""))
        self.emp_name_var.set(emp.get("name", ""))
        self.emp_email_var.set(emp.get("email", ""))
        self.emp_contact_var.set(emp.get("contact", ""))
        self.emp_dept_var.set(emp.get("department", "IT"))
        self.emp_desig_var.set(emp.get("designation", ""))
        self.emp_join_var.set(emp.get("joining_date", ""))
        self.emp_type_var.set(emp.get("employment_type", "Salaried"))
        self.emp_status_var.set(emp.get("status", "Active"))

        if emp.get("employment_type") == "Hourly":
            self.emp_rate_var.set(str(emp.get("hourly_rate", 0)))
        else:
            self.emp_rate_var.set(str(emp.get("basic_salary", 0)))

        self._on_emp_type_changed()

    def _add_employee(self):
        try:
            emp_id = self.emp_id_var.get().strip()
            name = self.emp_name_var.get().strip()
            if not emp_id or not name:
                messagebox.showerror("Error", "Employee ID and Full Name are mandatory!")
                return

            # Check duplicate ID
            if self.file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id):
                messagebox.showerror("Error", f"Employee with ID '{emp_id}' already exists!")
                return

            rate_val = float(self.emp_rate_var.get().strip() or 0)
            emp_type = self.emp_type_var.get()

            # Polymorphic/Subclass Object Creation via domain classes to validate
            if emp_type == "Salaried":
                emp_obj = SalariedEmployee(
                    emp_id, name, self.emp_email_var.get().strip(),
                    self.emp_contact_var.get().strip(), self.emp_dept_var.get(),
                    self.emp_desig_var.get().strip(), self.emp_join_var.get().strip(),
                    rate_val, self.emp_status_var.get()
                )
            else:
                emp_obj = HourlyEmployee(
                    emp_id, name, self.emp_email_var.get().strip(),
                    self.emp_contact_var.get().strip(), self.emp_dept_var.get(),
                    self.emp_desig_var.get().strip(), self.emp_join_var.get().strip(),
                    rate_val, self.emp_status_var.get()
                )

            self.file_manager.add_record(FileManager.EMPLOYEES_FILE, emp_obj.to_dict())
            messagebox.showinfo("Success", f"Employee '{name}' added successfully!")
            self._load_employee_table()
            self._clear_emp_form()
            self.refresh_all_data()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for Salary/Rate.")
        except EmployeeError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))

    def _update_employee(self):
        try:
            emp_id = self.emp_id_var.get().strip()
            if not emp_id:
                messagebox.showerror("Error", "Select an employee to update.")
                return

            existing = self.file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
            if not existing:
                messagebox.showerror("Error", f"Employee '{emp_id}' not found.")
                return

            rate_val = float(self.emp_rate_var.get().strip() or 0)
            emp_type = self.emp_type_var.get()

            if emp_type == "Salaried":
                emp_obj = SalariedEmployee(
                    emp_id, self.emp_name_var.get().strip(), self.emp_email_var.get().strip(),
                    self.emp_contact_var.get().strip(), self.emp_dept_var.get(),
                    self.emp_desig_var.get().strip(), self.emp_join_var.get().strip(),
                    rate_val, self.emp_status_var.get()
                )
            else:
                emp_obj = HourlyEmployee(
                    emp_id, self.emp_name_var.get().strip(), self.emp_email_var.get().strip(),
                    self.emp_contact_var.get().strip(), self.emp_dept_var.get(),
                    self.emp_desig_var.get().strip(), self.emp_join_var.get().strip(),
                    rate_val, self.emp_status_var.get()
                )

            self.file_manager.update_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id, emp_obj.to_dict())
            messagebox.showinfo("Success", f"Employee '{emp_id}' updated successfully!")
            self._load_employee_table()
            self.refresh_all_data()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for Salary/Rate.")
        except EmployeeError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))

    def _delete_employee(self):
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        # Check if finalized payroll history exists
        payroll_records = self.file_manager.find_records(FileManager.PAYROLL_FILE, "employee_id", emp_id)
        finalized_count = sum(1 for p in payroll_records if p.get("status") == "Finalized")

        if finalized_count > 0:
            messagebox.showerror(
                "Deletion Blocked",
                f"Cannot delete employee '{emp_id}'. They have {finalized_count} finalized payroll record(s). "
                "Historical payroll records must be preserved for auditing. You may mark them as 'Inactive' instead."
            )
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee '{emp_id}'?")
        if confirm:
            self.file_manager.delete_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
            messagebox.showinfo("Deleted", f"Employee '{emp_id}' removed.")
            self._load_employee_table()
            self._clear_emp_form()
            self.refresh_all_data()

    def _search_employees(self):
        query = self.emp_search_var.get().strip().lower()
        if not query:
            self._load_employee_table()
            return

        employees = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        matched = [
            e for e in employees
            if query in e.get("employee_id", "").lower() or query in e.get("name", "").lower()
        ]
        self._load_employee_table(matched)

    # ============================================================
    # 3. ATTENDANCE MANAGEMENT TAB
    # ============================================================
    def _build_attendance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Attendance Management ")

        # Top Form Frame
        form_frame = ttk.LabelFrame(tab, text="Attendance Entry & Modification", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        self.att_emp_var = tk.StringVar()
        self.att_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.att_in_var = tk.StringVar(value="09:00")
        self.att_out_var = tk.StringVar(value="18:00")
        self.att_break_var = tk.StringVar(value="1.0")
        self.att_status_var = tk.StringVar(value="Present")

        # Row 0
        ttk.Label(form_frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.att_emp_combo = ttk.Combobox(form_frame, textvariable=self.att_emp_var, width=15, state="readonly")
        self.att_emp_combo.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.att_date_var, width=15).grid(row=0, column=3, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Status:").grid(row=0, column=4, padx=5, pady=4, sticky="w")
        att_status_combo = ttk.Combobox(form_frame, textvariable=self.att_status_var, width=15, state="readonly")
        att_status_combo["values"] = Attendance.VALID_STATUSES
        att_status_combo.grid(row=0, column=5, padx=5, pady=4, sticky="w")
        att_status_combo.bind("<<ComboboxSelected>>", self._on_att_status_change)

        # Row 1
        ttk.Label(form_frame, text="Check In (HH:MM):").grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self.att_in_entry = ttk.Entry(form_frame, textvariable=self.att_in_var, width=15)
        self.att_in_entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Check Out (HH:MM):").grid(row=1, column=2, padx=5, pady=4, sticky="w")
        self.att_out_entry = ttk.Entry(form_frame, textvariable=self.att_out_var, width=15)
        self.att_out_entry.grid(row=1, column=3, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Break (Hours):").grid(row=1, column=4, padx=5, pady=4, sticky="w")
        self.att_break_entry = ttk.Entry(form_frame, textvariable=self.att_break_var, width=15)
        self.att_break_entry.grid(row=1, column=5, padx=5, pady=4, sticky="w")

        # Action Buttons
        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=2, column=0, columnspan=6, pady=8)

        ttk.Button(btn_box, text="Record Attendance", command=self._add_attendance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Update Attendance", command=self._update_attendance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Delete Entry", command=self._delete_attendance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Clear", command=self._clear_att_form).pack(side=tk.LEFT, padx=5)

        # Filter Section
        filter_frame = ttk.Frame(tab, padding=5)
        filter_frame.pack(fill=tk.X, padx=10)

        self.att_filter_emp_var = tk.StringVar(value="All")
        self.att_filter_month_var = tk.IntVar(value=10)
        self.att_filter_year_var = tk.IntVar(value=2026)

        ttk.Label(filter_frame, text="Filter by Employee:").pack(side=tk.LEFT, padx=4)
        self.att_filter_emp_combo = ttk.Combobox(filter_frame, textvariable=self.att_filter_emp_var, width=12, state="readonly")
        self.att_filter_emp_combo.pack(side=tk.LEFT, padx=4)

        ttk.Label(filter_frame, text="Month:").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Spinbox(filter_frame, from_=1, to=12, textvariable=self.att_filter_month_var, width=5).pack(side=tk.LEFT, padx=2)

        ttk.Label(filter_frame, text="Year:").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Spinbox(filter_frame, from_=2020, to=2030, textvariable=self.att_filter_year_var, width=6).pack(side=tk.LEFT, padx=2)

        ttk.Button(filter_frame, text="Apply Filter", command=self._load_attendance_table).pack(side=tk.LEFT, padx=8)
        ttk.Button(filter_frame, text="Show All", command=lambda: self._load_attendance_table(show_all=True)).pack(side=tk.LEFT, padx=4)

        # Attendance Table
        table_frame = ttk.LabelFrame(tab, text="Attendance Log", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("Date", "Emp ID", "Name", "Check In", "Check Out", "Break (h)", "Hours", "Status")
        self.att_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.att_tree.heading(col, text=col)

        self.att_tree.column("Date", width=100, anchor="center")
        self.att_tree.column("Emp ID", width=90, anchor="center")
        self.att_tree.column("Name", width=140)
        self.att_tree.column("Check In", width=80, anchor="center")
        self.att_tree.column("Check Out", width=80, anchor="center")
        self.att_tree.column("Break (h)", width=70, anchor="center")
        self.att_tree.column("Hours", width=70, anchor="e")
        self.att_tree.column("Status", width=95, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.att_tree.yview)
        self.att_tree.configure(yscrollcommand=scroll_y.set)

        self.att_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.att_tree.bind("<<TreeviewSelect>>", self._on_att_tree_select)
        self._load_attendance_table()

    def _on_att_status_change(self, event=None):
        status = self.att_status_var.get()
        if status in ["Absent", "Paid Leave", "Unpaid Leave", "Holiday"]:
            self.att_in_var.set("")
            self.att_out_var.set("")
            self.att_break_var.set("0.0")
        elif status == "Half-day":
            self.att_in_var.set("09:00")
            self.att_out_var.set("13:30")
            self.att_break_var.set("0.5")
        else:
            self.att_in_var.set("09:00")
            self.att_out_var.set("18:00")
            self.att_break_var.set("1.0")

    def _clear_att_form(self):
        self.att_emp_var.set("")
        self.att_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.att_status_var.set("Present")
        self._on_att_status_change()
        if self.att_tree.selection():
            self.att_tree.selection_remove(self.att_tree.selection())

    def _load_attendance_table(self, show_all=False):
        for item in self.att_tree.get_children():
            self.att_tree.delete(item)

        records = self.file_manager.read_data(FileManager.ATTENDANCE_FILE)
        emp_filter = self.att_filter_emp_var.get()
        month = self.att_filter_month_var.get()
        year = self.att_filter_year_var.get()
        prefix = f"{year}-{month:02d}"

        # Sort by date descending
        records = sorted(records, key=lambda x: x.get("date", ""), reverse=True)

        for rec in records:
            if not show_all:
                if emp_filter != "All" and rec.get("employee_id") != emp_filter:
                    continue
                if not rec.get("date", "").startswith(prefix):
                    continue

            emp_name = self._get_employee_name(rec.get("employee_id"))
            self.att_tree.insert("", tk.END, values=(
                rec.get("date"),
                rec.get("employee_id"),
                emp_name,
                rec.get("check_in", "-"),
                rec.get("check_out", "-"),
                rec.get("break_duration", 0),
                f"{rec.get('total_working_hours', 0):.2f}",
                rec.get("status")
            ))

    def _on_att_tree_select(self, event):
        selected = self.att_tree.selection()
        if not selected:
            return
        vals = self.att_tree.item(selected[0])["values"]
        self.att_date_var.set(vals[0])
        self.att_emp_var.set(vals[1])
        self.att_in_var.set("" if vals[3] == "-" else vals[3])
        self.att_out_var.set("" if vals[4] == "-" else vals[4])
        self.att_break_var.set(str(vals[5]))
        self.att_status_var.set(vals[7])

    def _add_attendance(self):
        try:
            emp_id = self.att_emp_var.get().strip()
            date = self.att_date_var.get().strip()
            if not emp_id or not date:
                messagebox.showerror("Error", "Employee ID and Date are required.")
                return

            # Check duplicate attendance for same employee and date
            all_att = self.file_manager.read_data(FileManager.ATTENDANCE_FILE)
            for a in all_att:
                if a.get("employee_id") == emp_id and a.get("date") == date:
                    messagebox.showerror("Duplicate Record", f"Attendance for {emp_id} on {date} already exists!")
                    return

            break_h = float(self.att_break_var.get().strip() or 0)
            att_obj = Attendance(
                employee_id=emp_id,
                date=date,
                check_in=self.att_in_var.get().strip(),
                check_out=self.att_out_var.get().strip(),
                break_duration=break_h,
                status=self.att_status_var.get()
            )

            self.file_manager.add_record(FileManager.ATTENDANCE_FILE, att_obj.to_dict())
            messagebox.showinfo("Success", f"Attendance recorded for {emp_id} on {date} ({att_obj.total_working_hours} hrs).")
            self._load_attendance_table()
            self._clear_att_form()
        except InvalidAttendanceError as e:
            messagebox.showerror("Attendance Error", str(e))
        except ValueError:
            messagebox.showerror("Error", "Break duration must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_attendance(self):
        try:
            emp_id = self.att_emp_var.get().strip()
            date = self.att_date_var.get().strip()
            if not emp_id or not date:
                messagebox.showerror("Error", "Select an attendance entry to update.")
                return

            break_h = float(self.att_break_var.get().strip() or 0)
            att_obj = Attendance(
                employee_id=emp_id,
                date=date,
                check_in=self.att_in_var.get().strip(),
                check_out=self.att_out_var.get().strip(),
                break_duration=break_h,
                status=self.att_status_var.get()
            )

            # Match on employee_id AND date
            records = self.file_manager.read_data(FileManager.ATTENDANCE_FILE)
            updated = False
            for i in range(len(records)):
                if records[i].get("employee_id") == emp_id and records[i].get("date") == date:
                    records[i] = att_obj.to_dict()
                    updated = True
                    break

            if updated:
                self.file_manager.write_data(FileManager.ATTENDANCE_FILE, records)
                messagebox.showinfo("Success", f"Attendance updated for {emp_id} on {date}.")
                self._load_attendance_table()
            else:
                messagebox.showerror("Not Found", "Matching attendance record not found.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete_attendance(self):
        emp_id = self.att_emp_var.get().strip()
        date = self.att_date_var.get().strip()
        if not emp_id or not date:
            messagebox.showerror("Error", "Select an attendance record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete attendance of {emp_id} on {date}?")
        if confirm:
            records = self.file_manager.read_data(FileManager.ATTENDANCE_FILE)
            new_records = [r for r in records if not (r.get("employee_id") == emp_id and r.get("date") == date)]
            self.file_manager.write_data(FileManager.ATTENDANCE_FILE, new_records)
            messagebox.showinfo("Deleted", "Attendance entry removed.")
            self._load_attendance_table()
            self._clear_att_form()

    # ============================================================
    # 4. LEAVE MANAGEMENT TAB
    # ============================================================
    def _build_leave_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Leave Management ")

        # Form Frame
        form_frame = ttk.LabelFrame(tab, text="Leave Application & Decision", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        self.leave_id_var = tk.StringVar()
        self.leave_emp_var = tk.StringVar()
        self.leave_start_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.leave_end_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.leave_type_var = tk.StringVar(value="Paid Leave")
        self.leave_reason_var = tk.StringVar()
        self.leave_status_var = tk.StringVar(value="Pending")

        ttk.Label(form_frame, text="Leave ID:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.leave_id_var, width=15, state="readonly").grid(row=0, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Employee ID:").grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.leave_emp_combo = ttk.Combobox(form_frame, textvariable=self.leave_emp_var, width=15, state="readonly")
        self.leave_emp_combo.grid(row=0, column=3, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Leave Type:").grid(row=0, column=4, padx=5, pady=4, sticky="w")
        type_combo = ttk.Combobox(form_frame, textvariable=self.leave_type_var, width=15, state="readonly")
        type_combo["values"] = Leave.VALID_TYPES
        type_combo.grid(row=0, column=5, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.leave_start_var, width=15).grid(row=1, column=1, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="End Date:").grid(row=1, column=2, padx=5, pady=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.leave_end_var, width=15).grid(row=1, column=3, padx=5, pady=4, sticky="w")

        ttk.Label(form_frame, text="Reason:").grid(row=1, column=4, padx=5, pady=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.leave_reason_var, width=22).grid(row=1, column=5, padx=5, pady=4, sticky="w")

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=2, column=0, columnspan=6, pady=8)

        ttk.Button(btn_box, text="Apply Leave", command=self._add_leave).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Approve", command=lambda: self._set_leave_status("Approved")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Reject", command=lambda: self._set_leave_status("Rejected")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_box, text="Clear", command=self._clear_leave_form).pack(side=tk.LEFT, padx=5)

        # Leave Records Table
        table_frame = ttk.LabelFrame(tab, text="Leave Records", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("Leave ID", "Emp ID", "Name", "Start Date", "End Date", "Days", "Type", "Status", "Reason")
        self.leave_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.leave_tree.heading(col, text=col)

        self.leave_tree.column("Leave ID", width=80, anchor="center")
        self.leave_tree.column("Emp ID", width=80, anchor="center")
        self.leave_tree.column("Name", width=130)
        self.leave_tree.column("Start Date", width=95, anchor="center")
        self.leave_tree.column("End Date", width=95, anchor="center")
        self.leave_tree.column("Days", width=60, anchor="center")
        self.leave_tree.column("Type", width=100, anchor="center")
        self.leave_tree.column("Status", width=90, anchor="center")
        self.leave_tree.column("Reason", width=160)

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.leave_tree.yview)
        self.leave_tree.configure(yscrollcommand=scroll_y.set)

        self.leave_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.leave_tree.bind("<<TreeviewSelect>>", self._on_leave_tree_select)
        self._load_leave_table()
        self._auto_fill_next_leave_id()

    def _auto_fill_next_leave_id(self):
        leaves = self.file_manager.read_data(FileManager.LEAVES_FILE)
        max_num = 0
        for lv in leaves:
            try:
                num = int(lv["leave_id"].replace("LV", ""))
                if num > max_num:
                    max_num = num
            except (ValueError, KeyError):
                continue
        self.leave_id_var.set(f"LV{max_num + 1:03d}")

    def _clear_leave_form(self):
        self._auto_fill_next_leave_id()
        self.leave_emp_var.set("")
        self.leave_start_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.leave_end_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.leave_type_var.set("Paid Leave")
        self.leave_reason_var.set("")
        if self.leave_tree.selection():
            self.leave_tree.selection_remove(self.leave_tree.selection())

    def _load_leave_table(self):
        for item in self.leave_tree.get_children():
            self.leave_tree.delete(item)

        leaves = self.file_manager.read_data(FileManager.LEAVES_FILE)
        for lv in leaves:
            leave_obj = Leave.from_dict(lv)
            emp_name = self._get_employee_name(leave_obj.employee_id)
            self.leave_tree.insert("", tk.END, values=(
                leave_obj.leave_id,
                leave_obj.employee_id,
                emp_name,
                leave_obj.start_date,
                leave_obj.end_date,
                leave_obj.get_number_of_days(),
                leave_obj.leave_type,
                leave_obj.status,
                leave_obj.reason
            ))

    def _on_leave_tree_select(self, event):
        selected = self.leave_tree.selection()
        if not selected:
            return
        vals = self.leave_tree.item(selected[0])["values"]
        self.leave_id_var.set(vals[0])
        self.leave_emp_var.set(vals[1])
        self.leave_start_var.set(vals[3])
        self.leave_end_var.set(vals[4])
        self.leave_type_var.set(vals[6])
        self.leave_reason_var.set(vals[8])

    def _add_leave(self):
        try:
            emp_id = self.leave_emp_var.get().strip()
            if not emp_id:
                messagebox.showerror("Error", "Select an employee.")
                return

            leave_id = self.leave_id_var.get().strip()
            leave_obj = Leave(
                leave_id=leave_id,
                employee_id=emp_id,
                start_date=self.leave_start_var.get().strip(),
                end_date=self.leave_end_var.get().strip(),
                leave_type=self.leave_type_var.get(),
                reason=self.leave_reason_var.get().strip(),
                status="Pending"
            )

            self.file_manager.add_record(FileManager.LEAVES_FILE, leave_obj.to_dict())
            messagebox.showinfo("Success", f"Leave application {leave_id} submitted for {emp_id}.")
            self._load_leave_table()
            self._clear_leave_form()
        except InvalidLeaveError as e:
            messagebox.showerror("Leave Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _set_leave_status(self, new_status):
        leave_id = self.leave_id_var.get().strip()
        if not leave_id:
            messagebox.showerror("Error", "Select a leave request from the list.")
            return

        leaves = self.file_manager.read_data(FileManager.LEAVES_FILE)
        found = False
        for lv in leaves:
            if lv.get("leave_id") == leave_id:
                lv["status"] = new_status
                found = True
                break

        if found:
            self.file_manager.write_data(FileManager.LEAVES_FILE, leaves)
            messagebox.showinfo("Updated", f"Leave {leave_id} status updated to '{new_status}'.")
            self._load_leave_table()
        else:
            messagebox.showerror("Error", f"Leave record '{leave_id}' not found.")

    # ============================================================
    # 5. COMPENSATION MANAGEMENT TAB
    # ============================================================
    def _build_compensation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Compensation Management ")

        container = ttk.LabelFrame(tab, text="Manage Allowances, Bonuses & Deductions", padding=20)
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        # Top selector
        top_box = ttk.Frame(container)
        top_box.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(top_box, text="Select Employee:").pack(side=tk.LEFT, padx=5)
        self.comp_emp_var = tk.StringVar()
        self.comp_emp_combo = ttk.Combobox(top_box, textvariable=self.comp_emp_var, width=15, state="readonly")
        self.comp_emp_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(top_box, text="Load Compensation", command=self._load_employee_compensation).pack(side=tk.LEFT, padx=10)

        self.comp_emp_info_lbl = ttk.Label(top_box, text="", font=("Segoe UI", 9, "italic"), foreground="#1E40AF")
        self.comp_emp_info_lbl.pack(side=tk.LEFT, padx=15)

        # Form fields
        form_grid = ttk.Frame(container)
        form_grid.pack(anchor="w", pady=10)

        self.comp_hra_var = tk.StringVar(value="0")
        self.comp_trans_var = tk.StringVar(value="0")
        self.comp_med_var = tk.StringVar(value="0")
        self.comp_other_allow_var = tk.StringVar(value="0")
        self.comp_bonus_var = tk.StringVar(value="0")
        self.comp_other_ded_var = tk.StringVar(value="0")

        # Earnings group
        earn_frame = ttk.LabelFrame(form_grid, text="Earnings & Allowances (Monthly)", padding=15)
        earn_frame.grid(row=0, column=0, padx=15, sticky="n")

        ttk.Label(earn_frame, text="House Rent Allowance (HRA):").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(earn_frame, textvariable=self.comp_hra_var, width=18).grid(row=0, column=1, pady=4)

        ttk.Label(earn_frame, text="Transport Allowance:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(earn_frame, textvariable=self.comp_trans_var, width=18).grid(row=1, column=1, pady=4)

        ttk.Label(earn_frame, text="Medical Allowance:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(earn_frame, textvariable=self.comp_med_var, width=18).grid(row=2, column=1, pady=4)

        ttk.Label(earn_frame, text="Other Allowances:").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(earn_frame, textvariable=self.comp_other_allow_var, width=18).grid(row=3, column=1, pady=4)

        ttk.Label(earn_frame, text="Performance Bonus:").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(earn_frame, textvariable=self.comp_bonus_var, width=18).grid(row=4, column=1, pady=4)

        # Deductions group
        ded_frame = ttk.LabelFrame(form_grid, text="Additional Deductions", padding=15)
        ded_frame.grid(row=0, column=1, padx=15, sticky="n")

        ttk.Label(ded_frame, text="Other / Misc Deductions:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(ded_frame, textvariable=self.comp_other_ded_var, width=18).grid(row=0, column=1, pady=4)

        note_lbl = tk.Label(
            ded_frame,
            text="(Note: Unpaid leave and absence\ndeductions are calculated automatically\nbased on attendance logs).",
            justify=tk.LEFT,
            font=("Segoe UI", 8, "italic"),
            fg="#6B7280"
        )
        note_lbl.grid(row=1, column=0, columnspan=2, pady=12, sticky="w")

        # Save Button
        save_btn_frame = ttk.Frame(container)
        save_btn_frame.pack(anchor="w", padx=15, pady=15)

        ttk.Button(save_btn_frame, text="Save Compensation", command=self._save_compensation, width=20).pack(side=tk.LEFT)

    def _load_employee_compensation(self):
        emp_id = self.comp_emp_var.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Please select an employee.")
            return

        emp = self.file_manager.find_record(FileManager.EMPLOYEES_FILE, "employee_id", emp_id)
        if emp:
            self.comp_emp_info_lbl.config(
                text=f"{emp.get('name')} | {emp.get('department')} | {emp.get('employment_type')}"
            )

        comp = self.payroll_manager.get_compensation(emp_id)
        self.comp_hra_var.set(str(comp.get("hra", 0)))
        self.comp_trans_var.set(str(comp.get("transport_allowance", 0)))
        self.comp_med_var.set(str(comp.get("medical_allowance", 0)))
        self.comp_other_allow_var.set(str(comp.get("other_allowances", 0)))
        self.comp_bonus_var.set(str(comp.get("performance_bonus", 0)))
        self.comp_other_ded_var.set(str(comp.get("other_deductions", 0)))

    def _save_compensation(self):
        try:
            emp_id = self.comp_emp_var.get().strip()
            if not emp_id:
                messagebox.showerror("Error", "Select an employee first.")
                return

            comp_record = {
                "employee_id": emp_id,
                "hra": float(self.comp_hra_var.get().strip() or 0),
                "transport_allowance": float(self.comp_trans_var.get().strip() or 0),
                "medical_allowance": float(self.comp_med_var.get().strip() or 0),
                "other_allowances": float(self.comp_other_allow_var.get().strip() or 0),
                "performance_bonus": float(self.comp_bonus_var.get().strip() or 0),
                "other_deductions": float(self.comp_other_ded_var.get().strip() or 0)
            }

            all_comp = self.file_manager.read_data(FileManager.COMPENSATION_FILE)
            existing_idx = None
            for i, c in enumerate(all_comp):
                if c.get("employee_id") == emp_id:
                    existing_idx = i
                    break

            if existing_idx is not None:
                all_comp[existing_idx] = comp_record
            else:
                all_comp.append(comp_record)

            self.file_manager.write_data(FileManager.COMPENSATION_FILE, all_comp)
            messagebox.showinfo("Success", f"Compensation details for {emp_id} saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "All allowance and deduction values must be numeric.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ============================================================
    # 6. PAYROLL PROCESSING TAB
    # ============================================================
    def _build_payroll_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Payroll Processing ")

        # Control Bar
        ctrl_frame = ttk.LabelFrame(tab, text="Monthly Processing Controls", padding=10)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        self.pay_month_var = tk.IntVar(value=10)
        self.pay_year_var = tk.IntVar(value=2026)

        ttk.Label(ctrl_frame, text="Select Month:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(ctrl_frame, from_=1, to=12, textvariable=self.pay_month_var, width=5).pack(side=tk.LEFT, padx=5)

        ttk.Label(ctrl_frame, text="Year:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Spinbox(ctrl_frame, from_=2020, to=2030, textvariable=self.pay_year_var, width=6).pack(side=tk.LEFT, padx=5)

        ttk.Button(ctrl_frame, text="Generate Monthly Payroll", command=self._generate_monthly_payroll).pack(side=tk.LEFT, padx=15)
        ttk.Button(ctrl_frame, text="View Existing Records", command=self._load_payroll_table).pack(side=tk.LEFT, padx=5)

        # Payroll Records Table
        table_frame = ttk.LabelFrame(tab, text="Generated Monthly Payroll Summary", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("Payroll ID", "Emp ID", "Name", "Department", "Type", "Month/Year", "Gross (Rs.)", "Deductions (Rs.)", "Net (Rs.)", "Status", "Payment")
        self.pay_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.pay_tree.heading(col, text=col)

        self.pay_tree.column("Payroll ID", width=75, anchor="center")
        self.pay_tree.column("Emp ID", width=70, anchor="center")
        self.pay_tree.column("Name", width=120)
        self.pay_tree.column("Department", width=85)
        self.pay_tree.column("Type", width=70, anchor="center")
        self.pay_tree.column("Month/Year", width=75, anchor="center")
        self.pay_tree.column("Gross (Rs.)", width=85, anchor="e")
        self.pay_tree.column("Deductions (Rs.)", width=95, anchor="e")
        self.pay_tree.column("Net (Rs.)", width=85, anchor="e")
        self.pay_tree.column("Status", width=70, anchor="center")
        self.pay_tree.column("Payment", width=70, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.pay_tree.yview)
        self.pay_tree.configure(yscrollcommand=scroll_y.set)

        self.pay_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Action Bar
        bottom_bar = ttk.Frame(tab, padding=5)
        bottom_bar.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(bottom_bar, text="View Detailed Breakdown", command=self._view_payroll_breakdown).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_bar, text="Finalize Selected", command=self._finalize_selected_payroll).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_bar, text="Finalize All Drafts", command=self._finalize_all_drafts).pack(side=tk.LEFT, padx=5)

        self._load_payroll_table()

    def _generate_monthly_payroll(self):
        """
        Runs payroll generation for all active employees.
        Demonstrates POLYMORPHISM: calculates salary using employee.calculate_salary().
        """
        month = self.pay_month_var.get()
        year = self.pay_year_var.get()

        employees_data = self.file_manager.read_data(FileManager.EMPLOYEES_FILE)
        active_employees = [e for e in employees_data if e.get("status") == "Active"]

        if not active_employees:
            messagebox.showwarning("No Active Employees", "There are no active employees to process payroll for.")
            return

        success_count = 0
        skipped_count = 0

        for emp_data in active_employees:
            try:
                employee_obj = create_employee_from_dict(emp_data)
                # POLYMORPHISM IN ACTION
                self.payroll_manager.generate_payroll(employee_obj, month, year)
                success_count += 1
            except DuplicatePayrollError:
                skipped_count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed for {emp_data.get('employee_id')}: {str(e)}")

        msg = f"Payroll processing finished for {month:02d}/{year}.\n\n" \
              f"• Successfully Generated: {success_count}\n" \
              f"• Skipped (Already Generated): {skipped_count}"
        messagebox.showinfo("Payroll Batch Complete", msg)
        self._load_payroll_table()
        self.refresh_all_data()

    def _load_payroll_table(self):
        for item in self.pay_tree.get_children():
            self.pay_tree.delete(item)

        month = self.pay_month_var.get()
        year = self.pay_year_var.get()
        records = self.payroll_manager.get_payroll_summary(month, year)

        for rec in records:
            b = rec.get("salary_breakdown", {})
            self.pay_tree.insert("", tk.END, values=(
                rec.get("payroll_id"),
                rec.get("employee_id"),
                rec.get("employee_name"),
                rec.get("department"),
                rec.get("employment_type"),
                f"{rec.get('month'):02d}/{rec.get('year')}",
                f"{b.get('gross_salary', 0):,.2f}",
                f"{b.get('total_deductions', 0):,.2f}",
                f"{b.get('net_salary', 0):,.2f}",
                rec.get("status"),
                rec.get("payment_status")
            ))

    def _view_payroll_breakdown(self):
        selected = self.pay_tree.selection()
        if not selected:
            messagebox.showinfo("Select Record", "Please select a payroll record from the table to view its breakdown.")
            return

        payroll_id = self.pay_tree.item(selected[0])["values"][0]
        payroll_rec = self.file_manager.find_record(FileManager.PAYROLL_FILE, "payroll_id", payroll_id)
        if not payroll_rec:
            return

        # Pop-up window for breakdown
        win = tk.Toplevel(self.root)
        win.title(f"Detailed Salary Breakdown - {payroll_id}")
        win.geometry("550x550")
        win.minsize(500, 450)

        txt_frame = ttk.Frame(win, padding=15)
        txt_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(txt_frame, wrap=tk.NONE, font=("Courier", 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(txt_frame, orient=tk.VERTICAL, command=text_widget.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=sb.set)

        payslip_str = self.payroll_manager.generate_payslip_text(payroll_rec)
        text_widget.insert(tk.END, payslip_str)
        text_widget.configure(state="disabled")

    def _finalize_selected_payroll(self):
        selected = self.pay_tree.selection()
        if not selected:
            messagebox.showinfo("Select Record", "Please select a draft payroll to finalize.")
            return

        payroll_id = self.pay_tree.item(selected[0])["values"][0]
        try:
            self.payroll_manager.finalize_payroll(payroll_id)
            messagebox.showinfo("Success", f"Payroll '{payroll_id}' has been finalized and locked!")
            self._load_payroll_table()
            self.refresh_all_data()
        except PayrollError as e:
            messagebox.showerror("Finalization Error", str(e))

    def _finalize_all_drafts(self):
        month = self.pay_month_var.get()
        year = self.pay_year_var.get()
        records = self.payroll_manager.get_payroll_summary(month, year)

        count = 0
        for rec in records:
            if rec.get("status") == "Draft":
                self.payroll_manager.finalize_payroll(rec["payroll_id"])
                count += 1

        if count > 0:
            messagebox.showinfo("Finalized", f"{count} draft payroll record(s) finalized!")
            self._load_payroll_table()
            self.refresh_all_data()
        else:
            messagebox.showinfo("Info", "No draft records found for the selected period.")

    # ============================================================
    # 7. PAYSLIPS TAB
    # ============================================================
    def _build_payslips_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Payslips ")

        ctrl_frame = ttk.LabelFrame(tab, text="Generate & Preview Payslip", padding=10)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        self.ps_emp_var = tk.StringVar()
        self.ps_month_var = tk.IntVar(value=10)
        self.ps_year_var = tk.IntVar(value=2026)

        ttk.Label(ctrl_frame, text="Employee ID:").pack(side=tk.LEFT, padx=5)
        self.ps_emp_combo = ttk.Combobox(ctrl_frame, textvariable=self.ps_emp_var, width=15, state="readonly")
        self.ps_emp_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(ctrl_frame, text="Month:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Spinbox(ctrl_frame, from_=1, to=12, textvariable=self.ps_month_var, width=5).pack(side=tk.LEFT, padx=5)

        ttk.Label(ctrl_frame, text="Year:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Spinbox(ctrl_frame, from_=2020, to=2030, textvariable=self.ps_year_var, width=6).pack(side=tk.LEFT, padx=5)

        ttk.Button(ctrl_frame, text="Preview Payslip", command=self._preview_payslip).pack(side=tk.LEFT, padx=15)
        ttk.Button(ctrl_frame, text="Save to .txt File", command=self._save_payslip_file).pack(side=tk.LEFT, padx=5)

        # Payslip Display Area
        content_frame = ttk.LabelFrame(tab, text="Payslip Document Preview", padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.ps_text = tk.Text(content_frame, wrap=tk.NONE, font=("Courier", 10), bg="#F8FAFC")
        self.ps_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.ps_text.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.ps_text.configure(yscrollcommand=scroll_y.set)

    def _get_selected_payroll(self):
        emp_id = self.ps_emp_var.get().strip()
        month = self.ps_month_var.get()
        year = self.ps_year_var.get()

        if not emp_id:
            messagebox.showerror("Error", "Please select an employee.")
            return None

        payrolls = self.file_manager.read_data(FileManager.PAYROLL_FILE)
        for p in payrolls:
            if p.get("employee_id") == emp_id and p.get("month") == month and p.get("year") == year:
                return p

        messagebox.showwarning(
            "Payroll Not Found",
            f"No payroll record found for employee '{emp_id}' for {month:02d}/{year}.\n"
            "Please generate payroll in the 'Payroll Processing' tab first."
        )
        return None

    def _preview_payslip(self):
        payroll = self._get_selected_payroll()
        if not payroll:
            return

        text = self.payroll_manager.generate_payslip_text(payroll)
        self.ps_text.configure(state="normal")
        self.ps_text.delete("1.0", tk.END)
        self.ps_text.insert(tk.END, text)
        self.ps_text.configure(state="disabled")

    def _save_payslip_file(self):
        payroll = self._get_selected_payroll()
        if not payroll:
            return

        saved_path = self.payroll_manager.save_payslip(payroll)
        messagebox.showinfo("Payslip Saved", f"Payslip file saved successfully at:\n\n{saved_path}")

    # ============================================================
    # 8. PAYMENT HISTORY TAB
    # ============================================================
    def _build_payment_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=" Payment History ")

        paned = ttk.PanedWindow(tab, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Upper: Pending Payments
        pending_frame = ttk.LabelFrame(paned, text="Pending Payments (Finalized Payrolls Awaiting Disbursement)", padding=10)
        paned.add(pending_frame, weight=1)

        # Pending controls
        p_ctrl = ttk.Frame(pending_frame)
        p_ctrl.pack(fill=tk.X, pady=(0, 6))

        self.pmt_method_var = tk.StringVar(value="Bank Transfer")
        self.pmt_ref_var = tk.StringVar()

        ttk.Label(p_ctrl, text="Payment Method:").pack(side=tk.LEFT, padx=4)
        method_combo = ttk.Combobox(p_ctrl, textvariable=self.pmt_method_var, width=15, state="readonly")
        method_combo["values"] = ["UPI", "Bank Transfer", "Cash", "Cheque"]
        method_combo.pack(side=tk.LEFT, padx=4)

        ttk.Label(p_ctrl, text="Transaction / Ref No:").pack(side=tk.LEFT, padx=(10, 4))
        ttk.Entry(p_ctrl, textvariable=self.pmt_ref_var, width=18).pack(side=tk.LEFT, padx=4)

        ttk.Button(p_ctrl, text="Record Payment", command=self._record_payment).pack(side=tk.LEFT, padx=10)

        # Pending Treeview
        cols_pend = ("Payroll ID", "Emp ID", "Name", "Department", "Period", "Net Salary (Rs.)", "Status")
        self.pend_tree = ttk.Treeview(pending_frame, columns=cols_pend, show="headings", selectmode="browse")
        for col in cols_pend:
            self.pend_tree.heading(col, text=col)

        self.pend_tree.column("Payroll ID", width=85, anchor="center")
        self.pend_tree.column("Emp ID", width=80, anchor="center")
        self.pend_tree.column("Name", width=140)
        self.pend_tree.column("Department", width=100)
        self.pend_tree.column("Period", width=80, anchor="center")
        self.pend_tree.column("Net Salary (Rs.)", width=110, anchor="e")
        self.pend_tree.column("Status", width=80, anchor="center")

        scroll_pend = ttk.Scrollbar(pending_frame, orient=tk.VERTICAL, command=self.pend_tree.yview)
        self.pend_tree.configure(yscrollcommand=scroll_pend.set)
        self.pend_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_pend.pack(side=tk.RIGHT, fill=tk.Y)

        # Lower: Completed Payments
        comp_frame = ttk.LabelFrame(paned, text="Disbursement History (Completed Transactions)", padding=10)
        paned.add(comp_frame, weight=1)

        c_ctrl = ttk.Frame(comp_frame)
        c_ctrl.pack(fill=tk.X, pady=(0, 6))

        self.pmt_filter_emp_var = tk.StringVar(value="All")
        ttk.Label(c_ctrl, text="Filter by Employee:").pack(side=tk.LEFT, padx=4)
        self.pmt_filter_emp_combo = ttk.Combobox(c_ctrl, textvariable=self.pmt_filter_emp_var, width=12, state="readonly")
        self.pmt_filter_emp_combo.pack(side=tk.LEFT, padx=4)

        ttk.Button(c_ctrl, text="Filter", command=self._load_completed_payments).pack(side=tk.LEFT, padx=6)
        ttk.Button(c_ctrl, text="Show All", command=lambda: self._load_completed_payments(show_all=True)).pack(side=tk.LEFT, padx=4)

        # Completed Treeview
        cols_comp = ("Payment ID", "Payroll ID", "Emp ID", "Name", "Disbursed Amount (Rs.)", "Date", "Method", "Reference No")
        self.comp_pmt_tree = ttk.Treeview(comp_frame, columns=cols_comp, show="headings", selectmode="browse")
        for col in cols_comp:
            self.comp_pmt_tree.heading(col, text=col)

        self.comp_pmt_tree.column("Payment ID", width=85, anchor="center")
        self.comp_pmt_tree.column("Payroll ID", width=85, anchor="center")
        self.comp_pmt_tree.column("Emp ID", width=80, anchor="center")
        self.comp_pmt_tree.column("Name", width=140)
        self.comp_pmt_tree.column("Disbursed Amount (Rs.)", width=130, anchor="e")
        self.comp_pmt_tree.column("Date", width=90, anchor="center")
        self.comp_pmt_tree.column("Method", width=100, anchor="center")
        self.comp_pmt_tree.column("Reference No", width=130)

        scroll_comp = ttk.Scrollbar(comp_frame, orient=tk.VERTICAL, command=self.comp_pmt_tree.yview)
        self.comp_pmt_tree.configure(yscrollcommand=scroll_comp.set)
        self.comp_pmt_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_comp.pack(side=tk.RIGHT, fill=tk.Y)

        self._load_pending_payments()
        self._load_completed_payments()

    def _load_pending_payments(self):
        for item in self.pend_tree.get_children():
            self.pend_tree.delete(item)

        pending = self.payroll_manager.get_pending_payments()
        for p in pending:
            b = p.get("salary_breakdown", {})
            self.pend_tree.insert("", tk.END, values=(
                p.get("payroll_id"),
                p.get("employee_id"),
                p.get("employee_name"),
                p.get("department"),
                f"{p.get('month'):02d}/{p.get('year')}",
                f"{b.get('net_salary', 0):,.2f}",
                p.get("payment_status")
            ))

    def _load_completed_payments(self, show_all=False):
        for item in self.comp_pmt_tree.get_children():
            self.comp_pmt_tree.delete(item)

        payments = self.payroll_manager.get_completed_payments()
        emp_filter = self.pmt_filter_emp_var.get()

        for pmt in payments:
            if not show_all and emp_filter != "All" and pmt.get("employee_id") != emp_filter:
                continue

            emp_name = self._get_employee_name(pmt.get("employee_id"))
            self.comp_pmt_tree.insert("", tk.END, values=(
                pmt.get("payment_id"),
                pmt.get("payroll_id"),
                pmt.get("employee_id"),
                emp_name,
                f"{pmt.get('amount', 0):,.2f}",
                pmt.get("payment_date"),
                pmt.get("payment_method"),
                pmt.get("transaction_ref", "-")
            ))

    def _record_payment(self):
        selected = self.pend_tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select a pending payroll record to disburse payment.")
            return

        payroll_id = self.pend_tree.item(selected[0])["values"][0]
        method = self.pmt_method_var.get()
        ref = self.pmt_ref_var.get().strip()

        if not ref:
            # Auto-generate dummy reference if left blank
            ref = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            payment_obj = self.payroll_manager.record_payment(
                payroll_id=payroll_id,
                payment_method=method,
                transaction_ref=ref
            )
            messagebox.showinfo(
                "Payment Recorded",
                f"Disbursed Rs. {payment_obj.amount:,.2f} via {method}.\n"
                f"Payment ID: {payment_obj.payment_id}\nRef: {ref}"
            )
            self._load_pending_payments()
            self._load_completed_payments()
            self._load_payroll_table()
            self.refresh_all_data()
            self.pmt_ref_var.set("")
        except PayrollNotFinalizedError as e:
            messagebox.showerror("Validation Error", str(e))
        except PayrollError as e:
            messagebox.showerror("Payment Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
