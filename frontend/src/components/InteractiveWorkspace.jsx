import React, { useState, useEffect } from 'react';
import {
  Users,
  Clock,
  CalendarCheck2,
  Calendar,
  CreditCard,
  FileSpreadsheet,
  FileText,
  DollarSign,
  TrendingUp,
  ShieldCheck,
  CheckCircle,
  XCircle,
  AlertCircle,
  Plus,
  Edit2,
  Trash2,
  Search,
  Filter,
  RefreshCw,
  Download,
  Sparkles,
  ChevronRight,
  Eye,
  Check,
  X,
  ExternalLink,
  Award,
  Layers,
  ArrowRight,
  Copy
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import confetti from 'canvas-confetti';
import { payrollApi } from '../api/payrollApi';

const DEPARTMENTS = ['All', 'IT', 'Finance', 'HR', 'Operations', 'Support', 'Marketing', 'Admin'];
const LEAVE_TYPES = ['Paid Leave', 'Unpaid Leave', 'Sick Leave', 'Casual Leave'];
const ATTENDANCE_STATUSES = ['Present', 'Absent', 'Half-day', 'Holiday', 'Paid Leave', 'Unpaid Leave'];
const PAYMENT_METHODS = ['Bank Transfer', 'UPI', 'Cash', 'Cheque'];

export default function InteractiveWorkspace() {
  // Navigation
  const [activeTab, setActiveTab] = useState('overview');

  // Backend Health / Connection status
  const [backendConnected, setBackendConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  // Core Data Stores
  const [stats, setStats] = useState({
    total_employees: 4,
    active_employees: 4,
    latest_payroll_net: 0,
    latest_payroll_period: 'None',
    pending_payments_count: 0,
    completed_payments_count: 0,
    department_breakdown: { IT: 1, Finance: 1, Operations: 1, Support: 1 },
    employment_type_breakdown: { Salaried: 2, Hourly: 2 },
  });

  const [employees, setEmployees] = useState([]);
  const [empSearch, setEmpSearch] = useState('');
  const [empDeptFilter, setEmpDeptFilter] = useState('All');

  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [attEmpFilter, setAttEmpFilter] = useState('ALL');
  const [attMonth, setAttMonth] = useState(10);
  const [attYear, setAttYear] = useState(2026);
  const [attShowAll, setAttShowAll] = useState(false);

  const [leaves, setLeaves] = useState([]);
  const [compensations, setCompensations] = useState([]);

  const [payrollMonth, setPayrollMonth] = useState(10);
  const [payrollYear, setPayrollYear] = useState(2026);
  const [payrolls, setPayrolls] = useState([]);
  const [isProcessingPayroll, setIsProcessingPayroll] = useState(false);

  // Payslip Preview state
  const [payslipEmpId, setPayslipEmpId] = useState('EMP001');
  const [payslipMonth, setPayslipMonth] = useState(10);
  const [payslipYear, setPayslipYear] = useState(2026);
  const [payslipText, setPayslipText] = useState('');
  const [payslipLoading, setPayslipLoading] = useState(false);

  // Payment State
  const [pendingPayments, setPendingPayments] = useState([]);
  const [completedPayments, setCompletedPayments] = useState([]);
  const [selectedPendingPayrollId, setSelectedPendingPayrollId] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('Bank Transfer');
  const [transactionRef, setTransactionRef] = useState('');

  // Modals state
  const [employeeModalOpen, setEmployeeModalOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [employeeForm, setEmployeeForm] = useState({
    employee_id: '',
    name: '',
    email: '',
    contact: '',
    department: 'IT',
    designation: '',
    joining_date: '2026-01-15',
    employment_type: 'Salaried',
    basic_salary: 50000,
    hourly_rate: 300,
    status: 'Active',
  });

  const [attendanceModalOpen, setAttendanceModalOpen] = useState(false);
  const [attendanceForm, setAttendanceForm] = useState({
    employee_id: 'EMP001',
    date: '2026-10-15',
    check_in: '09:00',
    check_out: '18:00',
    break_duration: 1.0,
    status: 'Present',
  });

  const [leaveModalOpen, setLeaveModalOpen] = useState(false);
  const [leaveForm, setLeaveForm] = useState({
    employee_id: 'EMP001',
    start_date: '2026-10-20',
    end_date: '2026-10-21',
    leave_type: 'Paid Leave',
    reason: 'Family event',
  });

  const [compModalOpen, setCompModalOpen] = useState(false);
  const [compForm, setCompForm] = useState({
    employee_id: '',
    hra: 0,
    transport_allowance: 0,
    medical_allowance: 0,
    other_allowances: 0,
    performance_bonus: 0,
    other_deductions: 0,
  });

  const [breakdownModalOpen, setBreakdownModalOpen] = useState(false);
  const [selectedBreakdown, setSelectedBreakdown] = useState(null);

  // Show Toast
  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4500);
  };

  // Initial Data Load
  useEffect(() => {
    checkConnectionAndLoad();
  }, []);

  const checkConnectionAndLoad = async () => {
    setLoading(true);
    try {
      const health = await payrollApi.checkHealth();
      if (health && health.status === 'online') {
        setBackendConnected(true);
        await refreshAllData();
      }
    } catch (err) {
      console.warn('Backend not yet reachable on /api. Running in demo fallback mode.', err);
      setBackendConnected(false);
      // Seed with initial sample data so UI is immediately interactive
      loadInitialFallbackData();
    } finally {
      setLoading(false);
    }
  };

  const refreshAllData = async () => {
    try {
      const [statsData, empsData, leavesData, compsData, pendData, histData] = await Promise.all([
        payrollApi.getDashboardStats().catch(() => null),
        payrollApi.getEmployees().catch(() => []),
        payrollApi.getLeaves().catch(() => []),
        payrollApi.getCompensationList().catch(() => []),
        payrollApi.getPendingPayments().catch(() => []),
        payrollApi.getPaymentHistory().catch(() => []),
      ]);

      if (statsData) setStats(statsData);
      if (empsData) {
        setEmployees(empsData);
        if (empsData.length > 0 && !payslipEmpId) {
          setPayslipEmpId(empsData[0].employee_id);
        }
      }
      if (leavesData) setLeaves(leavesData);
      if (compsData) setCompensations(compsData);
      if (pendData) {
        setPendingPayments(pendData);
        if (pendData.length > 0 && !selectedPendingPayrollId) {
          setSelectedPendingPayrollId(pendData[0].payroll_id);
        }
      }
      if (histData) setCompletedPayments(histData);

      // Load attendance for current filter
      loadAttendance(attEmpFilter, attMonth, attYear, attShowAll);
      // Load payroll for current period
      loadPayroll(payrollMonth, payrollYear);
    } catch (err) {
      console.error('Error refreshing data:', err);
    }
  };

  const loadAttendance = async (empId, m, y, showAll) => {
    try {
      const params = showAll ? {} : { employee_id: empId, month: m, year: y };
      const data = await payrollApi.getAttendance(params);
      setAttendanceRecords(data || []);
    } catch (err) {
      console.warn('Failed to load attendance:', err);
    }
  };

  const loadPayroll = async (m, y) => {
    try {
      const data = await payrollApi.getPayroll(m, y);
      setPayrolls(data || []);
    } catch (err) {
      console.warn('Failed to load payroll records:', err);
    }
  };

  const loadInitialFallbackData = () => {
    const defaultEmps = [
      {
        employee_id: 'EMP001',
        name: 'Rahul Sharma',
        email: 'rahul.sharma@techcorp.com',
        contact: '9876543210',
        department: 'IT',
        designation: 'Software Developer',
        joining_date: '2024-01-15',
        employment_type: 'Salaried',
        basic_salary: 50000,
        status: 'Active',
      },
      {
        employee_id: 'EMP002',
        name: 'Priya Patel',
        email: 'priya.patel@techcorp.com',
        contact: '9876543211',
        department: 'Finance',
        designation: 'Senior Accountant',
        joining_date: '2023-06-01',
        employment_type: 'Salaried',
        basic_salary: 60000,
        status: 'Active',
      },
      {
        employee_id: 'EMP003',
        name: 'Amit Kumar',
        email: 'amit.kumar@techcorp.com',
        contact: '9876543212',
        department: 'Operations',
        designation: 'Technician',
        joining_date: '2024-03-10',
        employment_type: 'Hourly',
        hourly_rate: 300,
        status: 'Active',
      },
      {
        employee_id: 'EMP004',
        name: 'Neha Singh',
        email: 'neha.singh@techcorp.com',
        contact: '9876543213',
        department: 'Support',
        designation: 'Help Desk Executive',
        joining_date: '2025-01-20',
        employment_type: 'Hourly',
        hourly_rate: 250,
        status: 'Active',
      },
    ];
    setEmployees(defaultEmps);
    setPayslipEmpId('EMP001');

    setLeaves([
      {
        leave_id: 'LV001',
        employee_id: 'EMP002',
        employee_name: 'Priya Patel',
        department: 'Finance',
        start_date: '2026-10-15',
        end_date: '2026-10-16',
        leave_type: 'Paid Leave',
        reason: 'Family function',
        status: 'Approved',
      },
      {
        leave_id: 'LV002',
        employee_id: 'EMP002',
        employee_name: 'Priya Patel',
        department: 'Finance',
        start_date: '2026-10-22',
        end_date: '2026-10-22',
        leave_type: 'Unpaid Leave',
        reason: 'Personal work',
        status: 'Approved',
      },
      {
        leave_id: 'LV003',
        employee_id: 'EMP004',
        employee_name: 'Neha Singh',
        department: 'Support',
        start_date: '2026-10-22',
        end_date: '2026-10-22',
        leave_type: 'Unpaid Leave',
        reason: 'Doctor appointment',
        status: 'Rejected',
      },
    ]);
  };

  // ============================================================
  // Employee Handlers
  // ============================================================
  const handleOpenAddEmployee = () => {
    // Generate next emp ID
    let maxNum = 0;
    employees.forEach((e) => {
      const match = e.employee_id.match(/\d+/);
      if (match) {
        const val = parseInt(match[0], 10);
        if (val > maxNum) maxNum = val;
      }
    });
    const nextId = `EMP${String(maxNum + 1).padStart(3, '0')}`;

    setEditingEmployee(null);
    setEmployeeForm({
      employee_id: nextId,
      name: '',
      email: '',
      contact: '',
      department: 'IT',
      designation: '',
      joining_date: new Date().toISOString().split('T')[0],
      employment_type: 'Salaried',
      basic_salary: 50000,
      hourly_rate: 300,
      status: 'Active',
    });
    setEmployeeModalOpen(true);
  };

  const handleOpenEditEmployee = (emp) => {
    setEditingEmployee(emp);
    setEmployeeForm({
      employee_id: emp.employee_id,
      name: emp.name,
      email: emp.email,
      contact: emp.contact,
      department: emp.department,
      designation: emp.designation,
      joining_date: emp.joining_date,
      employment_type: emp.employment_type,
      basic_salary: emp.basic_salary || 50000,
      hourly_rate: emp.hourly_rate || 300,
      status: emp.status,
    });
    setEmployeeModalOpen(true);
  };

  const handleSaveEmployee = async (e) => {
    e.preventDefault();
    try {
      if (editingEmployee) {
        if (backendConnected) {
          await payrollApi.updateEmployee(employeeForm.employee_id, employeeForm);
        }
        setEmployees((prev) =>
          prev.map((emp) =>
            emp.employee_id === employeeForm.employee_id ? { ...emp, ...employeeForm } : emp
          )
        );
        showToast(`Employee ${employeeForm.name} updated successfully!`);
      } else {
        if (backendConnected) {
          await payrollApi.addEmployee(employeeForm);
        }
        setEmployees((prev) => [...prev, { ...employeeForm }]);
        showToast(`Employee ${employeeForm.name} (${employeeForm.employee_id}) added!`);
      }
      setEmployeeModalOpen(false);
      if (backendConnected) refreshAllData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDeleteEmployee = async (empId) => {
    if (!window.confirm(`Are you sure you want to delete employee ${empId}?`)) return;
    try {
      if (backendConnected) {
        await payrollApi.deleteEmployee(empId);
      }
      setEmployees((prev) => prev.filter((e) => e.employee_id !== empId));
      showToast(`Employee ${empId} deleted successfully.`);
      if (backendConnected) refreshAllData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Filtered employees list
  const filteredEmployees = employees.filter((emp) => {
    const matchesSearch =
      empSearch === '' ||
      emp.name.toLowerCase().includes(empSearch.toLowerCase()) ||
      emp.employee_id.toLowerCase().includes(empSearch.toLowerCase()) ||
      emp.designation.toLowerCase().includes(empSearch.toLowerCase());
    const matchesDept = empDeptFilter === 'All' || emp.department === empDeptFilter;
    return matchesSearch && matchesDept;
  });

  // ============================================================
  // Attendance Handlers
  // ============================================================
  const handleOpenAddAttendance = () => {
    setAttendanceForm({
      employee_id: employees[0]?.employee_id || 'EMP001',
      date: new Date().toISOString().split('T')[0],
      check_in: '09:00',
      check_out: '18:00',
      break_duration: 1.0,
      status: 'Present',
    });
    setAttendanceModalOpen(true);
  };

  const handleSaveAttendance = async (e) => {
    e.preventDefault();
    try {
      if (backendConnected) {
        await payrollApi.addAttendance(attendanceForm);
        loadAttendance(attEmpFilter, attMonth, attYear, attShowAll);
      } else {
        // Fallback local calculation
        const workedHours =
          attendanceForm.status === 'Present'
            ? Math.max(0, 9 - parseFloat(attendanceForm.break_duration || 0))
            : attendanceForm.status === 'Half-day'
            ? 4.0
            : 0;
        setAttendanceRecords((prev) => [
          { ...attendanceForm, total_working_hours: workedHours },
          ...prev,
        ]);
      }
      showToast(`Attendance recorded for ${attendanceForm.employee_id} on ${attendanceForm.date}.`);
      setAttendanceModalOpen(false);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDeleteAttendance = async (empId, date) => {
    if (!window.confirm(`Delete attendance log for ${empId} on ${date}?`)) return;
    try {
      if (backendConnected) {
        await payrollApi.deleteAttendance(empId, date);
        loadAttendance(attEmpFilter, attMonth, attYear, attShowAll);
      } else {
        setAttendanceRecords((prev) =>
          prev.filter((r) => !(r.employee_id === empId && r.date === date))
        );
      }
      showToast(`Attendance entry deleted.`);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // ============================================================
  // Leave Handlers
  // ============================================================
  const handleApplyLeave = async (e) => {
    e.preventDefault();
    try {
      if (backendConnected) {
        await payrollApi.applyLeave(leaveForm);
        const updated = await payrollApi.getLeaves();
        setLeaves(updated);
      } else {
        const nextId = `LV${String(leaves.length + 1).padStart(3, '0')}`;
        const emp = employees.find((e) => e.employee_id === leaveForm.employee_id);
        setLeaves((prev) => [
          ...prev,
          {
            leave_id: nextId,
            ...leaveForm,
            employee_name: emp?.name || 'Unknown',
            department: emp?.department || 'IT',
            status: 'Pending',
          },
        ]);
      }
      showToast(`Leave application submitted for ${leaveForm.employee_id}.`);
      setLeaveModalOpen(false);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleLeaveDecision = async (leaveId, status) => {
    try {
      if (backendConnected) {
        await payrollApi.decideLeave(leaveId, status);
        const updated = await payrollApi.getLeaves();
        setLeaves(updated);
      } else {
        setLeaves((prev) =>
          prev.map((l) => (l.leave_id === leaveId ? { ...l, status } : l))
        );
      }
      showToast(`Leave ${leaveId} marked as ${status}!`);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDeleteLeave = async (leaveId) => {
    if (!window.confirm(`Delete leave application ${leaveId}?`)) return;
    try {
      if (backendConnected) {
        await payrollApi.deleteLeave(leaveId);
        const updated = await payrollApi.getLeaves();
        setLeaves(updated);
      } else {
        setLeaves((prev) => prev.filter((l) => l.leave_id !== leaveId));
      }
      showToast(`Leave record ${leaveId} removed.`);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // ============================================================
  // Compensation Handlers
  // ============================================================
  const handleOpenEditCompensation = (comp) => {
    setCompForm({
      employee_id: comp.employee_id,
      hra: comp.hra || 0,
      transport_allowance: comp.transport_allowance || 0,
      medical_allowance: comp.medical_allowance || 0,
      other_allowances: comp.other_allowances || 0,
      performance_bonus: comp.performance_bonus || 0,
      other_deductions: comp.other_deductions || 0,
    });
    setCompModalOpen(true);
  };

  const handleSaveCompensation = async (e) => {
    e.preventDefault();
    try {
      if (backendConnected) {
        await payrollApi.updateCompensation(compForm);
        const updated = await payrollApi.getCompensationList();
        setCompensations(updated);
      } else {
        setCompensations((prev) =>
          prev.map((c) =>
            c.employee_id === compForm.employee_id ? { ...c, ...compForm } : c
          )
        );
      }
      showToast(`Compensation updated for ${compForm.employee_id}!`);
      setCompModalOpen(false);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // ============================================================
  // Payroll Processing Handlers
  // ============================================================
  const handleGeneratePayroll = async () => {
    setIsProcessingPayroll(true);
    try {
      if (backendConnected) {
        const res = await payrollApi.generatePayrollBatch(payrollMonth, payrollYear);
        showToast(
          `Payroll Batch Complete for ${String(payrollMonth).padStart(2, '0')}/${payrollYear}: Generated ${res.generated_count}, Skipped ${res.skipped_count}.`
        );
        try {
          confetti({
            particleCount: 90,
            spread: 75,
            origin: { y: 0.6 },
            colors: ['#168C87', '#54C7C1', '#8D72DF', '#FFB067'],
          });
        } catch (e) {}
        await refreshAllData();
      } else {
        // Fallback demo simulation
        setTimeout(() => {
          setIsProcessingPayroll(false);
          showToast(`October 2026 Payroll Generated for 4 active employees!`);
          try {
            confetti({
              particleCount: 70,
              spread: 60,
              origin: { y: 0.6 },
            });
          } catch (e) {}
        }, 800);
        return;
      }
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setIsProcessingPayroll(false);
    }
  };

  const handleFinalizePayroll = async (payrollId) => {
    try {
      if (backendConnected) {
        await payrollApi.finalizePayroll(payrollId);
        showToast(`Payroll ${payrollId} finalized and locked for payment!`);
        await refreshAllData();
      } else {
        setPayrolls((prev) =>
          prev.map((p) =>
            p.payroll_id === payrollId ? { ...p, status: 'Finalized' } : p
          )
        );
        showToast(`Payroll ${payrollId} finalized!`);
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleFinalizeAllDrafts = async () => {
    try {
      if (backendConnected) {
        const res = await payrollApi.finalizeAllDrafts(payrollMonth, payrollYear);
        showToast(`Finalized ${res.count} draft payroll records!`);
        await refreshAllData();
      } else {
        setPayrolls((prev) =>
          prev.map((p) => ({ ...p, status: 'Finalized' }))
        );
        showToast(`All drafts finalized.`);
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleViewBreakdown = async (payroll) => {
    try {
      if (backendConnected) {
        const res = await payrollApi.getPayrollBreakdown(payroll.payroll_id);
        setSelectedBreakdown(res);
      } else {
        setSelectedBreakdown({
          payroll,
          payslip_text: `Payroll ID: ${payroll.payroll_id}\nEmployee: ${payroll.employee_name}\nNet Salary: Rs. ${payroll.salary_breakdown?.net_salary || 0}`,
        });
      }
      setBreakdownModalOpen(true);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // ============================================================
  // Payslips Handlers
  // ============================================================
  const handlePreviewPayslip = async () => {
    if (!payslipEmpId) {
      showToast('Please select an employee.', 'error');
      return;
    }
    setPayslipLoading(true);
    try {
      if (backendConnected) {
        const res = await payrollApi.previewPayslip(payslipEmpId, payslipMonth, payslipYear);
        setPayslipText(res.payslip_text);
        showToast(`Payslip loaded for ${payslipEmpId} (${payslipMonth}/${payslipYear}).`);
      } else {
        setPayslipText(
          `============================================================\nPAYSPHERE ENTERPRISE PAYSLIP (DEMO)\n============================================================\nEmployee ID: ${payslipEmpId}\nPeriod: ${payslipMonth}/${payslipYear}\nStatus: Calculated via Domain OOP Models\nRun 'python api_server.py' to generate exact formatted ASCII payslip text.\n============================================================`
        );
      }
    } catch (err) {
      setPayslipText('');
      showToast(err.message, 'error');
    } finally {
      setPayslipLoading(false);
    }
  };

  const handleDownloadPayslip = async () => {
    if (!payslipEmpId) return;
    try {
      if (backendConnected) {
        const res = await payrollApi.downloadPayslip(payslipEmpId, payslipMonth, payslipYear);
        // Create client download
        const blob = new Blob([res.content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = res.filename;
        link.click();
        URL.revokeObjectURL(url);
        showToast(`Payslip saved to ${res.saved_path || 'payslips/'} & downloaded!`);
      } else {
        const content = payslipText || 'Payslip preview demo';
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `payslip_${payslipEmpId}_${payslipMonth}_${payslipYear}.txt`;
        link.click();
        URL.revokeObjectURL(url);
        showToast(`Payslip downloaded as text file.`);
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // ============================================================
  // Payment Handlers
  // ============================================================
  const handleDisbursePayment = async (e) => {
    e.preventDefault();
    if (!selectedPendingPayrollId) {
      showToast('Please select a pending payroll to disburse.', 'error');
      return;
    }
    if (!transactionRef.trim()) {
      showToast('Please enter a Transaction / Ref No.', 'error');
      return;
    }

    try {
      if (backendConnected) {
        const res = await payrollApi.disbursePayment(
          selectedPendingPayrollId,
          paymentMethod,
          transactionRef
        );
        showToast(res.message);
        setTransactionRef('');
        await refreshAllData();
      } else {
        const target = pendingPayments.find((p) => p.payroll_id === selectedPendingPayrollId);
        showToast(`Disbursement of Rs. ${target?.salary_breakdown?.net_salary || 0} recorded via ${paymentMethod}!`);
        setPendingPayments((prev) =>
          prev.filter((p) => p.payroll_id !== selectedPendingPayrollId)
        );
        setTransactionRef('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Chart data for Overview
  const monthlyTrendData = [
    { month: 'Jul', expenditure: 142000, employees: 4 },
    { month: 'Aug', expenditure: 156000, employees: 4 },
    { month: 'Sep', expenditure: 168000, employees: 4 },
    { month: 'Oct', expenditure: stats.latest_payroll_net || 184500, employees: 4 },
  ];

  const deptChartData = Object.entries(stats.department_breakdown || {}).map(([name, count]) => ({
    name,
    count,
  }));

  const pieData = [
    { name: 'Salaried', value: stats.employment_type_breakdown?.Salaried || 2, color: '#168C87' },
    { name: 'Hourly', value: stats.employment_type_breakdown?.Hourly || 2, color: '#8D72DF' },
  ];

  return (
    <section id="workspace" className="py-12 px-4 sm:px-6 md:px-12 lg:px-16 bg-[#F6FAF8] min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Top Header & Backend Status */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between pb-6 mb-8 border-b border-navy-900/10 gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-tealbrand/10 text-tealbrand text-xs font-bold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              Full System Functional Workspace
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-navy-900 tracking-tight">
              Payroll Management System
            </h1>
            <p className="text-sm text-navy-700/70 mt-1">
              Integrated with Python OOP Backend (<code className="bg-white/80 px-1.5 py-0.5 rounded text-tealbrand-dark font-mono text-xs">employee.py</code>, <code className="bg-white/80 px-1.5 py-0.5 rounded text-tealbrand-dark font-mono text-xs">payroll.py</code>, <code className="bg-white/80 px-1.5 py-0.5 rounded text-tealbrand-dark font-mono text-xs">records.py</code>).
            </p>
          </div>

          {/* Connection status badge & Refresh button */}
          <div className="flex items-center gap-3">
            <div
              className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-bold shadow-sm border ${
                backendConnected
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-amber-50 text-amber-700 border-amber-200'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  backendConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
                }`}
              />
              {backendConnected ? 'Python Backend Connected' : 'Demo Mode (Run api_server.py)'}
            </div>

            <button
              onClick={checkConnectionAndLoad}
              disabled={loading}
              className="p-2.5 rounded-xl bg-white hover:bg-slate-100 text-navy-800 border border-slate-200 shadow-sm transition-all hover:scale-105 active:scale-95"
              title="Refresh All System Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-tealbrand' : ''}`} />
            </button>
          </div>
        </div>

        {/* Floating Toast Notification */}
        {toast && (
          <div
            className={`fixed bottom-6 right-6 z-50 px-5 py-3.5 rounded-2xl shadow-xl border flex items-center gap-3 text-sm font-semibold transition-all animate-bounce ${
              toast.type === 'error'
                ? 'bg-rose-50 text-rose-800 border-rose-200'
                : 'bg-emerald-50 text-emerald-900 border-emerald-200'
            }`}
          >
            {toast.type === 'error' ? (
              <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
            ) : (
              <CheckCircle className="w-5 h-5 text-emerald-600 flex-shrink-0" />
            )}
            <span>{toast.message}</span>
            <button onClick={() => setToast(null)} className="ml-2 hover:opacity-75">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Tab Navigation Pill Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-8 scrollbar-thin">
          {[
            { id: 'overview', label: 'Dashboard', icon: TrendingUp },
            { id: 'employees', label: 'Employees', icon: Users, count: employees.length },
            { id: 'attendance', label: 'Attendance', icon: Clock },
            { id: 'leaves', label: 'Leaves', icon: Calendar, count: leaves.filter((l) => l.status === 'Pending').length },
            { id: 'compensation', label: 'Compensation', icon: DollarSign },
            { id: 'payroll', label: 'Payroll Processing', icon: Sparkles },
            { id: 'payslips', label: 'Payslips', icon: FileText },
            { id: 'payments', label: 'Payment History', icon: CreditCard, count: pendingPayments.length },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs sm:text-sm whitespace-nowrap transition-all duration-200 ${
                  isActive
                    ? 'bg-navy-900 text-white shadow-md shadow-navy-900/15 scale-[1.02]'
                    : 'bg-white hover:bg-slate-100 text-navy-800/80 border border-slate-200/80 hover:text-navy-900'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-mint-300' : 'text-navy-500'}`} />
                <span>{tab.label}</span>
                {tab.count !== undefined && tab.count > 0 && (
                  <span
                    className={`ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-extrabold ${
                      isActive ? 'bg-tealbrand text-white' : 'bg-slate-100 text-navy-700'
                    }`}
                  >
                    {tab.count}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* ============================================================
            TAB 1: DASHBOARD OVERVIEW
        ============================================================ */}
        {activeTab === 'overview' && (
          <div className="space-y-8 animate-fadeIn">
            {/* Stat Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-navy-500 uppercase tracking-wider">Active Employees</span>
                  <div className="text-2xl sm:text-3xl font-extrabold text-navy-900 mt-1">{stats.active_employees}</div>
                  <span className="text-xs text-emerald-600 font-semibold mt-1 inline-flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> All verified & onboarded
                  </span>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-tealbrand/10 text-tealbrand flex items-center justify-center">
                  <Users className="w-6 h-6" />
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-navy-500 uppercase tracking-wider">Latest Batch Payroll</span>
                  <div className="text-2xl sm:text-3xl font-extrabold text-navy-900 mt-1">
                    ₹{stats.latest_payroll_net ? stats.latest_payroll_net.toLocaleString('en-IN') : '0.00'}
                  </div>
                  <span className="text-xs text-navy-500 font-medium mt-1 inline-block">
                    Period: {stats.latest_payroll_period || 'None'}
                  </span>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-accentpurple/10 text-accentpurple flex items-center justify-center">
                  <CreditCard className="w-6 h-6" />
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-navy-500 uppercase tracking-wider">Pending Payments</span>
                  <div className="text-2xl sm:text-3xl font-extrabold text-amber-600 mt-1">
                    {stats.pending_payments_count}
                  </div>
                  <span className="text-xs text-amber-600 font-medium mt-1 inline-block">
                    Awaiting Bank Disbursement
                  </span>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
                  <Clock className="w-6 h-6" />
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-navy-500 uppercase tracking-wider">Completed Payments</span>
                  <div className="text-2xl sm:text-3xl font-extrabold text-tealbrand-dark mt-1">
                    {stats.completed_payments_count}
                  </div>
                  <span className="text-xs text-emerald-600 font-medium mt-1 inline-block">
                    Disbursed with Ref No.
                  </span>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center">
                  <CheckCircle className="w-6 h-6" />
                </div>
              </div>
            </div>

            {/* Visual Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Disbursement Trend */}
              <div className="lg:col-span-2 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-navy-900 text-base">Monthly Disbursement Trend</h3>
                    <p className="text-xs text-navy-500">Net salary outlay aggregated across fiscal batches</p>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-slate-100 text-navy-700 text-xs font-bold">2026 Fiscal</span>
                </div>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={monthlyTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="expGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#168C87" stopOpacity={0.4} />
                          <stop offset="95%" stopColor="#168C87" stopOpacity={0.0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                      <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: '#64748B', fontSize: 12 }} />
                      <YAxis tickLine={false} axisLine={false} tick={{ fill: '#64748B', fontSize: 12 }} />
                      <Tooltip
                        formatter={(val) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Net Outlay']}
                        contentStyle={{ backgroundColor: '#17153D', borderRadius: '12px', color: '#fff', border: 'none' }}
                      />
                      <Area type="monotone" dataKey="expenditure" stroke="#168C87" strokeWidth={3} fillOpacity={1} fill="url(#expGradient)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Department Headcount */}
              <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col">
                <h3 className="font-bold text-navy-900 text-base mb-1">Department Allocations</h3>
                <p className="text-xs text-navy-500 mb-4">Active headcount per enterprise division</p>
                <div className="h-48 w-full flex-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={deptChartData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                      <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: '#64748B', fontSize: 11 }} />
                      <YAxis allowDecimals={false} tickLine={false} axisLine={false} tick={{ fill: '#64748B', fontSize: 11 }} />
                      <Tooltip contentStyle={{ backgroundColor: '#17153D', borderRadius: '12px', color: '#fff', border: 'none' }} />
                      <Bar dataKey="count" fill="#8D72DF" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Academic OOP Viva Guide Banner */}
            <div className="bg-gradient-to-r from-navy-900 to-[#1F2A4A] text-white p-6 sm:p-8 rounded-3xl shadow-lg relative overflow-hidden">
              <div className="relative z-10">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-mint-300 text-xs font-bold uppercase tracking-wider mb-3">
                  <Award className="w-3.5 h-3.5" />
                  Academic Semester Viva Guide
                </div>
                <h3 className="text-xl sm:text-2xl font-bold tracking-tight mb-2">
                  Object-Oriented Architecture & Domain Models
                </h3>
                <p className="text-slate-300 text-xs sm:text-sm max-w-2xl mb-6">
                  This system combines clean Python OOP engineering with modern web architecture:
                </p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                    <div className="font-bold text-mint-300 text-sm mb-1">Polymorphism & Inheritance</div>
                    <p className="text-xs text-slate-300">
                      <code className="text-mint-200">SalariedEmployee</code> and <code className="text-mint-200">HourlyEmployee</code> both inherit from <code className="text-mint-200">Employee</code> and implement <code className="text-mint-200">calculate_salary()</code> differently.
                    </p>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                    <div className="font-bold text-mint-300 text-sm mb-1">Composition & Aggregation</div>
                    <p className="text-xs text-slate-300">
                      Each <code className="text-mint-200">Payroll</code> owns a <code className="text-mint-200">SalaryBreakdown</code> instance. <code className="text-mint-200">PayrollManager</code> coordinates domain logic with <code className="text-mint-200">FileManager</code>.
                    </p>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                    <div className="font-bold text-mint-300 text-sm mb-1">File Persistence & Encapsulation</div>
                    <p className="text-xs text-slate-300">
                      Protected attributes with getters/setters and clean JSON file I/O operations in <code className="text-mint-200">data/</code> directory.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 2: EMPLOYEE MANAGEMENT
        ============================================================ */}
        {activeTab === 'employees' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Action Bar */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3 flex-1">
                {/* Search */}
                <div className="relative flex-1 min-w-[200px]">
                  <Search className="w-4 h-4 text-navy-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search by name, ID, or designation..."
                    value={empSearch}
                    onChange={(e) => setEmpSearch(e.target.value)}
                    className="w-full pl-9 pr-4 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-tealbrand focus:ring-1 focus:ring-tealbrand"
                  />
                </div>

                {/* Dept Filter */}
                <select
                  value={empDeptFilter}
                  onChange={(e) => setEmpDeptFilter(e.target.value)}
                  className="px-3 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-tealbrand bg-white"
                >
                  {DEPARTMENTS.map((dept) => (
                    <option key={dept} value={dept}>
                      Dept: {dept}
                    </option>
                  ))}
                </select>
              </div>

              {/* Add Button */}
              <button
                onClick={handleOpenAddEmployee}
                className="px-4 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-sm flex items-center justify-center gap-2 transition-all hover:scale-105 active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>Add Employee</span>
              </button>
            </div>

            {/* Employees Table */}
            <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-4">Employee ID</th>
                      <th className="py-3.5 px-4">Full Name</th>
                      <th className="py-3.5 px-4">Department</th>
                      <th className="py-3.5 px-4">Designation</th>
                      <th className="py-3.5 px-4">Type</th>
                      <th className="py-3.5 px-4 text-right">Base Pay / Rate</th>
                      <th className="py-3.5 px-4 text-center">Status</th>
                      <th className="py-3.5 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {filteredEmployees.map((emp) => (
                      <tr key={emp.employee_id} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3.5 px-4 font-mono font-bold text-tealbrand">{emp.employee_id}</td>
                        <td className="py-3.5 px-4 font-semibold text-navy-900">{emp.name}</td>
                        <td className="py-3.5 px-4 text-navy-700">{emp.department}</td>
                        <td className="py-3.5 px-4 text-navy-600">{emp.designation}</td>
                        <td className="py-3.5 px-4">
                          <span
                            className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                              emp.employment_type === 'Salaried'
                                ? 'bg-tealbrand/10 text-tealbrand'
                                : 'bg-accentpurple/10 text-accentpurple'
                            }`}
                          >
                            {emp.employment_type}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-right font-mono font-semibold text-navy-800">
                          {emp.employment_type === 'Salaried'
                            ? `₹${Number(emp.basic_salary || 0).toLocaleString('en-IN')}/mo`
                            : `₹${Number(emp.hourly_rate || 0).toLocaleString('en-IN')}/hr`}
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          <span
                            className={`inline-block px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                              emp.status === 'Active'
                                ? 'bg-emerald-100 text-emerald-800'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {emp.status}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <div className="flex items-center justify-end gap-1.5">
                            <button
                              onClick={() => handleOpenEditEmployee(emp)}
                              className="p-1.5 rounded-lg hover:bg-slate-100 text-navy-600 transition-colors"
                              title="Edit Employee"
                            >
                              <Edit2 className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteEmployee(emp.employee_id)}
                              className="p-1.5 rounded-lg hover:bg-rose-50 text-rose-600 transition-colors"
                              title="Delete Employee"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {filteredEmployees.length === 0 && (
                      <tr>
                        <td colSpan="8" className="py-8 text-center text-navy-400">
                          No employees found matching filter criteria.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 3: ATTENDANCE MANAGEMENT
        ============================================================ */}
        {activeTab === 'attendance' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Attendance Filter & Action Bar */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3">
                {/* Employee Filter */}
                <select
                  value={attEmpFilter}
                  onChange={(e) => {
                    setAttEmpFilter(e.target.value);
                    loadAttendance(e.target.value, attMonth, attYear, attShowAll);
                  }}
                  className="px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                >
                  <option value="ALL">All Employees</option>
                  {employees.map((emp) => (
                    <option key={emp.employee_id} value={emp.employee_id}>
                      {emp.employee_id} - {emp.name}
                    </option>
                  ))}
                </select>

                {/* Month Picker */}
                <div className="flex items-center gap-1 text-sm text-navy-700">
                  <span>Month:</span>
                  <select
                    value={attMonth}
                    onChange={(e) => {
                      const m = parseInt(e.target.value, 10);
                      setAttMonth(m);
                      loadAttendance(attEmpFilter, m, attYear, attShowAll);
                    }}
                    className="px-2.5 py-1.5 rounded-xl border border-slate-200 bg-white"
                  >
                    {[...Array(12)].map((_, i) => (
                      <option key={i + 1} value={i + 1}>
                        {i + 1}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Year Picker */}
                <div className="flex items-center gap-1 text-sm text-navy-700">
                  <span>Year:</span>
                  <input
                    type="number"
                    value={attYear}
                    onChange={(e) => {
                      const y = parseInt(e.target.value, 10);
                      setAttYear(y);
                      loadAttendance(attEmpFilter, attMonth, y, attShowAll);
                    }}
                    className="w-20 px-2 py-1.5 rounded-xl border border-slate-200 text-sm"
                  />
                </div>

                {/* Show All Toggle */}
                <button
                  onClick={() => {
                    const newVal = !attShowAll;
                    setAttShowAll(newVal);
                    loadAttendance(attEmpFilter, attMonth, attYear, newVal);
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-colors ${
                    attShowAll ? 'bg-navy-900 text-white border-navy-900' : 'bg-slate-100 text-navy-700 border-slate-200'
                  }`}
                >
                  {attShowAll ? 'Filtered View' : 'Show All Logs'}
                </button>
              </div>

              {/* Record Attendance Button */}
              <button
                onClick={handleOpenAddAttendance}
                className="px-4 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-sm flex items-center justify-center gap-2 transition-all hover:scale-105 active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>Record Attendance</span>
              </button>
            </div>

            {/* Attendance Table */}
            <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-4">Employee ID</th>
                      <th className="py-3.5 px-4">Date</th>
                      <th className="py-3.5 px-4">Status</th>
                      <th className="py-3.5 px-4 text-center">Check In</th>
                      <th className="py-3.5 px-4 text-center">Check Out</th>
                      <th className="py-3.5 px-4 text-center">Break (Hrs)</th>
                      <th className="py-3.5 px-4 text-right">Total Hours</th>
                      <th className="py-3.5 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {attendanceRecords.map((r, idx) => (
                      <tr key={`${r.employee_id}-${r.date}-${idx}`} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3.5 px-4 font-mono font-bold text-tealbrand">{r.employee_id}</td>
                        <td className="py-3.5 px-4 font-medium text-navy-900">{r.date}</td>
                        <td className="py-3.5 px-4">
                          <span
                            className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                              r.status === 'Present'
                                ? 'bg-emerald-100 text-emerald-800'
                                : r.status === 'Absent'
                                ? 'bg-rose-100 text-rose-800'
                                : r.status === 'Half-day'
                                ? 'bg-amber-100 text-amber-800'
                                : 'bg-purple-100 text-purple-800'
                            }`}
                          >
                            {r.status}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-center font-mono text-navy-700">{r.check_in || '—'}</td>
                        <td className="py-3.5 px-4 text-center font-mono text-navy-700">{r.check_out || '—'}</td>
                        <td className="py-3.5 px-4 text-center font-mono text-navy-700">{r.break_duration ?? 0}</td>
                        <td className="py-3.5 px-4 text-right font-mono font-bold text-navy-900">
                          {Number(r.total_working_hours || 0).toFixed(1)} hrs
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => handleDeleteAttendance(r.employee_id, r.date)}
                            className="p-1.5 rounded-lg hover:bg-rose-50 text-rose-600 transition-colors"
                            title="Delete log"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                    {attendanceRecords.length === 0 && (
                      <tr>
                        <td colSpan="8" className="py-8 text-center text-navy-400">
                          No attendance records found for this period.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 4: LEAVE MANAGEMENT
        ============================================================ */}
        {activeTab === 'leaves' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Header & Apply Button */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
              <div>
                <h3 className="font-bold text-navy-900 text-base">Leave Applications & Approval Workflow</h3>
                <p className="text-xs text-navy-500">Track and manage employee leave balances and decisions</p>
              </div>

              <button
                onClick={() => setLeaveModalOpen(true)}
                className="px-4 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-sm flex items-center gap-2 transition-all hover:scale-105 active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>Apply For Leave</span>
              </button>
            </div>

            {/* Leaves Table */}
            <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-4">Leave ID</th>
                      <th className="py-3.5 px-4">Employee</th>
                      <th className="py-3.5 px-4">Duration</th>
                      <th className="py-3.5 px-4">Leave Type</th>
                      <th className="py-3.5 px-4">Reason</th>
                      <th className="py-3.5 px-4 text-center">Status</th>
                      <th className="py-3.5 px-4 text-right">Decision / Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {leaves.map((lv) => (
                      <tr key={lv.leave_id} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3.5 px-4 font-mono font-bold text-tealbrand">{lv.leave_id}</td>
                        <td className="py-3.5 px-4">
                          <div className="font-semibold text-navy-900">{lv.employee_name || lv.employee_id}</div>
                          <div className="text-xs text-navy-500">{lv.department || lv.employee_id}</div>
                        </td>
                        <td className="py-3.5 px-4 font-mono text-navy-700 text-xs">
                          {lv.start_date} <span className="text-navy-400">to</span> {lv.end_date}
                        </td>
                        <td className="py-3.5 px-4">
                          <span
                            className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                              lv.leave_type === 'Paid Leave'
                                ? 'bg-tealbrand/10 text-tealbrand'
                                : 'bg-slate-100 text-slate-700'
                            }`}
                          >
                            {lv.leave_type}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-navy-600 text-xs max-w-xs truncate">{lv.reason}</td>
                        <td className="py-3.5 px-4 text-center">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-extrabold ${
                              lv.status === 'Approved'
                                ? 'bg-emerald-100 text-emerald-800'
                                : lv.status === 'Rejected'
                                ? 'bg-rose-100 text-rose-800'
                                : 'bg-amber-100 text-amber-800'
                            }`}
                          >
                            {lv.status}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <div className="flex items-center justify-end gap-2">
                            {lv.status === 'Pending' && (
                              <>
                                <button
                                  onClick={() => handleLeaveDecision(lv.leave_id, 'Approved')}
                                  className="px-2.5 py-1 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold transition-all flex items-center gap-1"
                                >
                                  <Check className="w-3.5 h-3.5" /> Approve
                                </button>
                                <button
                                  onClick={() => handleLeaveDecision(lv.leave_id, 'Rejected')}
                                  className="px-2.5 py-1 rounded-lg bg-rose-500 hover:bg-rose-600 text-white text-xs font-bold transition-all flex items-center gap-1"
                                >
                                  <X className="w-3.5 h-3.5" /> Reject
                                </button>
                              </>
                            )}
                            <button
                              onClick={() => handleDeleteLeave(lv.leave_id)}
                              className="p-1 rounded-lg text-slate-400 hover:text-rose-600 transition-colors"
                              title="Delete record"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {leaves.length === 0 && (
                      <tr>
                        <td colSpan="7" className="py-8 text-center text-navy-400">
                          No leave requests recorded.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 5: COMPENSATION MANAGEMENT
        ============================================================ */}
        {activeTab === 'compensation' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
              <div>
                <h3 className="font-bold text-navy-900 text-base">Employee Compensation Structures</h3>
                <p className="text-xs text-navy-500">
                  Allowances (HRA, Transport, Medical), performance bonuses, and custom deductions
                </p>
              </div>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-4">Emp ID</th>
                      <th className="py-3.5 px-4">Name</th>
                      <th className="py-3.5 px-4">Department</th>
                      <th className="py-3.5 px-4 text-right">HRA</th>
                      <th className="py-3.5 px-4 text-right">Transport</th>
                      <th className="py-3.5 px-4 text-right">Medical</th>
                      <th className="py-3.5 px-4 text-right">Bonus</th>
                      <th className="py-3.5 px-4 text-right">Other Deduct</th>
                      <th className="py-3.5 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {compensations.map((c) => (
                      <tr key={c.employee_id} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3.5 px-4 font-mono font-bold text-tealbrand">{c.employee_id}</td>
                        <td className="py-3.5 px-4 font-semibold text-navy-900">{c.employee_name}</td>
                        <td className="py-3.5 px-4 text-navy-700">{c.department}</td>
                        <td className="py-3.5 px-4 text-right font-mono">₹{Number(c.hra || 0).toLocaleString('en-IN')}</td>
                        <td className="py-3.5 px-4 text-right font-mono">₹{Number(c.transport_allowance || 0).toLocaleString('en-IN')}</td>
                        <td className="py-3.5 px-4 text-right font-mono">₹{Number(c.medical_allowance || 0).toLocaleString('en-IN')}</td>
                        <td className="py-3.5 px-4 text-right font-mono font-bold text-emerald-600">
                          ₹{Number(c.performance_bonus || 0).toLocaleString('en-IN')}
                        </td>
                        <td className="py-3.5 px-4 text-right font-mono text-rose-600">
                          ₹{Number(c.other_deductions || 0).toLocaleString('en-IN')}
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => handleOpenEditCompensation(c)}
                            className="px-3 py-1.5 rounded-xl bg-tealbrand/10 hover:bg-tealbrand hover:text-white text-tealbrand text-xs font-bold transition-all"
                          >
                            Edit
                          </button>
                        </td>
                      </tr>
                    ))}
                    {compensations.length === 0 && (
                      <tr>
                        <td colSpan="9" className="py-8 text-center text-navy-400">
                          No compensation records found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 6: PAYROLL PROCESSING
        ============================================================ */}
        {activeTab === 'payroll' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Control Bar */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-navy-700">Select Month:</span>
                  <select
                    value={payrollMonth}
                    onChange={(e) => {
                      const m = parseInt(e.target.value, 10);
                      setPayrollMonth(m);
                      loadPayroll(m, payrollYear);
                    }}
                    className="px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {[...Array(12)].map((_, i) => (
                      <option key={i + 1} value={i + 1}>
                        Month {i + 1}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-navy-700">Year:</span>
                  <input
                    type="number"
                    value={payrollYear}
                    onChange={(e) => {
                      const y = parseInt(e.target.value, 10);
                      setPayrollYear(y);
                      loadPayroll(payrollMonth, y);
                    }}
                    className="w-24 px-3 py-2 rounded-xl border border-slate-200 text-sm"
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3">
                <button
                  onClick={handleFinalizeAllDrafts}
                  className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-navy-800 font-bold text-sm transition-all"
                >
                  Finalize All Drafts
                </button>

                <button
                  onClick={handleGeneratePayroll}
                  disabled={isProcessingPayroll}
                  className="px-5 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-md flex items-center gap-2 transition-all hover:scale-105 active:scale-95 disabled:opacity-75"
                >
                  <Sparkles className={`w-4 h-4 ${isProcessingPayroll ? 'animate-spin' : ''}`} />
                  <span>{isProcessingPayroll ? 'Calculating...' : 'Generate Monthly Payroll'}</span>
                </button>
              </div>
            </div>

            {/* Generated Payroll Table */}
            <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3.5 px-4">Payroll ID</th>
                      <th className="py-3.5 px-4">Employee</th>
                      <th className="py-3.5 px-4">Period</th>
                      <th className="py-3.5 px-4 text-right">Gross (₹)</th>
                      <th className="py-3.5 px-4 text-right">Deductions (₹)</th>
                      <th className="py-3.5 px-4 text-right">Net Salary (₹)</th>
                      <th className="py-3.5 px-4 text-center">Status</th>
                      <th className="py-3.5 px-4 text-center">Payment</th>
                      <th className="py-3.5 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {payrolls.map((rec) => {
                      const b = rec.salary_breakdown || {};
                      return (
                        <tr key={rec.payroll_id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="py-3.5 px-4 font-mono font-bold text-tealbrand">{rec.payroll_id}</td>
                          <td className="py-3.5 px-4">
                            <div className="font-semibold text-navy-900">{rec.employee_name}</div>
                            <div className="text-xs text-navy-500">
                              {rec.employee_id} • {rec.department}
                            </div>
                          </td>
                          <td className="py-3.5 px-4 font-mono text-xs">
                            {String(rec.month).padStart(2, '0')}/{rec.year}
                          </td>
                          <td className="py-3.5 px-4 text-right font-mono">
                            ₹{Number(b.gross_salary || 0).toLocaleString('en-IN')}
                          </td>
                          <td className="py-3.5 px-4 text-right font-mono text-rose-600">
                            ₹{Number(b.total_deductions || 0).toLocaleString('en-IN')}
                          </td>
                          <td className="py-3.5 px-4 text-right font-mono font-bold text-tealbrand-dark text-base">
                            ₹{Number(b.net_salary || 0).toLocaleString('en-IN')}
                          </td>
                          <td className="py-3.5 px-4 text-center">
                            <span
                              className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                                rec.status === 'Finalized'
                                  ? 'bg-emerald-100 text-emerald-800'
                                  : 'bg-amber-100 text-amber-800'
                              }`}
                            >
                              {rec.status}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 text-center">
                            <span
                              className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                                rec.payment_status === 'Paid'
                                  ? 'bg-purple-100 text-purple-800'
                                  : 'bg-slate-100 text-slate-700'
                              }`}
                            >
                              {rec.payment_status}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <div className="flex items-center justify-end gap-2">
                              <button
                                onClick={() => handleViewBreakdown(rec)}
                                className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-navy-700 text-xs font-semibold flex items-center gap-1"
                              >
                                <Eye className="w-3.5 h-3.5" /> Breakdown
                              </button>
                              {rec.status === 'Draft' && (
                                <button
                                  onClick={() => handleFinalizePayroll(rec.payroll_id)}
                                  className="px-2.5 py-1 rounded-lg bg-tealbrand hover:bg-tealbrand-dark text-white text-xs font-semibold"
                                >
                                  Finalize
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                    {payrolls.length === 0 && (
                      <tr>
                        <td colSpan="9" className="py-8 text-center text-navy-400">
                          No payroll generated for {payrollMonth}/{payrollYear}. Click "Generate Monthly Payroll" to run calculations.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 7: PAYSLIPS
        ============================================================ */}
        {activeTab === 'payslips' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Payslip Generator Control Bar */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-navy-700">Select Employee:</span>
                  <select
                    value={payslipEmpId}
                    onChange={(e) => setPayslipEmpId(e.target.value)}
                    className="px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {employees.map((emp) => (
                      <option key={emp.employee_id} value={emp.employee_id}>
                        {emp.employee_id} - {emp.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-navy-700">Month:</span>
                  <select
                    value={payslipMonth}
                    onChange={(e) => setPayslipMonth(parseInt(e.target.value, 10))}
                    className="px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {[...Array(12)].map((_, i) => (
                      <option key={i + 1} value={i + 1}>
                        Month {i + 1}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-navy-700">Year:</span>
                  <input
                    type="number"
                    value={payslipYear}
                    onChange={(e) => setPayslipYear(parseInt(e.target.value, 10))}
                    className="w-24 px-3 py-2 rounded-xl border border-slate-200 text-sm"
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3">
                <button
                  onClick={handlePreviewPayslip}
                  disabled={payslipLoading}
                  className="px-4 py-2.5 rounded-xl bg-navy-900 hover:bg-navy-800 text-white font-bold text-sm shadow-sm flex items-center gap-2 transition-all hover:scale-105 active:scale-95"
                >
                  <Eye className="w-4 h-4 text-mint-300" />
                  <span>{payslipLoading ? 'Generating...' : 'Preview Payslip'}</span>
                </button>

                <button
                  onClick={handleDownloadPayslip}
                  disabled={!payslipText}
                  className="px-4 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-sm flex items-center gap-2 transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
                >
                  <Download className="w-4 h-4" />
                  <span>Download .txt File</span>
                </button>
              </div>
            </div>

            {/* Document Preview Area */}
            <div className="bg-[#1E1E2E] text-emerald-400 p-6 rounded-3xl shadow-xl font-mono text-xs sm:text-sm border border-slate-700 overflow-x-auto min-h-[380px] relative">
              <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-700/60 text-slate-400 text-xs">
                <span>PAYSPHERE ITEMISED SALARY DOCUMENT PREVIEW</span>
                {payslipText && (
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(payslipText);
                      showToast('Payslip text copied to clipboard!');
                    }}
                    className="flex items-center gap-1 text-slate-300 hover:text-white transition-colors"
                  >
                    <Copy className="w-3.5 h-3.5" /> Copy Text
                  </button>
                )}
              </div>

              {payslipText ? (
                <pre className="whitespace-pre text-slate-100 font-mono leading-relaxed">{payslipText}</pre>
              ) : (
                <div className="h-64 flex flex-col items-center justify-center text-slate-400 gap-2">
                  <FileText className="w-8 h-8 opacity-40" />
                  <p>Select an employee & month above, then click "Preview Payslip".</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============================================================
            TAB 8: PAYMENT HISTORY
        ============================================================ */}
        {activeTab === 'payments' && (
          <div className="space-y-8 animate-fadeIn">
            {/* Pending Payments Section */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-navy-900 text-base">Pending Payments Awaiting Disbursement</h3>
                  <p className="text-xs text-navy-500">Finalized payrolls ready to be settled via Bank Transfer or UPI</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold">
                  {pendingPayments.length} Pending
                </span>
              </div>

              {/* Disbursement Action Form */}
              <form
                onSubmit={handleDisbursePayment}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-wrap items-center gap-3"
              >
                <div className="flex-1 min-w-[200px]">
                  <label className="block text-[11px] font-bold text-navy-600 mb-1">Select Payroll</label>
                  <select
                    value={selectedPendingPayrollId}
                    onChange={(e) => setSelectedPendingPayrollId(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    <option value="">-- Choose Pending Payroll --</option>
                    {pendingPayments.map((p) => (
                      <option key={p.payroll_id} value={p.payroll_id}>
                        {p.payroll_id} - {p.employee_name} (₹{p.salary_breakdown?.net_salary?.toLocaleString('en-IN')})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="w-40">
                  <label className="block text-[11px] font-bold text-navy-600 mb-1">Method</label>
                  <select
                    value={paymentMethod}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {PAYMENT_METHODS.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex-1 min-w-[180px]">
                  <label className="block text-[11px] font-bold text-navy-600 mb-1">Transaction / Ref No.</label>
                  <input
                    type="text"
                    placeholder="e.g. UTR9283741"
                    value={transactionRef}
                    onChange={(e) => setTransactionRef(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                  />
                </div>

                <div className="self-end pt-1">
                  <button
                    type="submit"
                    disabled={!selectedPendingPayrollId || !transactionRef}
                    className="px-5 py-2.5 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-sm flex items-center gap-2 transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
                  >
                    <CreditCard className="w-4 h-4" />
                    <span>Disburse Payment</span>
                  </button>
                </div>
              </form>

              {/* Pending Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3 px-4">Payroll ID</th>
                      <th className="py-3 px-4">Employee</th>
                      <th className="py-3 px-4">Department</th>
                      <th className="py-3 px-4">Period</th>
                      <th className="py-3 px-4 text-right">Net Salary</th>
                      <th className="py-3 px-4 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {pendingPayments.map((p) => (
                      <tr key={p.payroll_id} className="hover:bg-slate-50/80">
                        <td className="py-3 px-4 font-mono font-bold text-tealbrand">{p.payroll_id}</td>
                        <td className="py-3 px-4 font-semibold text-navy-900">{p.employee_name}</td>
                        <td className="py-3 px-4 text-navy-700">{p.department}</td>
                        <td className="py-3 px-4 font-mono text-xs">
                          {String(p.month).padStart(2, '0')}/{p.year}
                        </td>
                        <td className="py-3 px-4 text-right font-mono font-bold text-tealbrand-dark">
                          ₹{Number(p.salary_breakdown?.net_salary || 0).toLocaleString('en-IN')}
                        </td>
                        <td className="py-3 px-4 text-center">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">
                            Awaiting Disbursement
                          </span>
                        </td>
                      </tr>
                    ))}
                    {pendingPayments.length === 0 && (
                      <tr>
                        <td colSpan="6" className="py-6 text-center text-navy-400">
                          No pending payments awaiting disbursement.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Completed Payments History Section */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm space-y-4">
              <div>
                <h3 className="font-bold text-navy-900 text-base">Completed Disbursement Transactions</h3>
                <p className="text-xs text-navy-500">Audited settlement history with bank reference identifiers</p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200/80 text-navy-600 font-bold text-xs uppercase tracking-wider">
                    <tr>
                      <th className="py-3 px-4">Transaction ID</th>
                      <th className="py-3 px-4">Payroll ID</th>
                      <th className="py-3 px-4">Employee</th>
                      <th className="py-3 px-4 text-right">Amount (₹)</th>
                      <th className="py-3 px-4">Method</th>
                      <th className="py-3 px-4">Reference No</th>
                      <th className="py-3 px-4">Payment Date</th>
                      <th className="py-3 px-4 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {completedPayments.map((pmt) => (
                      <tr key={pmt.payment_id} className="hover:bg-slate-50/80">
                        <td className="py-3 px-4 font-mono font-bold text-purple-700">{pmt.payment_id}</td>
                        <td className="py-3 px-4 font-mono text-tealbrand">{pmt.payroll_id}</td>
                        <td className="py-3 px-4 font-semibold text-navy-900">{pmt.employee_name || pmt.employee_id}</td>
                        <td className="py-3 px-4 text-right font-mono font-bold text-emerald-700">
                          ₹{Number(pmt.amount || 0).toLocaleString('en-IN')}
                        </td>
                        <td className="py-3 px-4">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-navy-800">
                            {pmt.payment_method}
                          </span>
                        </td>
                        <td className="py-3 px-4 font-mono text-xs text-navy-700">{pmt.transaction_ref}</td>
                        <td className="py-3 px-4 font-mono text-xs text-navy-500">{pmt.payment_date}</td>
                        <td className="py-3 px-4 text-center">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                            Paid
                          </span>
                        </td>
                      </tr>
                    ))}
                    {completedPayments.length === 0 && (
                      <tr>
                        <td colSpan="8" className="py-8 text-center text-navy-400">
                          No completed disbursements recorded yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================
            MODAL 1: ADD / EDIT EMPLOYEE
        ============================================================ */}
        {employeeModalOpen && (
          <div className="fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <h3 className="text-lg font-bold text-navy-900">
                  {editingEmployee ? `Edit Employee ${employeeForm.employee_id}` : 'Add New Employee'}
                </h3>
                <button onClick={() => setEmployeeModalOpen(false)} className="p-1 text-slate-400 hover:text-navy-900">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleSaveEmployee} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Employee ID</label>
                    <input
                      type="text"
                      disabled={!!editingEmployee}
                      value={employeeForm.employee_id}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, employee_id: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono bg-slate-50"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Full Name</label>
                    <input
                      type="text"
                      value={employeeForm.name}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, name: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      placeholder="e.g. John Doe"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Email</label>
                    <input
                      type="email"
                      value={employeeForm.email}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, email: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      placeholder="john@company.com"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Contact No</label>
                    <input
                      type="text"
                      value={employeeForm.contact}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, contact: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      placeholder="9876543210"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Department</label>
                    <select
                      value={employeeForm.department}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, department: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                    >
                      {DEPARTMENTS.filter((d) => d !== 'All').map((d) => (
                        <option key={d} value={d}>
                          {d}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Designation</label>
                    <input
                      type="text"
                      value={employeeForm.designation}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, designation: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      placeholder="e.g. Developer"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Employment Type</label>
                    <select
                      value={employeeForm.employment_type}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, employment_type: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                    >
                      <option value="Salaried">Salaried</option>
                      <option value="Hourly">Hourly</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">
                      {employeeForm.employment_type === 'Salaried' ? 'Basic Salary (₹/mo)' : 'Hourly Rate (₹/hr)'}
                    </label>
                    <input
                      type="number"
                      value={
                        employeeForm.employment_type === 'Salaried'
                          ? employeeForm.basic_salary
                          : employeeForm.hourly_rate
                      }
                      onChange={(e) => {
                        const val = parseFloat(e.target.value) || 0;
                        if (employeeForm.employment_type === 'Salaried') {
                          setEmployeeForm({ ...employeeForm, basic_salary: val });
                        } else {
                          setEmployeeForm({ ...employeeForm, hourly_rate: val });
                        }
                      }}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Joining Date</label>
                    <input
                      type="date"
                      value={employeeForm.joining_date}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, joining_date: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Status</label>
                    <select
                      value={employeeForm.status}
                      onChange={(e) => setEmployeeForm({ ...employeeForm, status: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                    >
                      <option value="Active">Active</option>
                      <option value="Inactive">Inactive</option>
                    </select>
                  </div>
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setEmployeeModalOpen(false)}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-semibold text-navy-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white text-sm font-bold shadow-sm"
                  >
                    {editingEmployee ? 'Update Employee' : 'Add Employee'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ============================================================
            MODAL 2: RECORD ATTENDANCE
        ============================================================ */}
        {attendanceModalOpen && (
          <div className="fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-100">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <h3 className="text-lg font-bold text-navy-900">Record Daily Attendance</h3>
                <button onClick={() => setAttendanceModalOpen(false)} className="p-1 text-slate-400 hover:text-navy-900">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleSaveAttendance} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-navy-700 mb-1">Employee</label>
                  <select
                    value={attendanceForm.employee_id}
                    onChange={(e) => setAttendanceForm({ ...attendanceForm, employee_id: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {employees.map((emp) => (
                      <option key={emp.employee_id} value={emp.employee_id}>
                        {emp.employee_id} - {emp.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Date</label>
                    <input
                      type="date"
                      value={attendanceForm.date}
                      onChange={(e) => setAttendanceForm({ ...attendanceForm, date: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Status</label>
                    <select
                      value={attendanceForm.status}
                      onChange={(e) => setAttendanceForm({ ...attendanceForm, status: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                    >
                      {ATTENDANCE_STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Check In (HH:MM)</label>
                    <input
                      type="text"
                      value={attendanceForm.check_in}
                      onChange={(e) => setAttendanceForm({ ...attendanceForm, check_in: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                      placeholder="09:00"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Check Out (HH:MM)</label>
                    <input
                      type="text"
                      value={attendanceForm.check_out}
                      onChange={(e) => setAttendanceForm({ ...attendanceForm, check_out: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                      placeholder="18:00"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-navy-700 mb-1">Break Duration (Hours)</label>
                  <input
                    type="number"
                    step="0.5"
                    value={attendanceForm.break_duration}
                    onChange={(e) =>
                      setAttendanceForm({ ...attendanceForm, break_duration: parseFloat(e.target.value) || 0 })
                    }
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                  />
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setAttendanceModalOpen(false)}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-semibold text-navy-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white text-sm font-bold shadow-sm"
                  >
                    Save Attendance
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ============================================================
            MODAL 3: APPLY LEAVE
        ============================================================ */}
        {leaveModalOpen && (
          <div className="fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-100">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <h3 className="text-lg font-bold text-navy-900">Apply For Leave</h3>
                <button onClick={() => setLeaveModalOpen(false)} className="p-1 text-slate-400 hover:text-navy-900">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleApplyLeave} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-navy-700 mb-1">Employee</label>
                  <select
                    value={leaveForm.employee_id}
                    onChange={(e) => setLeaveForm({ ...leaveForm, employee_id: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {employees.map((emp) => (
                      <option key={emp.employee_id} value={emp.employee_id}>
                        {emp.employee_id} - {emp.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Start Date</label>
                    <input
                      type="date"
                      value={leaveForm.start_date}
                      onChange={(e) => setLeaveForm({ ...leaveForm, start_date: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">End Date</label>
                    <input
                      type="date"
                      value={leaveForm.end_date}
                      onChange={(e) => setLeaveForm({ ...leaveForm, end_date: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-navy-700 mb-1">Leave Type</label>
                  <select
                    value={leaveForm.leave_type}
                    onChange={(e) => setLeaveForm({ ...leaveForm, leave_type: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm bg-white"
                  >
                    {LEAVE_TYPES.map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-navy-700 mb-1">Reason</label>
                  <textarea
                    rows="3"
                    value={leaveForm.reason}
                    onChange={(e) => setLeaveForm({ ...leaveForm, reason: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm"
                    placeholder="Brief explanation for leave..."
                    required
                  />
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setLeaveModalOpen(false)}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-semibold text-navy-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white text-sm font-bold shadow-sm"
                  >
                    Submit Application
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ============================================================
            MODAL 4: EDIT COMPENSATION
        ============================================================ */}
        {compModalOpen && (
          <div className="fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <h3 className="text-lg font-bold text-navy-900">
                  Edit Compensation for {compForm.employee_id}
                </h3>
                <button onClick={() => setCompModalOpen(false)} className="p-1 text-slate-400 hover:text-navy-900">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleSaveCompensation} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">HRA (₹)</label>
                    <input
                      type="number"
                      value={compForm.hra}
                      onChange={(e) => setCompForm({ ...compForm, hra: parseFloat(e.target.value) || 0 })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Transport Allowance (₹)</label>
                    <input
                      type="number"
                      value={compForm.transport_allowance}
                      onChange={(e) =>
                        setCompForm({ ...compForm, transport_allowance: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Medical Allowance (₹)</label>
                    <input
                      type="number"
                      value={compForm.medical_allowance}
                      onChange={(e) =>
                        setCompForm({ ...compForm, medical_allowance: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Other Allowances (₹)</label>
                    <input
                      type="number"
                      value={compForm.other_allowances}
                      onChange={(e) =>
                        setCompForm({ ...compForm, other_allowances: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Performance Bonus (₹)</label>
                    <input
                      type="number"
                      value={compForm.performance_bonus}
                      onChange={(e) =>
                        setCompForm({ ...compForm, performance_bonus: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono text-emerald-600 font-bold"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-navy-700 mb-1">Other Deductions (₹)</label>
                    <input
                      type="number"
                      value={compForm.other_deductions}
                      onChange={(e) =>
                        setCompForm({ ...compForm, other_deductions: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-sm font-mono text-rose-600 font-bold"
                    />
                  </div>
                </div>

                {/* Total Allowance Preview */}
                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 text-xs flex justify-between font-bold text-navy-800">
                  <span>Total Allowances:</span>
                  <span className="text-tealbrand-dark font-mono">
                    ₹
                    {(
                      Number(compForm.hra) +
                      Number(compForm.transport_allowance) +
                      Number(compForm.medical_allowance) +
                      Number(compForm.other_allowances) +
                      Number(compForm.performance_bonus)
                    ).toLocaleString('en-IN')}
                  </span>
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setCompModalOpen(false)}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-semibold text-navy-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-tealbrand hover:bg-tealbrand-dark text-white text-sm font-bold shadow-sm"
                  >
                    Save Compensation
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ============================================================
            MODAL 5: DETAILED PAYROLL BREAKDOWN
        ============================================================ */}
        {breakdownModalOpen && selectedBreakdown && (
          <div className="fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-xl w-full p-6 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <div>
                  <h3 className="text-lg font-bold text-navy-900">
                    Detailed Salary Breakdown — {selectedBreakdown.payroll?.payroll_id}
                  </h3>
                  <p className="text-xs text-navy-500">
                    {selectedBreakdown.payroll?.employee_name} ({selectedBreakdown.payroll?.employee_id})
                  </p>
                </div>
                <button onClick={() => setBreakdownModalOpen(false)} className="p-1 text-slate-400 hover:text-navy-900">
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Formatted Code View of Breakdown */}
              <div className="bg-[#1E1E2E] text-slate-100 p-5 rounded-2xl font-mono text-xs overflow-x-auto leading-relaxed shadow-inner">
                <pre>{selectedBreakdown.payslip_text}</pre>
              </div>

              <div className="pt-5 flex items-center justify-end gap-3">
                <button
                  onClick={() => setBreakdownModalOpen(false)}
                  className="px-5 py-2 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-sm font-bold"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
