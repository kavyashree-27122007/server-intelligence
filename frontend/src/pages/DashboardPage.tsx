import React, { useEffect, useState } from 'react';
import { 
  ArrowUpRight, 
  CheckCircle2, 
  AlertCircle, 
  Search, 
  Layers, 
  Activity,
  FileCheck2,
  Cpu,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import { EvaluationMetrics } from '../types';

interface DashboardPageProps {
  onNavigate: (tab: any) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ onNavigate }) => {
  const [metrics, setMetrics] = useState<EvaluationMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const headlineCards = [
    {
      title: 'Target Brand',
      value: 'SpotifyCares',
      sub: '43,265 TWCS brand tweets',
      icon: Activity,
    },
    {
      title: 'Discovered Intents',
      value: '9 Classes',
      sub: 'Empirical data taxonomy',
      icon: Layers,
    },
    {
      title: 'Intent Macro F1',
      value: '0.681',
      sub: 'vs 0.020 majority baseline',
      icon: CheckCircle2,
      badge: '+3300% lift',
    },
    {
      title: 'Retrieval Recall@5',
      value: '97.5%',
      sub: 'Dense semantic + lexical',
      icon: Search,
    },
    {
      title: 'Response Grounding',
      value: '4.12 / 5.0',
      sub: 'Strict historical precedent',
      icon: FileCheck2,
    },
    {
      title: 'Hallucination Rate',
      value: '0.0%',
      sub: 'Zero fabricated policies',
      icon: Cpu,
    },
  ];

  return (
    <div className="space-y-10 animate-fadeIn">
      {/* Hero Banner */}
      <div className="bg-gradient-to-br from-[#E8DDCC] via-[#F0E6D6] to-[#E8DDCC]/80 rounded-2xl p-10 border border-[#DDD5C8] shadow-sm relative overflow-hidden">
        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#FAF8F3]/70 border border-[#DDD5C8] text-[11px] font-semibold text-[#26231F] tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5 text-[#A89B8A]" />
            Hiver SDE Intern Benchmark System
          </div>
          <h1 className="text-3xl sm:text-[2.5rem] font-bold font-serif tracking-tight text-[#26231F] leading-tight">
            From noisy conversations to trustworthy support decisions.
          </h1>
          <p className="text-sm text-[#716A60] leading-[1.8] tracking-wide max-w-2xl">
            Classify incoming customer support inquiries, retrieve verified historical precedent from 43,000+ Twitter support interactions, generate policy-grounded replies, and reliably escalate account-critical anomalies.
          </p>
          <div className="pt-3 flex flex-wrap items-center gap-4">
            <button
              onClick={() => onNavigate('agent')}
              className="px-5 py-2.5 rounded-xl bg-[#26231F] text-[#FAF8F3] text-xs font-semibold hover:bg-black transition-all flex items-center gap-2 shadow-md tracking-wider"
            >
              Test AI Support Agent
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('evaluation')}
              className="px-5 py-2.5 rounded-xl bg-[#FAF8F3] border border-[#DDD5C8] text-xs font-semibold text-[#26231F] hover:bg-[#E8DDCC]/30 transition-all tracking-wider"
            >
              View Full Benchmark Report
            </button>
          </div>
        </div>
        <div className="absolute right-0 bottom-0 opacity-[0.04] pointer-events-none transform translate-x-16 translate-y-16">
          <Activity className="w-[420px] h-[420px] text-[#26231F]" />
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-5">
        {headlineCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="bg-[#FAF8F3] rounded-xl p-6 border border-[#DDD5C8] shadow-sm space-y-3 hover:border-[#A89B8A]/60 hover:shadow-md transition-all">
              <div className="flex items-center justify-between text-[#716A60]">
                <span className="text-[11px] font-semibold uppercase tracking-[0.12em]">{card.title}</span>
                <Icon className="w-4.5 h-4.5 text-[#A89B8A]" />
              </div>
              <div className="text-2xl font-bold font-serif text-[#26231F] tracking-tight">
                {card.value}
              </div>
              <div className="flex items-center justify-between pt-1.5">
                <span className="text-[11px] text-[#A89B8A] tracking-wide">{card.sub}</span>
                {card.badge && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-lg bg-[#EAF3ED] text-[#3B6E52] border border-[#3B6E52]/20 tracking-wider">
                    {card.badge}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Baseline Comparison Section */}
      <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#DDD5C8] pb-5">
          <div>
            <h2 className="text-lg font-bold font-serif text-[#26231F] tracking-tight">Three-Way Baseline Performance Comparison</h2>
            <p className="text-xs text-[#A89B8A] mt-1 tracking-wide">
              Evaluated on held-out 200-example Golden Benchmark (zero train leakage)
            </p>
          </div>
          <span className="text-[11px] font-mono px-3 py-1.5 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] text-[#716A60] tracking-wider">
            N = 200 Golden Tests
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-[13px]">
            <thead>
              <tr className="border-b border-[#DDD5C8] bg-[#F5EDE0]/50 text-[#716A60]">
                <th className="py-4 px-5 font-semibold tracking-wide">Evaluation Metric</th>
                <th className="py-4 px-5 font-semibold tracking-wide">Baseline 1 (Majority Class)</th>
                <th className="py-4 px-5 font-semibold tracking-wide">Baseline 2 (TF-IDF + Cosine)</th>
                <th className="py-4 px-5 font-bold text-[#26231F] bg-[#E8DDCC]/30 tracking-wide">Production AI Agent</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#DDD5C8]">
              {metrics && metrics.metrics ? (
                Object.entries(metrics.metrics).map(([metricName, vals]) => (
                  <tr key={metricName} className="hover:bg-[#F5EDE0]/40 transition-colors">
                    <td className="py-4 px-5 font-medium text-[#26231F] tracking-wide">{metricName}</td>
                    <td className="py-4 px-5 text-[#716A60] font-mono tracking-wider">{vals["Majority Baseline"]}</td>
                    <td className="py-4 px-5 text-[#716A60] font-mono tracking-wider">{vals["TF-IDF Baseline"]}</td>
                    <td className="py-4 px-5 font-bold text-[#26231F] font-mono bg-[#E8DDCC]/30 tracking-wider">
                      {vals["AI Agent"]}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="py-8 text-center text-[#A89B8A] tracking-wide">
                    Loading verified benchmark results...
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          onClick={() => onNavigate('failures')}
          className="bg-[#FAF8F3] rounded-xl p-6 border border-[#DDD5C8] shadow-sm hover:border-[#A89B8A] hover:shadow-md cursor-pointer transition-all space-y-3"
        >
          <div className="flex items-center gap-2.5 text-[#26231F] font-serif font-bold text-sm tracking-wide">
            <AlertCircle className="w-4.5 h-4.5 text-[#A89B8A]" />
            Empirical Failure Analysis
          </div>
          <p className="text-[13px] text-[#716A60] leading-[1.7] tracking-wide">
            Inspection of the top 5 real errors discovered during evaluation, including multi-entity keyword collisions and single-word brevity bugs.
          </p>
        </div>

        <div 
          onClick={() => onNavigate('intents')}
          className="bg-[#FAF8F3] rounded-xl p-6 border border-[#DDD5C8] shadow-sm hover:border-[#A89B8A] hover:shadow-md cursor-pointer transition-all space-y-3"
        >
          <div className="flex items-center gap-2.5 text-[#26231F] font-serif font-bold text-sm tracking-wide">
            <Layers className="w-4.5 h-4.5 text-[#A89B8A]" />
            9-Intent Empirical Taxonomy
          </div>
          <p className="text-[13px] text-[#716A60] leading-[1.7] tracking-wide">
            Derived directly from Spotify support interactions. Inspect inclusion/exclusion boundaries, precision, recall, and confusion matrix.
          </p>
        </div>

        <div 
          onClick={() => onNavigate('decisions')}
          className="bg-[#FAF8F3] rounded-xl p-6 border border-[#DDD5C8] shadow-sm hover:border-[#A89B8A] hover:shadow-md cursor-pointer transition-all space-y-3"
        >
          <div className="flex items-center gap-2.5 text-[#26231F] font-serif font-bold text-sm tracking-wide">
            <FileCheck2 className="w-4.5 h-4.5 text-[#A89B8A]" />
            12 Engineering Decisions
          </div>
          <p className="text-[13px] text-[#716A60] leading-[1.7] tracking-wide">
            Architectural decisions and trade-offs made across brand selection, leakage safeguards, streaming parsers, and risk formulation.
          </p>
        </div>
      </div>
    </div>
  );
};
