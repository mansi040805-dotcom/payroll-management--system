import React from 'react';
import { Layers, ShieldCheck, ArrowUp } from 'lucide-react';

export default function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-navy-900 text-white pt-16 pb-12 px-6 md:px-12 lg:px-16 border-t border-slate-800">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-navy-800">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-tealbrand flex items-center justify-center p-1.5 shadow-sm">
                <svg viewBox="0 0 32 32" className="w-full h-full" fill="none">
                  <rect width="32" height="32" rx="8" fill="#168C87" />
                  <circle cx="11" cy="11" r="5" fill="#9DDFC0" />
                  <rect x="9" y="19" width="14" height="4.5" rx="2.2" fill="white" />
                  <circle cx="21" cy="11" r="3.5" fill="#8D72DF" />
                </svg>
              </div>
              <span className="font-extrabold text-xl tracking-tight text-white">
                PaySphere
              </span>
            </div>

            <p className="text-sm text-slate-300 max-w-sm leading-relaxed">
              "Payroll Management, Made Effortless." A modern, robust compensation engine engineered for precision, attendance tracking, and streamlined financial reconciliation.
            </p>

            <div className="flex items-center gap-2 text-xs text-mint-300 font-medium">
              <ShieldCheck className="w-4 h-4 text-tealbrand" />
              <span>Built with strict OOP Architecture & Polymorphic Models</span>
            </div>
          </div>

          {/* Column 1: Navigation */}
          <div>
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-4">
              Navigation
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-300">
              <li>
                <a href="#hero" className="hover:text-mint-300 transition-colors">Hero Overview</a>
              </li>
              <li>
                <a href="#features" className="hover:text-mint-300 transition-colors">Platform Features</a>
              </li>
              <li>
                <a href="#preview" className="hover:text-mint-300 transition-colors">Interactive Dashboard</a>
              </li>
              <li>
                <a href="#how-it-works" className="hover:text-mint-300 transition-colors">How It Works</a>
              </li>
              <li>
                <a href="#calculator" className="hover:text-mint-300 transition-colors">Salary Breakdown</a>
              </li>
            </ul>
          </div>

          {/* Column 2: System Capabilities */}
          <div>
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-4">
              Capabilities
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-300">
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Salaried Employees</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Hourly Employees</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Daily Attendance Punch</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Statutory Deductions (PF/Tax)</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">JSON Data Persistence</span>
              </li>
            </ul>
          </div>

          {/* Column 3: Application Ecosystem */}
          <div>
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-4">
              Ecosystem
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-300">
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Python Tkinter GUI</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Web Showcase Client</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Automated PDF Payslips</span>
              </li>
              <li>
                <span className="hover:text-mint-300 transition-colors cursor-default">Enterprise Audit Trail</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <p>© {new Date().getFullYear()} PaySphere Systems. All rights reserved.</p>

          <button
            onClick={scrollToTop}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-navy-800 hover:bg-tealbrand hover:text-white text-slate-300 transition-all text-xs font-bold"
          >
            <span>Back to Top</span>
            <ArrowUp className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </footer>
  );
}
