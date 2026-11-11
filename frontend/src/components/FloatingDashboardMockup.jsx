import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Users,
  CalendarCheck2,
  ClockAlert,
  Coins,
  Calculator,
  ReceiptText,
  CreditCard,
  FileBarChart2,
  Settings,
  Search,
  Bell,
  ChevronDown,
  Sparkles,
  TrendingUp,
  Activity,
  Flame,
  CheckCircle2,
  ExternalLink,
  ShieldCheck,
  UserCheck
} from 'lucide-react';

export default function FloatingDashboardMockup({ mouseX = 0, mouseY = 0, isInteractive = true }) {
  const [activeNav, setActiveNav] = useState('Dashboard');
  const [timeFilter, setTimeFilter] = useState('Monthly');
  const [hoveredBar, setHoveredBar] = useState(null);

  // Dynamic 3D tilt calculation based on mouse coordinates
  const tiltX = isInteractive ? Math.min(Math.max(mouseY * -7, -10), 10) + 7 : 7;
  const tiltY = isInteractive ? Math.min(Math.max(mouseX * 9, -16), 8) - 13.5 : -13.5;

  const barData = [
    { label: 'Jan', current: 68, avg: 45, val: '₹16.8L' },
    { label: 'Feb', current: 75, avg: 52, val: '₹17.2L' },
    { label: 'Mar', current: 48, avg: 38, val: '₹17.9L' },
    { label: 'Apr', current: 62, avg: 49, val: '₹18.1L' },
    { label: 'May', current: 78, avg: 58, val: '₹18.3L' },
    { label: 'Jun', current: 52, avg: 40, val: '₹18.4L' },
    { label: 'Jul', current: 65, avg: 50, val: '₹18.5L' },
  ];

  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard },
    { name: 'Employees', icon: Users },
    { name: 'Attendance', icon: CalendarCheck2 },
    { name: 'Leave Management', icon: ClockAlert },
    { name: 'Compensation', icon: Coins },
    { name: 'Payroll', icon: Calculator },
    { name: 'Payslips', icon: ReceiptText },
    { name: 'Payments', icon: CreditCard },
    { name: 'Reports', icon: FileBarChart2 },
    { name: 'Settings', icon: Settings },
  ];

  return (
    <div className="relative w-full perspective-mockup-container select-none">
      {/* Ambient decorative glow behind the floating window */}
      <div className="absolute -inset-4 bg-gradient-to-r from-mint-300/30 via-tealbrand/20 to-accentpurple/25 rounded-[36px] blur-2xl transform rotate-1 scale-95 opacity-80 pointer-events-none" />

      {/* Main 3D Tilted Window */}
      <div
        className="relative bg-white rounded-[26px] md:rounded-[30px] border border-white/90 shadow-[0_30px_70px_-15px_rgba(20,35,55,0.25),0_15px_30px_-10px_rgba(22,140,135,0.18)] overflow-hidden transition-transform duration-300 ease-out"
        style={{
          transform: `perspective(1400px) rotateY(${tiltY}deg) rotateX(${tiltX}deg) rotateZ(1.2deg)`,
          transformStyle: 'preserve-3d',
        }}
      >
        <div className="flex h-full min-h-[580px] lg:min-h-[640px] text-navy-900">
          {/* ================= SIDEBAR ================= */}
          <aside className="w-[185px] lg:w-[215px] bg-[#FAFDFD] border-r border-slate-100/90 p-4 lg:p-5 flex flex-col justify-between shrink-0">
            <div>
              {/* Brand Header */}
              <div className="flex items-center gap-2.5 pb-6 pt-1 px-1.5 border-b border-slate-100">
                <div className="w-8 h-8 rounded-lg bg-tealbrand flex items-center justify-center p-1.5 shadow-sm shadow-teal-900/20">
                  <svg viewBox="0 0 32 32" className="w-full h-full" fill="none">
                    <rect width="32" height="32" rx="8" fill="#168C87" />
                    <circle cx="11" cy="11" r="5" fill="#9DDFC0" />
                    <rect x="9" y="19" width="14" height="4.5" rx="2.2" fill="white" />
                    <circle cx="21" cy="11" r="3.5" fill="#8D72DF" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-extrabold text-sm tracking-tight text-navy-900 leading-none">PaySphere</h3>
                  <span className="text-[9px] font-medium text-slate-400">Enterprise Core</span>
                </div>
              </div>

              {/* Navigation Items */}
              <div className="mt-4 space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeNav === item.name;
                  return (
                    <button
                      key={item.name}
                      onClick={() => setActiveNav(item.name)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-[12px] font-semibold transition-all text-left ${
                        isActive
                          ? 'bg-mint-100/90 text-tealbrand font-bold shadow-xs'
                          : 'text-slate-500 hover:text-navy-900 hover:bg-slate-100/70'
                      }`}
                    >
                      <Icon className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-tealbrand' : 'text-slate-400'}`} />
                      <span className="truncate">{item.name}</span>
                      {isActive && (
                        <span className="ml-auto w-1.5 h-1.5 rounded-full bg-tealbrand"></span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Bottom Purple Gradient App Banner - Exactly as in the Reference Image */}
            <div className="mt-4 p-3.5 rounded-2xl bg-gradient-to-br from-[#6C4ECF] to-[#452EA7] text-white shadow-md shadow-indigo-950/20">
              <p className="text-[11px] font-semibold text-white/95 leading-tight mb-2.5">
                Try desktop app version
              </p>
              <button
                onClick={() => alert("PaySphere Python Desktop GUI is available in the root repository (gui.py). Run 'python gui.py' to launch it!")}
                className="w-full py-1.5 px-3 rounded-full bg-white text-accentpurple-deep hover:bg-mint-50 text-[11px] font-bold shadow-sm transition-all text-center block"
              >
                Download
              </button>
            </div>
          </aside>

          {/* ================= MAIN DASHBOARD BODY ================= */}
          <main className="flex-1 p-5 lg:p-6 bg-[#FFFFFF] flex flex-col justify-between overflow-hidden">
            {/* Top Header Bar */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 gap-4">
              {/* Search Bar matching reference pill shape */}
              <div className="relative w-64 lg:w-72">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search here"
                  readOnly
                  className="w-full pl-8 pr-3 py-1.5 bg-[#F4F7F8] rounded-full text-[11px] text-navy-800 placeholder:text-slate-400 focus:outline-none border border-transparent"
                />
              </div>

              {/* Right User Actions */}
              <div className="flex items-center gap-3">
                <button className="relative p-1.5 rounded-full hover:bg-slate-100 text-slate-500 transition-colors">
                  <Bell className="w-4 h-4 text-slate-500" />
                  <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-tealbrand ring-2 ring-white"></span>
                </button>
                <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-tealbrand to-mint-300 flex items-center justify-center text-white text-[10px] font-bold shadow-xs">
                    HR
                  </div>
                  <span className="text-[11px] font-bold text-navy-800 hidden sm:inline">Admin</span>
                </div>
              </div>
            </div>

            {/* Dashboard Title & Dropdown */}
            <div className="flex items-center justify-between mt-3 mb-2">
              <h2 className="text-base lg:text-lg font-bold text-navy-900 tracking-tight">
                Payroll Dashboard
              </h2>
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#F4F7F8] text-[11px] font-semibold text-slate-600 border border-slate-200/60 cursor-pointer hover:bg-slate-100 transition-colors">
                <span>Show by {timeFilter}</span>
                <ChevronDown className="w-3 h-3 text-slate-500" />
              </div>
            </div>

            {/* Top Activity Graph Section (Matching Reference Activity Section) */}
            <div className="bg-[#FAFDFD] rounded-2xl p-4 border border-slate-100/90 relative">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <span className="text-[12px] font-bold text-navy-900">Activity</span>
                  <span className="text-[10px] text-slate-400 ml-2">Monthly Payroll Expenditure</span>
                </div>

                {/* Right Stat Pills */}
                <div className="flex items-center gap-4 text-right">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-lg bg-mint-100 flex items-center justify-center text-tealbrand">
                      <Users className="w-3 h-3" />
                    </div>
                    <div className="text-left">
                      <div className="text-[11px] font-extrabold text-navy-900 leading-none">128</div>
                      <div className="text-[9px] text-tealbrand font-semibold">↗ 8.2% Active</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 pl-3 border-l border-slate-200">
                    <div className="w-6 h-6 rounded-lg bg-purple-50 flex items-center justify-center text-accentpurple">
                      <Coins className="w-3 h-3" />
                    </div>
                    <div className="text-left">
                      <div className="text-[11px] font-extrabold text-navy-900 leading-none">₹18.45L</div>
                      <div className="text-[9px] text-slate-400">Total Net Disbursed</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Bar Chart Visualization (Styled closely to the reference dual bars) */}
              <div className="h-28 flex items-end justify-between pt-2 px-2 gap-2">
                {barData.map((b, i) => (
                  <div
                    key={b.label}
                    className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group cursor-pointer"
                    onMouseEnter={() => setHoveredBar(i)}
                    onMouseLeave={() => setHoveredBar(null)}
                  >
                    {/* Hover tooltip */}
                    {hoveredBar === i && (
                      <div className="absolute -top-3 bg-navy-900 text-white text-[9px] py-0.5 px-2 rounded shadow-md pointer-events-none z-10">
                        {b.val}
                      </div>
                    )}
                    {/* Dual bar group */}
                    <div className="w-full max-w-[28px] flex items-end justify-center gap-1 h-20">
                      {/* Dark teal bar */}
                      <div
                        className="w-2.5 rounded-t-sm bg-tealbrand transition-all duration-300 group-hover:bg-[#116e6a]"
                        style={{ height: `${b.current}%` }}
                      />
                      {/* Mint/light grey background bar */}
                      <div
                        className="w-2.5 rounded-t-sm bg-[#E3EFEA] group-hover:bg-[#c9e8de] transition-colors"
                        style={{ height: `${b.avg}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-semibold text-slate-400 group-hover:text-navy-900">
                      {b.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Middle Section: 3 Information Cards (Heart Rate / Thermometer / Flame style metrics) */}
            <div className="grid grid-cols-3 gap-3 my-3">
              {/* Card 1: Attendance Rate with ECG pulse curve */}
              <div className="bg-[#FAFDFD] rounded-xl p-3 border border-slate-100 flex flex-col justify-between">
                <div className="flex items-center justify-between text-slate-400 text-[10px]">
                  <span className="flex items-center gap-1 font-semibold text-navy-800">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    Attendance Rate
                  </span>
                  <span>•••</span>
                </div>

                {/* Mini ECG curve SVG */}
                <div className="py-1">
                  <svg viewBox="0 0 100 24" className="w-full h-5 stroke-rose-500 fill-none" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M 0 14 L 20 14 L 30 4 L 40 22 L 50 10 L 60 16 L 75 14 L 100 14" />
                  </svg>
                </div>

                <div className="flex items-baseline gap-1">
                  <span className="text-base font-extrabold text-navy-900">94.8%</span>
                  <span className="text-[9px] text-slate-400 font-medium">Avg Month</span>
                </div>
              </div>

              {/* Card 2: Pending Approvals with Temperature/Gauge style */}
              <div className="bg-[#FAFDFD] rounded-xl p-3 border border-slate-100 flex flex-col justify-between">
                <div className="flex items-center justify-between text-slate-400 text-[10px]">
                  <span className="flex items-center gap-1 font-semibold text-navy-800">
                    <span className="w-1.5 h-1.5 rounded-full bg-tealbrand"></span>
                    Pending Pay
                  </span>
                  <span>•••</span>
                </div>

                <div className="flex items-center justify-between py-1 px-1">
                  <div className="w-7 h-7 rounded-full bg-mint-100/80 flex items-center justify-center text-tealbrand">
                    <Activity className="w-4 h-4" />
                  </div>
                  <div className="text-right">
                    <div className="text-base font-extrabold text-navy-900">12</div>
                    <div className="text-[9px] text-amber-600 font-semibold">Under Review</div>
                  </div>
                </div>

                <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                  <div className="bg-tealbrand h-full rounded-full" style={{ width: '85%' }}></div>
                </div>
              </div>

              {/* Card 3: Avg Net Compensation (Flame/Calories style in reference) */}
              <div className="bg-[#FAFDFD] rounded-xl p-3 border border-slate-100 flex flex-col justify-between">
                <div className="flex items-center justify-between text-slate-400 text-[10px]">
                  <span className="flex items-center gap-1 font-semibold text-navy-800">
                    <span className="w-1.5 h-1.5 rounded-full bg-accentpurple"></span>
                    Avg Salary
                  </span>
                  <span>•••</span>
                </div>

                <div className="flex items-center justify-between py-1">
                  <div className="w-7 h-7 rounded-full bg-purple-100/70 flex items-center justify-center text-accentpurple">
                    <Flame className="w-4 h-4 fill-accentpurple/40" />
                  </div>
                  <div className="text-right">
                    <div className="text-base font-extrabold text-navy-900">₹42.5k</div>
                    <div className="text-[9px] text-slate-400">per employee</div>
                  </div>
                </div>

                <div className="text-[9px] text-tealbrand font-medium">
                  100% Tax Compliant
                </div>
              </div>
            </div>

            {/* Bottom Banner Card (Matching Reference "Check your result blood donors in here !") */}
            <div className="bg-[#F8FBFA] rounded-2xl p-3 px-4 border border-slate-200/80 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-navy-900 text-mint-300 flex items-center justify-center shrink-0 shadow-sm">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-[11px] font-bold text-navy-900 leading-tight">
                    Check your payroll disbursement status here!
                  </h4>
                  <p className="text-[9px] text-slate-500">
                    See automated bank direct deposit records & download payslips
                  </p>
                </div>
              </div>

              <a
                href="#preview"
                className="px-3.5 py-1.5 rounded-xl bg-accentpurple hover:bg-accentpurple-deep text-white text-[11px] font-bold shadow-sm transition-all"
              >
                Check
              </a>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
