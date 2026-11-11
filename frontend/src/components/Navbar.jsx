import React, { useState } from 'react';
import { Layers, ArrowRight, Download, Menu, X, Sparkles, Terminal } from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="relative z-50 w-full pt-5 px-6 md:px-12 lg:px-16">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand Logo */}
        <a href="#workspace" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-white shadow-md shadow-teal-900/10 flex items-center justify-center p-2 transition-transform duration-300 group-hover:scale-105 border border-white/80">
            <svg viewBox="0 0 32 32" className="w-full h-full" fill="none">
              <rect x="2" y="2" width="28" height="28" rx="8" fill="#168C87" />
              <circle cx="11" cy="12" r="4.5" fill="#9DDFC0" />
              <rect x="10" y="19" width="13" height="4" rx="2" fill="white" />
              <circle cx="21" cy="12" r="3.5" fill="#8D72DF" />
            </svg>
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-2xl tracking-tight text-navy-900 flex items-center gap-1.5">
              PaySphere
              <span className="inline-block w-2 h-2 rounded-full bg-tealbrand animate-pulse"></span>
            </span>
            <span className="text-[11px] font-medium text-navy-600/80 -mt-1 tracking-wider uppercase">
              OOP Payroll System
            </span>
          </div>
        </a>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-1 bg-white/40 backdrop-blur-md px-5 py-2 rounded-full border border-white/60 shadow-sm text-sm font-semibold text-navy-800">
          <a
            href="#workspace"
            className="px-3.5 py-1.5 rounded-full bg-navy-900 text-white shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-mint-300" />
            <span>Interactive App</span>
          </a>
          <a
            href="#hero"
            className="px-3.5 py-1.5 rounded-full hover:bg-white/80 hover:text-tealbrand transition-all"
          >
            Showcase
          </a>
          <a
            href="#features"
            className="px-3.5 py-1.5 rounded-full hover:bg-white/80 hover:text-tealbrand transition-all"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            className="px-3.5 py-1.5 rounded-full hover:bg-white/80 hover:text-tealbrand transition-all"
          >
            How It Works
          </a>
          <a
            href="#calculator"
            className="px-3.5 py-1.5 rounded-full hover:bg-white/80 hover:text-tealbrand transition-all"
          >
            Salary Formula
          </a>
        </nav>

        {/* Right CTA */}
        <div className="hidden lg:flex items-center gap-3">
          <a
            href="#workspace"
            className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-navy-900 hover:bg-navy-800 text-white text-sm font-semibold shadow-md shadow-navy-900/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            <span>Launch Workspace</span>
            <ArrowRight className="w-4 h-4 text-mint-300" />
          </a>
        </div>

        {/* Mobile menu button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2.5 rounded-xl bg-white/70 text-navy-900 border border-white/80"
          aria-label="Toggle navigation menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-3 p-4 bg-white/95 backdrop-blur-xl rounded-2xl shadow-xl border border-white space-y-2">
          <a
            href="#workspace"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-bold text-tealbrand bg-mint-100"
          >
            Interactive Workspace
          </a>
          <a
            href="#hero"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-navy-800 hover:bg-mint-100"
          >
            Showcase
          </a>
          <a
            href="#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-navy-800 hover:bg-mint-100"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-navy-800 hover:bg-mint-100"
          >
            How It Works
          </a>
          <a
            href="#calculator"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-navy-800 hover:bg-mint-100"
          >
            Salary Formula
          </a>
          <div className="pt-2 border-t border-slate-100 flex flex-col gap-2">
            <a
              href="#workspace"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full text-center py-2.5 rounded-xl bg-navy-900 text-white text-sm font-semibold"
            >
              Launch Workspace
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
