import React, { useState } from 'react';
import {
  Users,
  TrendingUp,
  CreditCard,
  CalendarCheck2,
  Filter,
  Download,
  CheckCircle,
  Clock,
  Sparkles,
  FileSpreadsheet,
  ChevronRight,
  Eye,
  CheckCircle2,
  DollarSign
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { monthlyPayrollData, departmentStats, sampleEmployees } from '../data/mockData';
import confetti from 'canvas-confetti';

export default function DashboardPreviewSection() {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedDept, setSelectedDept] = useState('All');
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [isProcessingPayroll, setIsProcessingPayroll] = useState(false);
  const [payrollSuccessMessage, setPayrollSuccessMessage] = useState(null);

  // Filter employees
  const filteredEmployees = selectedDept === 'All'
    ? sampleEmployees
    : sampleEmployees.filter(e => e.department === selectedDept);

  // Simulate generating batch payroll
  const handleBatchPayrollRun = () => {
    setIsProcessingPayroll(true);
    setPayrollSuccessMessage(null);

    setTimeout(() => {
      setIsProcessingPayroll(false);
      setPayrollSuccessMessage('June 2026 Batch Payroll Successfully Finalized! ₹18,45,000 computed for 128 employees.');
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#168C87', '#54C7C1', '#8D72DF', '#FFB067']
        });
      } catch (err) {
        // fallback if canvas not available
      }
    }, 1200);
  };

  return (
    <section id="preview" className="py-24 px-6 md:px-12 lg:px-16 bg-[#F9FBFA] relative">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between mb-12 gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-tealbrand/10 border border-tealbrand/20 text-tealbrand text-xs font-bold uppercase tracking-wider mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              Live Interactive Workspace
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-navy-900 tracking-tight leading-tight">
              Enterprise Payroll Dashboard
            </h2>
            <p className="mt-2 text-base text-navy-800/70 max-w-xl">
              Inspect real-time monthly disbursement trends, department allocations, and employee compensation models.
            </p>
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleBatchPayrollRun}
              disabled={isProcessingPayroll}
              className="px-5 py-3 rounded-2xl bg-tealbrand hover:bg-tealbrand-dark text-white font-bold text-sm shadow-md shadow-tealbrand/20 flex items-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-75"
            >
              <Sparkles className={`w-4 h-4 ${isProcessingPayroll ? 'animate-spin' : ''}`} />
              <span>{isProcessingPayroll ? 'Calculating Payroll...' : 'Run June Payroll'}</span>
            </button>
          </div>
        </div>

        {/* Success Alert Banner */}
        {payrollSuccessMessage && (
          <div className="mb-6 p-4 rounded-2xl bg-mint-100 border border-tealbrand/30 flex items-center justify-between shadow-sm animate-fade-in">
            <div className="flex items-center gap-3 text-navy-900 text-sm font-semibold">
              <CheckCircle2 className="w-5 h-5 text-tealbrand" />
              <span>{payrollSuccessMessage}</span>
            </div>
            <button
              onClick={() => setPayrollSuccessMessage(null)}
              className="text-xs font-bold text-tealbrand hover:underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Dashboard Frame (Slight 3D perspective, ultra readable) */}
        <div className="bg-white rounded-[32px] border border-slate-200/90 shadow-[0_20px_50px_-10px_rgba(23,21,61,0.08)] p-6 lg:p-8">
          {/* Top navigation tabs inside preview */}
          <div className="flex flex-wrap items-center justify-between pb-6 mb-6 border-b border-slate-100 gap-4">
            <div className="flex items-center gap-2 p-1.5 bg-[#F2F6F5] rounded-2xl">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === 'overview'
                    ? 'bg-white text-navy-900 shadow-sm'
                    : 'text-slate-500 hover:text-navy-900'
                }`}
              >
                Executive Overview
              </button>
              <button
                onClick={() => setActiveTab('employees')}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === 'employees'
                    ? 'bg-white text-navy-900 shadow-sm'
                    : 'text-slate-500 hover:text-navy-900'
                }`}
              >
                Employee Directory ({sampleEmployees.length})
              </button>
              <button
                onClick={() => setActiveTab('breakdown')}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === 'breakdown'
                    ? 'bg-white text-navy-900 shadow-sm'
                    : 'text-slate-500 hover:text-navy-900'
                }`}
              >
                Department Allocations
              </button>
            </div>

            {/* Quick metrics header */}
            <div className="flex items-center gap-6 text-xs font-semibold text-slate-500">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                Active Cycle: <strong className="text-navy-900">June 2026</strong>
              </span>
              <span className="hidden sm:inline">
                Status: <strong className="text-tealbrand">Finalized</strong>
              </span>
            </div>
          </div>

          {/* TAB 1: EXECUTIVE OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Top 4 KPI Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-[#F7FBF9] border border-slate-100">
                  <div className="flex items-center justify-between text-slate-400 mb-2">
                    <span className="text-xs font-semibold text-navy-800">Total Headcount</span>
                    <Users className="w-4 h-4 text-tealbrand" />
                  </div>
                  <div className="text-2xl font-black text-navy-900">128</div>
                  <span className="text-[11px] text-tealbrand font-semibold">↗ +8.2% from last quarter</span>
                </div>

                <div className="p-4 rounded-2xl bg-[#F7FBF9] border border-slate-100">
                  <div className="flex items-center justify-between text-slate-400 mb-2">
                    <span className="text-xs font-semibold text-navy-800">Monthly Net Payroll</span>
                    <DollarSign className="w-4 h-4 text-accentpurple" />
                  </div>
                  <div className="text-2xl font-black text-navy-900">₹18,45,000</div>
                  <span className="text-[11px] text-slate-400 font-medium">98.4% direct deposited</span>
                </div>

                <div className="p-4 rounded-2xl bg-[#F7FBF9] border border-slate-100">
                  <div className="flex items-center justify-between text-slate-400 mb-2">
                    <span className="text-xs font-semibold text-navy-800">Attendance Rate</span>
                    <CalendarCheck2 className="w-4 h-4 text-rose-500" />
                  </div>
                  <div className="text-2xl font-black text-navy-900">94.8%</div>
                  <span className="text-[11px] text-emerald-600 font-semibold">Healthy organization score</span>
                </div>

                <div className="p-4 rounded-2xl bg-[#F7FBF9] border border-slate-100">
                  <div className="flex items-center justify-between text-slate-400 mb-2">
                    <span className="text-xs font-semibold text-navy-800">Pending Review</span>
                    <Clock className="w-4 h-4 text-amber-500" />
                  </div>
                  <div className="text-2xl font-black text-navy-900">12 slips</div>
                  <span className="text-[11px] text-amber-600 font-semibold">Requires manager signoff</span>
                </div>
              </div>

              {/* Charts Row */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* 6-Month Expenditure Area Chart */}
                <div className="lg:col-span-8 p-5 rounded-2xl bg-[#FAFDFD] border border-slate-100">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="text-sm font-bold text-navy-900">Payroll Expenditure History (6 Months)</h4>
                      <p className="text-xs text-slate-400">Total gross disbursement with basic vs allowances</p>
                    </div>
                    <span className="text-xs font-bold text-tealbrand bg-mint-100 px-2.5 py-1 rounded-full">
                      ₹18.45 Lakhs peak
                    </span>
                  </div>
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={monthlyPayrollData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <defs>
                          <linearGradient id="colorExpenditure" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#168C87" stopOpacity={0.4}/>
                            <stop offset="95%" stopColor="#168C87" stopOpacity={0.0}/>
                          </linearGradient>
                          <linearGradient id="colorBasic" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8D72DF" stopOpacity={0.3}/>
                            <stop offset="95%" stopColor="#8D72DF" stopOpacity={0.0}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2ECE9" />
                        <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                        <YAxis
                          stroke="#94A3B8"
                          fontSize={11}
                          tickLine={false}
                          tickFormatter={(v) => `₹${(v / 100000).toFixed(1)}L`}
                        />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#17153D', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }}
                          formatter={(v) => [`₹${v.toLocaleString('en-IN')}`, 'Amount']}
                        />
                        <Area type="monotone" dataKey="expenditure" stroke="#168C87" strokeWidth={2.5} fillOpacity={1} fill="url(#colorExpenditure)" name="Gross Total" />
                        <Area type="monotone" dataKey="basic" stroke="#8D72DF" strokeWidth={2} fillOpacity={1} fill="url(#colorBasic)" name="Basic Base" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Mini Department Allocation Bar */}
                <div className="lg:col-span-4 p-5 rounded-2xl bg-[#FAFDFD] border border-slate-100 flex flex-col justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-navy-900 mb-1">Department Budget Share</h4>
                    <p className="text-xs text-slate-400 mb-4">Distribution across organizational units</p>
                    <div className="space-y-3">
                      {departmentStats.map((dept) => (
                        <div key={dept.name}>
                          <div className="flex justify-between text-xs font-semibold text-navy-900 mb-1">
                            <span>{dept.name}</span>
                            <span className="text-slate-500">{dept.budget} ({dept.count})</span>
                          </div>
                          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                            <div
                              className="h-full rounded-full"
                              style={{
                                width: `${(dept.count / 128) * 100 * 1.8}%`,
                                backgroundColor: dept.color
                              }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-slate-100 text-xs text-slate-500 flex items-center justify-between">
                    <span>Highest Budget:</span>
                    <strong className="text-navy-900">Engineering (44.4%)</strong>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: EMPLOYEE DIRECTORY */}
          {activeTab === 'employees' && (
            <div className="space-y-4">
              {/* Filter Row */}
              <div className="flex flex-wrap items-center justify-between gap-3 pb-2">
                <div className="flex items-center gap-2">
                  <Filter className="w-4 h-4 text-slate-400" />
                  <span className="text-xs font-bold text-navy-800">Filter Department:</span>
                  {['All', 'Engineering', 'Product & Design', 'Human Resources', 'Operations & Support'].map((d) => (
                    <button
                      key={d}
                      onClick={() => setSelectedDept(d)}
                      className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                        selectedDept === d
                          ? 'bg-tealbrand text-white'
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                    >
                      {d}
                    </button>
                  ))}
                </div>
                <span className="text-xs text-slate-400">Showing {filteredEmployees.length} employees</span>
              </div>

              {/* Employee Table */}
              <div className="overflow-x-auto border border-slate-100 rounded-2xl">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAFDFD] border-b border-slate-100 text-slate-400 font-semibold">
                    <tr>
                      <th className="py-3 px-4">Employee</th>
                      <th className="py-3 px-4">Class Model</th>
                      <th className="py-3 px-4">Department</th>
                      <th className="py-3 px-4">Base / Rate</th>
                      <th className="py-3 px-4">Allowances</th>
                      <th className="py-3 px-4">Deductions</th>
                      <th className="py-3 px-4 font-bold text-navy-900">Net Pay</th>
                      <th className="py-3 px-4">Attendance</th>
                      <th className="py-3 px-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-navy-800">
                    {filteredEmployees.map((emp) => (
                      <tr key={emp.id} className="hover:bg-mint-50/50 transition-colors">
                        <td className="py-3 px-4 flex items-center gap-2.5">
                          <div className="w-7 h-7 rounded-full bg-slate-100 text-navy-900 font-bold flex items-center justify-center text-[10px]">
                            {emp.avatar}
                          </div>
                          <div>
                            <div className="font-bold text-navy-900">{emp.name}</div>
                            <div className="text-[10px] text-slate-400">{emp.id} • {emp.role}</div>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-0.5 rounded-md font-bold text-[10px] ${
                            emp.type === 'Salaried'
                              ? 'bg-blue-50 text-blue-700 border border-blue-100'
                              : 'bg-purple-50 text-purple-700 border border-purple-100'
                          }`}>
                            {emp.type}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-slate-600">{emp.department}</td>
                        <td className="py-3 px-4">
                          {emp.type === 'Salaried'
                            ? `₹${emp.basicSalary.toLocaleString('en-IN')}`
                            : `₹${emp.hourlyRate}/hr (${emp.hoursWorked}h)`}
                        </td>
                        <td className="py-3 px-4 text-emerald-600 font-medium">+₹{emp.allowances.toLocaleString('en-IN')}</td>
                        <td className="py-3 px-4 text-rose-500 font-medium">-₹{emp.deductions.toLocaleString('en-IN')}</td>
                        <td className="py-3 px-4 font-extrabold text-navy-900">
                          ₹{emp.netSalary.toLocaleString('en-IN')}
                        </td>
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-1.5">
                            <div className="w-12 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                              <div
                                className="bg-tealbrand h-full"
                                style={{ width: `${emp.attendanceRate}%` }}
                              />
                            </div>
                            <span className="text-[10px] font-semibold">{emp.attendanceRate}%</span>
                          </div>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <button
                            onClick={() => setSelectedEmployee(emp)}
                            className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 hover:border-tealbrand text-slate-600 hover:text-tealbrand text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                          >
                            <Eye className="w-3 h-3" />
                            <span>Slip</span>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 3: DEPARTMENT ALLOCATIONS */}
          {activeTab === 'breakdown' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
              <div>
                <h4 className="text-base font-bold text-navy-900 mb-2">Compensation Composition</h4>
                <p className="text-xs text-slate-500 mb-6">
                  Payroll distribution divided into core compensation classes according to polymorphic formulas.
                </p>
                <div className="space-y-4">
                  {departmentStats.map((item) => (
                    <div key={item.name} className="flex items-center justify-between p-3 rounded-xl bg-slate-50">
                      <div className="flex items-center gap-2.5">
                        <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                        <span className="text-xs font-bold text-navy-900">{item.name}</span>
                      </div>
                      <div className="text-right">
                        <div className="text-xs font-extrabold text-navy-900">{item.budget}</div>
                        <div className="text-[10px] text-slate-400">{item.count} staff members</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Donut Chart */}
              <div className="h-64 flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={departmentStats}
                      dataKey="count"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={85}
                      paddingAngle={4}
                    >
                      {departmentStats.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(val, name) => [`${val} Employees`, name]}
                      contentStyle={{ backgroundColor: '#17153D', borderRadius: '10px', color: '#fff', fontSize: '11px' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>

        {/* MODAL: ITEMISED PAYSLIP INSPECTION */}
        {selectedEmployee && (
          <div className="fixed inset-0 z-50 bg-navy-900/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-white animate-scale-up">
              <div className="flex items-start justify-between pb-4 border-b border-slate-100">
                <div>
                  <span className="text-[10px] font-bold text-tealbrand uppercase tracking-wider">
                    Official Salary Slip
                  </span>
                  <h3 className="text-xl font-extrabold text-navy-900 mt-0.5">
                    {selectedEmployee.name}
                  </h3>
                  <p className="text-xs text-slate-400">
                    ID: {selectedEmployee.id} • {selectedEmployee.role} ({selectedEmployee.department})
                  </p>
                </div>
                <button
                  onClick={() => setSelectedEmployee(null)}
                  className="w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200 flex items-center justify-center text-sm font-bold"
                >
                  ✕
                </button>
              </div>

              <div className="py-4 space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-slate-50">
                  <span className="text-slate-500">Employment Class</span>
                  <span className="font-bold text-navy-900">{selectedEmployee.type} Employee</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-50">
                  <span className="text-slate-500">Base Earnings</span>
                  <span className="font-bold text-navy-900">₹{selectedEmployee.basicSalary.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-50">
                  <span className="text-slate-500">Allowances (HRA + Med + Travel)</span>
                  <span className="font-bold text-emerald-600">+₹{selectedEmployee.allowances.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-50">
                  <span className="text-slate-500">Statutory Deductions (PF + TDS)</span>
                  <span className="font-bold text-rose-500">-₹{selectedEmployee.deductions.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between py-2 pt-3 border-t border-slate-200 text-sm">
                  <span className="font-extrabold text-navy-900">Net Take-Home Pay</span>
                  <span className="font-extrabold text-tealbrand text-base">
                    ₹{selectedEmployee.netSalary.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <span className="text-[11px] text-slate-400">Status: Disbursed via Direct Bank Transfer</span>
                <button
                  onClick={() => alert(`Downloaded PDF Payslip for ${selectedEmployee.name}`)}
                  className="px-4 py-2 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download PDF</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
