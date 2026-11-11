import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import InteractiveWorkspace from './components/InteractiveWorkspace';
import FeaturesSection from './components/FeaturesSection';
import HowItWorksSection from './components/HowItWorksSection';
import SalaryCalculatorSection from './components/SalaryCalculatorSection';
import Footer from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-[#F6FAF8] text-navy-900 selection:bg-mint-300 selection:text-navy-900 antialiased overflow-x-hidden">
      {/* Top Navbar overlapping the mint hero gradient */}
      <div className="bg-mint-gradient">
        <Navbar />
      </div>

      <main className="flex-1">
        {/* HERO SECTION — Dribbble / Reference UI Showcase */}
        <HeroSection />

        {/* PRIMARY FUNCTIONAL WORKSPACE — All 8 modules connected to Python OOP backend */}
        <InteractiveWorkspace />

        {/* SECTION A — Platform Features */}
        <FeaturesSection />

        {/* SECTION B — How It Works Timeline */}
        <HowItWorksSection />

        {/* SECTION C — Salary Breakdown & Formula Calculator */}
        <SalaryCalculatorSection />
      </main>

      {/* FOOTER */}
      <Footer />
    </div>
  );
}
