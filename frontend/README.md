# PaySphere — Modern Web UI & Python OOP Integration

> **"Payroll Management, Made Effortless."**

A modern enterprise payroll web application connected directly to the Python Object-Oriented Programming (OOP) Payroll engine (`employee.py`, `payroll.py`, `records.py`, `file_manager.py`).

---

## 🚀 Key Functional Modules & Clickables

All 8 core modules from the system are fully interactive and connected:

1. **Dashboard Overview**:
   - Real-time metric cards (Active Employees, Latest Month Outlay, Pending Payments, Completed Payments).
   - Monthly disbursement expenditure curve (`Recharts` AreaChart).
   - Department headcount distribution (`Recharts` BarChart).
   - Academic OOP Viva Guide (explaining Polymorphism, Composition, Inheritance, Encapsulation).

2. **Employee Management**:
   - Filter by Department and live search by Name, ID, or Designation.
   - **Add Employee** modal with auto-generated ID (e.g. `EMP005`), Salaried vs. Hourly validation, and default compensation initialization.
   - **Edit Employee** and **Delete Employee** actions.

3. **Attendance Management**:
   - Filter by Employee, Month, Year, or toggle "Show All Logs".
   - **Record Attendance** modal with automatic calculation of working hours from check-in/out and break duration.
   - Color-coded status badges (`Present`, `Absent`, `Half-day`, `Holiday`, `Paid Leave`, `Unpaid Leave`).
   - Delete attendance entry action.

4. **Leave Management**:
   - **Apply For Leave** modal with date range, leave type, and reason.
   - Interactive **Approve** and **Reject** buttons with instant status updates.
   - Delete leave record.

5. **Compensation Management**:
   - View compensation breakdown (HRA, Transport, Medical, Other Allowances, Performance Bonus, Deductions).
   - **Edit Compensation** modal with live Total Allowances calculation and backend sync.

6. **Payroll Processing**:
   - Select Month and Year.
   - **Generate Monthly Payroll**: Polymorphically computes salary for all active employees using attendance and compensation records.
   - Confetti celebration upon successful batch run!
   - **View Breakdown** modal: Complete itemized salary calculation sheet.
   - **Finalize Selected Draft** and **Finalize All Drafts** batch locking.

7. **Payslips**:
   - Select Employee, Month, and Year.
   - **Preview Payslip**: Renders the exact formatted ASCII text payslip.
   - **Download .txt File**: Directly saves and downloads the payslip to the browser and `payslips/` directory.

8. **Payment History**:
   - **Pending Payments** section: Lists finalized payrolls awaiting disbursement.
   - Select payment method (`Bank Transfer`, `UPI`, `Cash`, `Cheque`), input Transaction / Ref No, and click **Disburse Payment**.
   - **Completed Transactions** audit table with payment date, method badge, and reference ID.

---

## 💻 How to Run the Application

### Option A: One-Command Full App (Recommended)
From the project root:
```bash
python run_system.py
```
This initializes sample data, starts the Python OOP backend, and serves the UI at **`http://localhost:5000`** while automatically opening your default web browser.

### Option B: Python CLI Flag
```bash
python main.py --web
```

### Option C: Vite Development Server
If developing UI components with hot-module reloading:
1. Start the Python backend:
   ```bash
   python api_server.py
   ```
2. In a separate terminal, start Vite:
   ```bash
   cd frontend
   npm run dev
   ```
   Open **`http://localhost:3000`** (Vite proxies all `/api` calls directly to Python on port 5000).

### Option D: Classic Tkinter Desktop GUI
The original desktop GUI remains 100% available:
```bash
python main.py
```
