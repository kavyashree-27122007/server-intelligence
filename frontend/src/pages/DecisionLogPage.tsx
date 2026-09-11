import React, { useEffect, useState } from 'react';
import { BookOpen, Scale, ArrowRight, Lightbulb } from 'lucide-react';
import { api } from '../services/api';
import { DecisionEntry } from '../types';

export const DecisionLogPage: React.FC = () => {
  const [decisions, setDecisions] = useState<DecisionEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDecisions()
      .then(setDecisions)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-2">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-[#A89B8A]" />
          <h1 className="text-xl font-bold font-serif text-[#26231F] tracking-wide">Architectural & Engineering Decision Log</h1>
        </div>
        <p className="text-[13px] text-[#716A60] max-w-3xl leading-relaxed tracking-wide">
          A transparent record of 12 non-obvious engineering decisions and trade-offs made throughout the design and execution of the Support Intelligence pipeline.
        </p>
      </div>

      {/* Decision Cards Timeline */}
      <div className="space-y-4">
        {decisions.map((item, idx) => (
          <div 
            key={item.decision_id}
            className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-3 hover:border-[#A89B8A]/60 transition-all"
          >
            <div className="flex items-center justify-between border-b border-[#DDD5C8] pb-3">
              <div className="flex items-center gap-2.5">
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#E8DDCC]/50 text-[#26231F] border border-[#DDD5C8] tracking-wider">
                  {item.decision_id}
                </span>
                <h3 className="text-sm font-bold font-serif text-[#26231F] tracking-wide">{item.title}</h3>
              </div>
              <span className="text-[11px] font-mono text-[#716A60] tracking-wider">Step #{idx + 1}</span>
            </div>

            <div className="space-y-2 text-[13px]">
              <div>
                <span className="text-[10px] font-semibold text-[#716A60] uppercase tracking-wider block">Decision</span>
                <p className="text-[#26231F] font-medium leading-relaxed mt-0.5 tracking-wide">
                  {item.decision}
                </p>
              </div>

              <div>
                <span className="text-[10px] font-semibold text-[#716A60] uppercase tracking-wider block">Rationale ("Why")</span>
                <p className="text-[#716A60] leading-relaxed mt-0.5 tracking-wide">
                  {item.why}
                </p>
              </div>

              <div className="p-3.5 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] space-y-1">
                <span className="text-[10px] font-semibold text-[#26231F] uppercase tracking-wider flex items-center gap-1.5">
                  <Scale className="w-3 h-3 text-[#A89B8A]" />
                  Engineering Trade-Off
                </span>
                <p className="text-[#716A60] text-[13px] leading-relaxed tracking-wide">
                  {item.tradeoff}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
