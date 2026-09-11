import React, { useEffect, useState } from 'react';
import { AlertTriangle, HelpCircle, ArrowRight, Lightbulb, Wrench } from 'lucide-react';
import { api } from '../services/api';
import { FailureMode } from '../types';

export const FailureAnalysisPage: React.FC = () => {
  const [failures, setFailures] = useState<FailureMode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getFailures()
      .then(setFailures)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-2">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-[#A89B8A]" />
          <h1 className="text-xl font-bold font-serif text-[#26231F] tracking-wide">Empirical Top-5 Failure Modes</h1>
        </div>
        <p className="text-[13px] text-[#716A60] max-w-3xl leading-relaxed tracking-wide">
          In accordance with strict technical honesty, these 5 failure patterns were extracted directly from errors observed during evaluation on the 200-scenario Golden Benchmark. Each entry documents the concrete example, root cause, and engineering fix.
        </p>
      </div>

      {/* Failure Mode Cards */}
      <div className="space-y-5">
        {failures.map((item) => (
          <div 
            key={item.rank}
            className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-4 hover:border-[#A89B8A]/60 transition-all"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#DDD5C8] pb-3">
              <div className="flex items-center gap-2.5">
                <span className="w-6 h-6 rounded-full bg-[#E8DDCC]/60 text-[#26231F] font-mono text-xs flex items-center justify-center font-bold">
                  {item.rank}
                </span>
                <h3 className="text-sm font-bold font-serif text-[#26231F] tracking-wide">{item.category}</h3>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#F5EDE0] border border-[#DDD5C8] text-[#716A60] tracking-wider">
                Empirical Evaluation Anomaly
              </span>
            </div>

            {/* Real Example Box */}
            <div className="p-3.5 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] text-[13px] space-y-1">
              <span className="text-[10px] font-semibold text-[#716A60] uppercase tracking-wider block">
                Observed Customer Query
              </span>
              <p className="text-[#26231F] italic font-sans font-medium tracking-wide">
                "{item.example_message}"
              </p>
            </div>

            {/* Expected vs Actual */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[13px]">
              <div className="p-3.5 rounded-lg bg-decision-auto-bg/40 border border-decision-auto/20 space-y-1">
                <span className="font-semibold text-decision-auto text-[11px] block tracking-wide">Expected Pipeline Behavior</span>
                <p className="text-[#26231F] text-[11px] leading-relaxed font-mono tracking-wide">
                  {item.expected_behavior}
                </p>
              </div>

              <div className="p-3.5 rounded-lg bg-decision-esc-bg/40 border border-decision-esc/20 space-y-1">
                <span className="font-semibold text-decision-esc text-[11px] block tracking-wide">Actual Measured Behavior</span>
                <p className="text-[#26231F] text-[11px] leading-relaxed font-mono tracking-wide">
                  {item.actual_behavior}
                </p>
              </div>
            </div>

            {/* Why Failed & Hypothesis & Fix */}
            <div className="space-y-3 pt-1 text-[13px] border-t border-[#DDD5C8]/60">
              <div className="space-y-1">
                <div className="flex items-center gap-1.5 font-semibold text-[#26231F] text-[11px] tracking-wide">
                  <HelpCircle className="w-3.5 h-3.5 text-[#A89B8A]" />
                  Root Cause Analysis
                </div>
                <p className="text-[#716A60] text-[13px] leading-relaxed pl-5 tracking-wide">
                  {item.why_failed}
                </p>
              </div>

              <div className="space-y-1">
                <div className="flex items-center gap-1.5 font-semibold text-[#26231F] text-[11px] tracking-wide">
                  <Lightbulb className="w-3.5 h-3.5 text-[#A89B8A]" />
                  Engineering Hypothesis
                </div>
                <p className="text-[#716A60] text-[13px] leading-relaxed pl-5 tracking-wide">
                  {item.hypothesis}
                </p>
              </div>

              <div className="space-y-1">
                <div className="flex items-center gap-1.5 font-semibold text-[#26231F] text-[11px] tracking-wide">
                  <Wrench className="w-3.5 h-3.5 text-[#A89B8A]" />
                  Recommended Fix
                </div>
                <p className="text-[#716A60] text-[13px] leading-relaxed pl-5 tracking-wide">
                  {item.potential_fix}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
