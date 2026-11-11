/**
 * payrollApi.js - Frontend API Client for PaySphere Backend
 *
 * Connects the React UI to the Python Flask REST API server (api_server.py).
 * Provides robust error handling, toast-friendly errors, and fallback support.
 */

const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(url, config);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const errorMsg = data.error || data.message || `Request failed with status ${res.status}`;
      const err = new Error(errorMsg);
      err.status = res.status;
      err.data = data;
      throw err;
    }

    return data;
  } catch (error) {
    console.warn(`API call failed: ${url}`, error.message);
    throw error;
  }
}

export const payrollApi = {
  // System Health
  checkHealth: () => request('/health'),

  // Dashboard Metrics
  getDashboardStats: () => request('/dashboard/stats'),

  // Employees
  getEmployees: (params = {}) => {
    const query = new URLSearchParams();
    if (params.search) query.append('search', params.search);
    if (params.department && params.department !== 'All') query.append('department', params.department);
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request(`/employees${qStr}`);
  },
  addEmployee: (empData) => request('/employees', {
    method: 'POST',
    body: JSON.stringify(empData),
  }),
  updateEmployee: (empId, empData) => request(`/employees/${empId}`, {
    method: 'PUT',
    body: JSON.stringify(empData),
  }),
  deleteEmployee: (empId) => request(`/employees/${empId}`, {
    method: 'DELETE',
  }),

  // Attendance
  getAttendance: (params = {}) => {
    const query = new URLSearchParams();
    if (params.employee_id && params.employee_id !== 'ALL') query.append('employee_id', params.employee_id);
    if (params.month) query.append('month', params.month);
    if (params.year) query.append('year', params.year);
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request(`/attendance${qStr}`);
  },
  addAttendance: (record) => request('/attendance', {
    method: 'POST',
    body: JSON.stringify(record),
  }),
  updateAttendance: (record) => request('/attendance', {
    method: 'PUT',
    body: JSON.stringify(record),
  }),
  deleteAttendance: (empId, date) => request(`/attendance?employee_id=${empId}&date=${date}`, {
    method: 'DELETE',
  }),

  // Leaves
  getLeaves: () => request('/leaves'),
  applyLeave: (leaveData) => request('/leaves', {
    method: 'POST',
    body: JSON.stringify(leaveData),
  }),
  decideLeave: (leaveId, status) => request(`/leaves/${leaveId}/decision`, {
    method: 'POST',
    body: JSON.stringify({ status }),
  }),
  deleteLeave: (leaveId) => request(`/leaves/${leaveId}`, {
    method: 'DELETE',
  }),

  // Compensation
  getCompensationList: () => request('/compensation'),
  getEmployeeCompensation: (empId) => request(`/compensation/${empId}`),
  updateCompensation: (compData) => request('/compensation', {
    method: 'POST',
    body: JSON.stringify(compData),
  }),

  // Payroll Processing
  getPayroll: (month, year) => {
    const query = new URLSearchParams();
    if (month) query.append('month', month);
    if (year) query.append('year', year);
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request(`/payroll${qStr}`);
  },
  generatePayrollBatch: (month, year) => request('/payroll/generate', {
    method: 'POST',
    body: JSON.stringify({ month, year }),
  }),
  finalizePayroll: (payrollId) => request(`/payroll/finalize/${payrollId}`, {
    method: 'POST',
  }),
  finalizeAllDrafts: (month, year) => request('/payroll/finalize-all', {
    method: 'POST',
    body: JSON.stringify({ month, year }),
  }),
  getPayrollBreakdown: (payrollId) => request(`/payroll/breakdown/${payrollId}`),

  // Payslips
  previewPayslip: (employee_id, month, year) =>
    request(`/payslips/preview?employee_id=${employee_id}&month=${month}&year=${year}`),
  downloadPayslip: (employee_id, month, year) => request('/payslips/download', {
    method: 'POST',
    body: JSON.stringify({ employee_id, month, year }),
  }),

  // Payments / Disbursements
  getPendingPayments: () => request('/payments/pending'),
  getPaymentHistory: () => request('/payments/history'),
  disbursePayment: (payrollId, paymentMethod, transactionRef) => request('/payments/disburse', {
    method: 'POST',
    body: JSON.stringify({
      payroll_id: payrollId,
      payment_method: paymentMethod,
      transaction_ref: transactionRef,
    }),
  }),
};
