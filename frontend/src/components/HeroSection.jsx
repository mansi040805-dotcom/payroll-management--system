import React, { useState } from 'react';
import {
  Sparkles,
  Layers,
  Users,
  Coins,
  TrendingUp,
  ArrowRight,
  ShieldAlert,
  CheckCircle2,
  SlidersHorizontal,
  Compass
} from 'lucide-react';
import FloatingDashboardMockup from './FloatingDashboardMockup';

export default function HeroSection() {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [activeIconTooltip, setActiveIconTooltip] = useState(null);

  const handleMouseMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5; // -0.5 to 0.5
    const y = (e.clientY - rect.top) / rect.height - 0.5; // -0.5 to 0.5
    setMousePos({ x, y });
  };

  const handleMouseLeave = () => {
    setMousePos({ x: 0, y: 0 });
  };

  return (
    <section
      id="hero"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className="relative min-h-[92vh] w-full overflow-hidden bg-mint-gradient pb-20 pt-8 lg:pt-14 px-6 md:px-12 lg:px-16 flex items-center"
    >
      {/* Decorative ambient background accents */}
      <div className="absolute top-10 left-1/4 w-96 h-96 bg-white/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-[500px] h-[500px] bg-tealbrand/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center relative z-10">
        {/* ================= LEFT COLUMN — TEXT AND FEATURES ================= */}
        <div className="lg:col-span-5 flex flex-col justify-center text-left">
          {/* Main Heading - following reference line breaks and bold dark-navy typography */}
          <h1 className="text-4xl sm:text-5xl lg:text-[58px] font-extrabold text-navy-900 tracking-[-0.03em] leading-[1.08] mb-5">
            Payroll &<br />
            Compensation<br />
            Management
          </h1>

          {/* Supporting Text */}
          <p className="text-base sm:text-lg text-navy-800/85 font-normal leading-relaxed max-w-lg mb-8">
            A smarter way to manage employees, automate salary calculations, track attendance, and simplify payroll operations.
          </p>

          {/* Large Translucent Feature Panel (Frosted Mint/White Rectangular Panel) */}
          <div className="frosted-panel rounded-[26px] p-5 sm:p-6 mb-8 max-w-md shadow-lg shadow-teal-900/5">
            <div className="flex flex-col gap-4">
              {/* Feature 1 */}
              <div className="flex items-center gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center p-2.5 shrink-0 transition-transform duration-300 group-hover:scale-110">
                  {/* Elegant sparkle / automation symbol */}
                  <div className="w-full h-full rounded-xl bg-gradient-to-tr from-[#FF7A59] to-[#FFB067] flex items-center justify-center text-white shadow-sm">
                    <Sparkles className="w-5 h-5 fill-white/30" />
                  </div>
                </div>
                <div>
                  <h3 className="text-base font-bold text-navy-900 group-hover:text-tealbrand transition-colors">
                    Smart Payroll Management
                  </h3>
                  <p className="text-xs text-navy-700/75 mt-0.5 font-medium">
                    Automated allowances, overtime & tax deductions
                  </p>
                </div>
              </div>

              {/* Subtle divider */}
              <div className="w-full h-px bg-white/60" />

              {/* Feature 2 */}
              <div className="flex items-center gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center p-2.5 shrink-0 transition-transform duration-300 group-hover:scale-110">
                  {/* Layered geometric symbol */}
                  <div className="w-full h-full rounded-xl bg-gradient-to-tr from-[#6C4ECF] to-[#8D72DF] flex items-center justify-center text-white shadow-sm">
                    <Layers className="w-5 h-5 fill-white/20" />
                  </div>
                </div>
                <div>
                  <h3 className="text-base font-bold text-navy-900 group-hover:text-accentpurple transition-colors">
                    Seamless Employee Management
                  </h3>
                  <p className="text-xs text-navy-700/75 mt-0.5 font-medium">
                    Salaried & hourly polymorphic architecture
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Three Large Circular/Squircle White Icon Containers (Matching Figma/Sketch/Xd in Reference) */}
          <div className="flex items-center gap-4 sm:gap-5">
            {/* Icon 1: Employee Management */}
            <div className="relative group">
              <button
                onMouseEnter={() => setActiveIconTooltip('Employee Management')}
                onMouseLeave={() => setActiveIconTooltip(null)}
                className="w-16 h-16 sm:w-[72px] sm:h-[72px] rounded-3xl bg-white shadow-squircle hover:shadow-xl transition-all duration-300 flex items-center justify-center p-4 hover:-translate-y-1 active:scale-95 border border-white"
                aria-label="Employee Management"
              >
                {/* Custom multi-color graphic badge */}
                <div className="w-full h-full rounded-2xl bg-gradient-to-br from-[#168C87] to-[#54C7C1] flex items-center justify-center text-white shadow-sm">
                  <Users className="w-6 h-6" />
                </div>
              </button>
              <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-navy-900 text-white text-[11px] font-semibold py-1 px-2.5 rounded-full whitespace-nowrap pointer-events-none shadow-md z-20">
                Employee Management
              </div>
            </div>

            {/* Icon 2: Salary & Compensation */}
            <div className="relative group">
              <button
                onMouseEnter={() => setActiveIconTooltip('Salary & Compensation')}
                onMouseLeave={() => setActiveIconTooltip(null)}
                className="w-16 h-16 sm:w-[72px] sm:h-[72px] rounded-3xl bg-white shadow-squircle hover:shadow-xl transition-all duration-300 flex items-center justify-center p-4 hover:-translate-y-1 active:scale-95 border border-white"
                aria-label="Salary & Compensation"
              >
                {/* Custom multi-color graphic badge */}
                <div className="w-full h-full rounded-2xl bg-gradient-to-br from-[#F59E0B] to-[#FBBF24] flex items-center justify-center text-white shadow-sm">
                  <Coins className="w-6 h-6" />
                </div>
              </button>
              <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-navy-900 text-white text-[11px] font-semibold py-1 px-2.5 rounded-full whitespace-nowrap pointer-events-none shadow-md z-20">
                Salary & Compensation
              </div>
            </div>

            {/* Icon 3: Payroll Analytics */}
            <div className="relative group">
              <button
                onMouseEnter={() => setActiveIconTooltip('Payroll Analytics')}
                onMouseLeave={() => setActiveIconTooltip(null)}
                className="w-16 h-16 sm:w-[72px] sm:h-[72px] rounded-3xl bg-white shadow-squircle hover:shadow-xl transition-all duration-300 flex items-center justify-center p-4 hover:-translate-y-1 active:scale-95 border border-white"
                aria-label="Payroll Analytics"
              >
                {/* Custom multi-color graphic badge */}
                <div className="w-full h-full rounded-2xl bg-gradient-to-br from-[#6C4ECF] to-[#8D72DF] flex items-center justify-center text-white shadow-sm">
                  <TrendingUp className="w-6 h-6" />
                </div>
              </button>
              <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-navy-900 text-white text-[11px] font-semibold py-1 px-2.5 rounded-full whitespace-nowrap pointer-events-none shadow-md z-20">
                Payroll Analytics
              </div>
            </div>

            {/* Subtle interactive indicator */}
            <div className="hidden sm:flex flex-col ml-2">
              <span className="text-[12px] font-bold text-navy-900 leading-tight">Interactive Showcase</span>
              <span className="text-[11px] text-navy-800/70">Move cursor to tilt 3D preview</span>
            </div>
          </div>
        </div>

        {/* ================= RIGHT COLUMN — LARGE FLOATING DASHBOARD ================= */}
        <div className="lg:col-span-7 w-full flex justify-end">
          <div className="w-full max-w-2xl lg:max-w-none lg:-mr-12 xl:-mr-16">
            <FloatingDashboardMockup
              mouseX={mousePos.x}
              mouseY={mousePos.y}
              isInteractive={true}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
