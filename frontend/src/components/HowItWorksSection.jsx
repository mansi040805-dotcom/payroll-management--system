import React, { useState } from 'react';
import {
  UserPlus,
  CalendarCheck,
  Sliders,
  PlayCircle,
  FileCheck2,
  ArrowRight,
  Sparkles,
  Check
} from 'lucide-react';
import { howItWorksSteps } from '../data/mockData';

const stepIcons = [
  UserPlus,
  CalendarCheck,
  Sliders,
  PlayCircle,
  FileCheck2,
];

export default function HowItWorksSection() {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <section id="how-it-works" className="py-24 px-6 md:px-12 lg:px-16 bg-white relative overflow-hidden">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-mint-200/60 border border-mint-300 text-tealbrand text-xs font-bold uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            Seamless 5-Step Pipeline
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-navy-900 tracking-tight leading-tight">
            From Attendance to Payroll, Simplified.
          </h2>
          <p className="mt-3.5 text-base text-navy-800/70 font-normal leading-relaxed">
            A frictionless workflow taking your organization from daily punches to finalized bank disbursement in minutes.
          </p>
        </div>

        {/* Desktop Connected Horizontal Timeline */}
        <div className="relative mb-14 hidden lg:block">
          {/* Horizontal Connecting Line */}
          <div className="absolute top-1/2 left-8 right-8 -translate-y-1/2 h-1 bg-slate-100 -z-0">
            <div
              className="h-full bg-gradient-to-r from-tealbrand via-mint-300 to-accentpurple transition-all duration-500 rounded-full"
              style={{ width: `${(activeStep / (howItWorksSteps.length - 1)) * 100}%` }}
            />
          </div>

          <div className="grid grid-cols-5 gap-4 relative z-10">
            {howItWorksSteps.map((step, idx) => {
              const Icon = stepIcons[idx];
              const isPassed = idx <= activeStep;
              const isCurrent = idx === activeStep;

              return (
                <button
                  key={step.step}
                  onClick={() => setActiveStep(idx)}
                  className="flex flex-col items-center text-center group cursor-pointer focus:outline-none"
                >
                  {/* Step Bubble */}
                  <div
                    className={`w-14 h-14 rounded-2xl flex items-center justify-center font-bold text-sm transition-all duration-300 shadow-md ${
                      isCurrent
                        ? 'bg-tealbrand text-white scale-110 ring-4 ring-mint-200 shadow-tealbrand/20'
                        : isPassed
                        ? 'bg-white text-tealbrand border-2 border-tealbrand'
                        : 'bg-white text-slate-400 border border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    {isPassed && !isCurrent ? (
                      <Check className="w-5 h-5 stroke-[2.5]" />
                    ) : (
                      <Icon className="w-5 h-5" />
                    )}
                  </div>

                  <span className="mt-3 text-[11px] font-extrabold uppercase tracking-wider text-tealbrand">
                    Step {step.step}
                  </span>
                  <span className={`text-xs font-bold mt-0.5 line-clamp-1 transition-colors ${
                    isCurrent ? 'text-navy-900 font-extrabold' : 'text-slate-500 group-hover:text-navy-900'
                  }`}>
                    {step.title}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Detailed Active Step Focus Card */}
        <div className="bg-[#FAFDFD] rounded-[30px] p-8 lg:p-10 border border-slate-100 shadow-lg shadow-teal-900/5">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-7">
              <div className="flex items-center gap-2 mb-3">
                <span className="px-3 py-1 rounded-full bg-tealbrand text-white text-xs font-bold">
                  Step {howItWorksSteps[activeStep].step}
                </span>
                <span className="px-3 py-1 rounded-full bg-mint-100 text-tealbrand text-xs font-bold">
                  {howItWorksSteps[activeStep].badge}
                </span>
              </div>

              <h3 className="text-2xl sm:text-3xl font-extrabold text-navy-900 mb-2">
                {howItWorksSteps[activeStep].title}
              </h3>
              <p className="text-sm font-semibold text-slate-500 mb-4">
                {howItWorksSteps[activeStep].subtitle}
              </p>

              <p className="text-base text-navy-800/80 leading-relaxed mb-6">
                {howItWorksSteps[activeStep].description}
              </p>

              {/* Navigation controls */}
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setActiveStep((prev) => Math.max(prev - 1, 0))}
                  disabled={activeStep === 0}
                  className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  onClick={() => setActiveStep((prev) => Math.min(prev + 1, howItWorksSteps.length - 1))}
                  disabled={activeStep === howItWorksSteps.length - 1}
                  className="px-5 py-2 rounded-xl bg-navy-900 text-white text-xs font-bold hover:bg-navy-800 flex items-center gap-1.5 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <span>Next Step</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Visual preview card for current step */}
            <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
              <div className="text-xs font-mono text-slate-400 mb-3 flex items-center justify-between">
                <span>OOP Model Execution</span>
                <span className="text-tealbrand font-bold">Python Engine</span>
              </div>

              {activeStep === 0 && (
                <div className="space-y-2 text-xs font-mono bg-slate-50 p-4 rounded-xl text-navy-900">
                  <div className="text-tealbrand font-semibold"># Instantiating polymorphic object</div>
                  <div>emp = SalariedEmployee(</div>
                  <div className="pl-4">emp_id="EMP-1001",</div>
                  <div className="pl-4">name="Aarav Mehta",</div>
                  <div className="pl-4">basic_salary=145000</div>
                  <div>)</div>
                </div>
              )}

              {activeStep === 1 && (
                <div className="space-y-2 text-xs font-mono bg-slate-50 p-4 rounded-xl text-navy-900">
                  <div className="text-tealbrand font-semibold"># Attendance & Overtime Logs</div>
                  <div>logs = attendance_manager.get_monthly(emp_id)</div>
                  <div>work_days = logs.present_count  <span className="text-slate-400"># 22 days</span></div>
                  <div>leaves = leave_manager.approved_count <span className="text-slate-400"># 2 days</span></div>
                </div>
              )}

              {activeStep === 2 && (
                <div className="space-y-2 text-xs font-mono bg-slate-50 p-4 rounded-xl text-navy-900">
                  <div className="text-tealbrand font-semibold"># Compensation & Allowance Rules</div>
                  <div>comp.hra = basic * 0.40  <span className="text-slate-400"># ₹25,000</span></div>
                  <div>comp.medical = 4000</div>
                  <div>comp.transport = 5000</div>
                </div>
              )}

              {activeStep === 3 && (
                <div className="space-y-2 text-xs font-mono bg-slate-50 p-4 rounded-xl text-navy-900">
                  <div className="text-tealbrand font-semibold"># Polymorphic Calculation</div>
                  <div>gross = basic + allowances + bonus + overtime</div>
                  <div>net = gross - deductions</div>
                  <div>payroll_manager.finalize(cycle="2026-06")</div>
                </div>
              )}

              {activeStep === 4 && (
                <div className="space-y-2 text-xs font-mono bg-slate-50 p-4 rounded-xl text-navy-900">
                  <div className="text-tealbrand font-semibold"># Payslip Generation & Bank Log</div>
                  <div>slip = payslip_gen.generate_pdf(emp, payroll)</div>
                  <div>payment = Payment(ref="TXN-9842", status="PAID")</div>
                  <div className="text-emerald-600 font-bold">✓ Transaction Disbursed</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
