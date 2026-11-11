import React, { useState } from 'react';
import {
  Users,
  CalendarCheck2,
  ClockAlert,
  Calculator,
  Layers,
  ReceiptText,
  CreditCard,
  Coins,
  ArrowUpRight,
  Sparkles
} from 'lucide-react';
import { platformFeatures } from '../data/mockData';

const iconMap = {
  Users,
  CalendarCheck2,
  ClockAlert,
  Calculator,
  Layers,
  ReceiptText,
  CreditCard,
  Coins,
};

export default function FeaturesSection() {
  const [hoveredCard, setHoveredCard] = useState(null);

  return (
    <section id="features" className="py-24 px-6 md:px-12 lg:px-16 bg-[#F4F8F7] relative">
      {/* Subtle background decoration */}
      <div className="absolute top-0 inset-x-0 h-24 bg-gradient-to-b from-[#52C7C2]/15 to-transparent pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-mint-200/60 border border-mint-300 text-tealbrand text-xs font-bold uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            Core Capabilities
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-navy-900 tracking-tight leading-tight">
            Everything Your Payroll Needs.
          </h2>
          <p className="mt-3.5 text-base text-navy-800/70 font-normal leading-relaxed">
            Engineered with strict object-oriented principles, automated statutory rules, and crystal-clear audit trails.
          </p>
        </div>

        {/* 8 Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {platformFeatures.map((f) => {
            const Icon = iconMap[f.icon] || Layers;
            const isHovered = hoveredCard === f.id;

            return (
              <div
                key={f.id}
                onMouseEnter={() => setHoveredCard(f.id)}
                onMouseLeave={() => setHoveredCard(null)}
                className={`relative bg-white rounded-3xl p-6 border transition-all duration-300 flex flex-col justify-between group ${
                  isHovered
                    ? 'border-tealbrand/40 shadow-xl shadow-tealbrand/10 -translate-y-1.5'
                    : 'border-slate-100 shadow-sm hover:shadow-md'
                }`}
              >
                <div>
                  {/* Top Icon and Tag */}
                  <div className="flex items-center justify-between mb-5">
                    <div
                      className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                        isHovered
                          ? 'bg-tealbrand text-white shadow-md shadow-tealbrand/20 scale-105'
                          : 'bg-[#EBF7F4] text-tealbrand'
                      }`}
                    >
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 px-2.5 py-1 rounded-full border border-slate-100">
                      {f.tag}
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="text-lg font-bold text-navy-900 mb-2.5 group-hover:text-tealbrand transition-colors flex items-center justify-between">
                    <span>{f.title}</span>
                    <ArrowUpRight
                      className={`w-4 h-4 transition-transform duration-300 ${
                        isHovered ? 'translate-x-0.5 -translate-y-0.5 text-tealbrand' : 'opacity-0 text-slate-300'
                      }`}
                    />
                  </h3>

                  {/* Description */}
                  <p className="text-xs text-navy-700/70 leading-relaxed font-normal">
                    {f.desc}
                  </p>
                </div>

                {/* Bottom subtle accent bar */}
                <div className="mt-6 pt-4 border-t border-slate-100/80 flex items-center justify-between text-[11px] font-semibold text-slate-400 group-hover:text-tealbrand">
                  <span>Explore module</span>
                  <span className="text-xs font-bold">→</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
