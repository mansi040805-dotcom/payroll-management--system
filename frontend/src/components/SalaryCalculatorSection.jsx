import React, { useState } from 'react';
import {
  Calculator,
  Sliders,
  DollarSign,
  PieChart as PieIcon,
  HelpCircle,
  Sparkles,
  ArrowRight,
  RotateCcw
} from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { salaryPresets } from '../data/mockData';

export default function SalaryCalculatorSection() {
  const [basic, setBasic] = useState(70000);
  const [hra, setHra] = useState(25000);
  const [transport, setTransport] = useState(6000);
  const [medical, setMedical] = useState(4000);
  const [otherAllowances, setOtherAllowances] = useState(5000);
  const [bonus, setBonus] = useState(10000);
  const [overtimeHours, setOvertimeHours] = useState(10);
  const [hourlyRate, setHourlyRate] = useState(500);
  const [taxDeductions, setTaxDeductions] = useState(12000);
  const [pfDeduction, setPfDeduction] = useState(8400);

  // Formulas
  const totalAllowances = hra + transport + medical + otherAllowances;
  const overtimePay = overtimeHours * hourlyRate;
  const grossSalary = basic + totalAllowances + bonus + overtimePay;
  const totalDeductions = taxDeductions + pfDeduction;
  const netSalary = Math.max(grossSalary - totalDeductions, 0);

  // Donut chart segments
  const chartData = [
    { name: 'Basic Salary', value: basic, color: '#168C87' },
    { name: 'Allowances (HRA/Med/Tr)', value: totalAllowances, color: '#77D4C7' },
    { name: 'Bonus & Overtime', value: bonus + overtimePay, color: '#FFB067' },
    { name: 'Deductions (PF/Tax)', value: totalDeductions, color: '#8D72DF' },
  ];

  const applyPreset = (presetKey) => {
    const p = salaryPresets[presetKey];
    if (!p) return;
    setBasic(p.basic);
    setHra(p.hra);
    setTransport(p.transport);
    setMedical(p.medical);
    setOtherAllowances(p.other);
    setBonus(p.bonus);
    setOvertimeHours(p.overtimeHours);
    setHourlyRate(p.hourlyOvertimeRate);
    setTaxDeductions(p.taxDeduction);
    setPfDeduction(p.pfDeduction);
  };

  return (
    <section id="calculator" className="py-24 px-6 md:px-12 lg:px-16 bg-[#F4F8F7] relative">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-14">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-mint-200/60 border border-mint-300 text-tealbrand text-xs font-bold uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            Transparent Mathematical Model
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-navy-900 tracking-tight leading-tight">
            Every Salary. Clearly Calculated.
          </h2>
          <p className="mt-3.5 text-base text-navy-800/70 font-normal leading-relaxed">
            Experience our dynamic compensation engine with full formula transparency and instant visual breakdown.
          </p>

          {/* Quick Presets */}
          <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
            <span className="text-xs font-bold text-slate-500 mr-1">Load Preset:</span>
            <button
              onClick={() => applyPreset('softwareEngineer')}
              className="px-3.5 py-1.5 rounded-full bg-white hover:bg-tealbrand hover:text-white text-navy-900 text-xs font-bold shadow-xs border border-slate-200 transition-all"
            >
              Senior Software Engineer
            </button>
            <button
              onClick={() => applyPreset('productDesigner')}
              className="px-3.5 py-1.5 rounded-full bg-white hover:bg-tealbrand hover:text-white text-navy-900 text-xs font-bold shadow-xs border border-slate-200 transition-all"
            >
              Product Designer
            </button>
            <button
              onClick={() => applyPreset('operationsAssociate')}
              className="px-3.5 py-1.5 rounded-full bg-white hover:bg-tealbrand hover:text-white text-navy-900 text-xs font-bold shadow-xs border border-slate-200 transition-all"
            >
              Operations Associate
            </button>
          </div>
        </div>

        {/* Main Interactive Calculator Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Interactive Inputs */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-sm space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h3 className="font-extrabold text-lg text-navy-900 flex items-center gap-2">
                <Sliders className="w-5 h-5 text-tealbrand" />
                <span>Salary Parameters</span>
              </h3>
              <span className="text-xs font-mono text-slate-400">Currency: INR (₹)</span>
            </div>

            {/* Basic Salary Slider */}
            <div>
              <div className="flex justify-between items-center text-xs font-bold text-navy-900 mb-1.5">
                <span>Basic Salary</span>
                <span className="text-sm font-extrabold text-tealbrand">₹{basic.toLocaleString('en-IN')}</span>
              </div>
              <input
                type="range"
                min="20000"
                max="250000"
                step="2000"
                value={basic}
                onChange={(e) => setBasic(Number(e.target.value))}
                className="w-full accent-tealbrand cursor-pointer h-2 bg-slate-100 rounded-lg"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>₹20,000</span>
                <span>Fixed Monthly Base</span>
                <span>₹2,50,000</span>
              </div>
            </div>

            {/* Allowances Group */}
            <div className="pt-2">
              <span className="text-xs font-extrabold uppercase tracking-wider text-slate-400 block mb-3">
                Monthly Allowances
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>HRA (House Rent)</span>
                    <span className="text-tealbrand">₹{hra.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="5000"
                    max="60000"
                    step="1000"
                    value={hra}
                    onChange={(e) => setHra(Number(e.target.value))}
                    className="w-full accent-tealbrand cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>

                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>Transport Allowance</span>
                    <span className="text-tealbrand">₹{transport.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="1000"
                    max="15000"
                    step="500"
                    value={transport}
                    onChange={(e) => setTransport(Number(e.target.value))}
                    className="w-full accent-tealbrand cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>

                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>Medical Allowance</span>
                    <span className="text-tealbrand">₹{medical.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="1000"
                    max="12000"
                    step="500"
                    value={medical}
                    onChange={(e) => setMedical(Number(e.target.value))}
                    className="w-full accent-tealbrand cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>

                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>Other Allowances</span>
                    <span className="text-tealbrand">₹{otherAllowances.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="20000"
                    step="500"
                    value={otherAllowances}
                    onChange={(e) => setOtherAllowances(Number(e.target.value))}
                    className="w-full accent-tealbrand cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>
              </div>
            </div>

            {/* Performance Bonus & Overtime */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                  <span>Performance Bonus</span>
                  <span className="text-amber-600">₹{bonus.toLocaleString('en-IN')}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="50000"
                  step="1000"
                  value={bonus}
                  onChange={(e) => setBonus(Number(e.target.value))}
                  className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-200 rounded"
                />
              </div>

              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
                <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                  <span>Overtime ({overtimeHours} hrs @ ₹{hourlyRate}/h)</span>
                  <span className="text-amber-600">₹{overtimePay.toLocaleString('en-IN')}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="2"
                  value={overtimeHours}
                  onChange={(e) => setOvertimeHours(Number(e.target.value))}
                  className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-200 rounded"
                />
              </div>
            </div>

            {/* Deductions Group */}
            <div className="pt-2">
              <span className="text-xs font-extrabold uppercase tracking-wider text-slate-400 block mb-3">
                Statutory Deductions
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-3.5 rounded-2xl bg-purple-50/60 border border-purple-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>Tax Deduction (TDS)</span>
                    <span className="text-accentpurple font-bold">₹{taxDeductions.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="40000"
                    step="500"
                    value={taxDeductions}
                    onChange={(e) => setTaxDeductions(Number(e.target.value))}
                    className="w-full accent-accentpurple cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>

                <div className="p-3.5 rounded-2xl bg-purple-50/60 border border-purple-100">
                  <div className="flex justify-between text-xs font-bold text-navy-900 mb-1">
                    <span>Provident Fund (PF)</span>
                    <span className="text-accentpurple font-bold">₹{pfDeduction.toLocaleString('en-IN')}</span>
                  </div>
                  <input
                    type="range"
                    min="1800"
                    max="20000"
                    step="200"
                    value={pfDeduction}
                    onChange={(e) => setPfDeduction(Number(e.target.value))}
                    className="w-full accent-accentpurple cursor-pointer h-1.5 bg-slate-200 rounded"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Visual Breakdown Card & Formulas */}
          <div className="lg:col-span-5 space-y-6">
            {/* Live Donut Summary Card */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-lg shadow-teal-900/5">
              <h3 className="font-extrabold text-lg text-navy-900 mb-1">
                Compensation Breakdown
              </h3>
              <p className="text-xs text-slate-400 mb-4">
                Visual proportional split of earnings vs deductions
              </p>

              {/* Donut Chart */}
              <div className="h-56 relative flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      innerRadius={65}
                      outerRadius={92}
                      paddingAngle={3}
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(val) => [`₹${val.toLocaleString('en-IN')}`, 'Amount']}
                      contentStyle={{ backgroundColor: '#17153D', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '11px' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
                {/* Center Net Pay Callout */}
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-[10px] uppercase font-bold text-slate-400">Take-Home</span>
                  <span className="text-lg font-black text-navy-900">
                    ₹{(netSalary / 1000).toFixed(1)}k
                  </span>
                  <span className="text-[9px] text-tealbrand font-bold">Net Salary</span>
                </div>
              </div>

              {/* Exact Formula Display as Requested in Requirements */}
              <div className="mt-4 p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-2.5">
                <div className="text-[11px] font-mono text-slate-500">
                  <span className="font-bold text-navy-900">Gross Salary Formula:</span><br />
                  <code className="text-tealbrand font-bold">
                    Gross = Basic ({basic.toLocaleString()}) + Allowances ({totalAllowances.toLocaleString()}) + Bonus ({bonus.toLocaleString()}) + Overtime ({overtimePay.toLocaleString()})
                  </code>
                  <div className="text-right font-extrabold text-navy-900 mt-0.5">
                    = ₹{grossSalary.toLocaleString('en-IN')}
                  </div>
                </div>

                <div className="h-px bg-slate-200" />

                <div className="text-[11px] font-mono text-slate-500">
                  <span className="font-bold text-navy-900">Net Salary Formula:</span><br />
                  <code className="text-accentpurple font-bold">
                    Net Salary = Gross Salary ({grossSalary.toLocaleString()}) - Deductions ({totalDeductions.toLocaleString()})
                  </code>
                  <div className="text-right font-black text-tealbrand text-sm mt-0.5">
                    = ₹{netSalary.toLocaleString('en-IN')}
                  </div>
                </div>
              </div>

              {/* Total Take-Home Hero Highlight */}
              <div className="mt-5 p-5 rounded-2xl bg-gradient-to-r from-mint-50 to-tealbrand/10 border border-tealbrand/20 flex items-center justify-between">
                <div>
                  <span className="text-[11px] font-extrabold uppercase tracking-wider text-tealbrand">
                    Calculated Monthly Net
                  </span>
                  <div className="text-3xl font-black text-navy-900 tracking-tight mt-0.5">
                    ₹{netSalary.toLocaleString('en-IN')}
                  </div>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-white shadow-md flex items-center justify-center text-tealbrand font-extrabold text-lg">
                  ₹
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
