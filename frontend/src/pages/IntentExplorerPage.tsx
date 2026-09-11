import React, { useEffect, useState } from 'react';
import { Layers, HelpCircle, CheckCircle, BarChart2 } from 'lucide-react';
import { api } from '../services/api';
import { IntentInfo } from '../types';

export const IntentExplorerPage: React.FC = () => {
  const [intents, setIntents] = useState<IntentInfo[]>([]);
  const [selectedIntent, setSelectedIntent] = useState<IntentInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getIntents()
      .then((data) => {
        setIntents(data.intents);
        if (data.intents.length > 0) setSelectedIntent(data.intents[0]);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header Overview */}
      <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-2">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-[#A89B8A]" />
          <h1 className="text-xl font-bold font-serif text-[#26231F] tracking-wide">Data-Discovered Intent Taxonomy</h1>
        </div>
        <p className="text-[13px] text-[#716A60] max-w-3xl leading-relaxed tracking-wide">
          Discovered empirically from historical Twitter support interactions for <span className="font-semibold text-[#26231F]">SpotifyCares</span>. Rather than adopting arbitrary generic categories (such as Banking77), these 9 intents capture real operational challenges: local audio buffer glitches, DRM licensing, SD card storage, and family plan address matching.
        </p>
      </div>

      {/* Main Taxonomy Grid & Detail View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Intent List Cards (5 Cols) */}
        <div className="lg:col-span-5 space-y-2.5">
          {intents.map((item) => {
            const isSelected = selectedIntent?.intent_id === item.intent_id;
            return (
              <div
                key={item.intent_id}
                onClick={() => setSelectedIntent(item)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer space-y-2 ${
                  isSelected
                    ? 'bg-[#FAF8F3] border-[#26231F] shadow-sm ring-1 ring-[#26231F]'
                    : 'bg-[#FAF8F3]/70 border-[#DDD5C8] hover:border-[#A89B8A]'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[13px] font-bold font-serif text-[#26231F] tracking-wide">{item.intent_name}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#F5EDE0] border border-[#DDD5C8] text-[#716A60] tracking-wider">
                    {item.support || 0} Golden Tests
                  </span>
                </div>
                <p className="text-[13px] text-[#716A60] line-clamp-2 tracking-wide">
                  {item.description}
                </p>
                <div className="flex items-center gap-4 text-[11px] font-mono pt-1 text-[#716A60] border-t border-[#DDD5C8]/40 tracking-wide">
                  <span>Prec: <strong className="text-[#26231F]">{item.precision ? (item.precision * 100).toFixed(0) : '—'}%</strong></span>
                  <span>Rec: <strong className="text-[#26231F]">{item.recall ? (item.recall * 100).toFixed(0) : '—'}%</strong></span>
                  <span>F1: <strong className="text-[#26231F]">{item.f1 ? (item.f1 * 100).toFixed(0) : '—'}%</strong></span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right Column: Deep Intent Inspector (7 Cols) */}
        <div className="lg:col-span-7">
          {selectedIntent ? (
            <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-6 sticky top-24">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-wider text-[#A89B8A] block">Taxonomy Specification</span>
                <h2 className="text-lg font-bold font-serif text-[#26231F] mt-0.5 tracking-wide">{selectedIntent.intent_name}</h2>
                <p className="text-[13px] text-[#716A60] mt-2 leading-relaxed tracking-wide">
                  {selectedIntent.description}
                </p>
              </div>

              {/* Evaluation Metrics Pill */}
              <div className="grid grid-cols-3 gap-3 p-3 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] text-center">
                <div>
                  <span className="text-[10px] text-[#716A60] uppercase block tracking-wider">Precision</span>
                  <span className="text-sm font-bold font-mono text-[#26231F] tracking-wide">
                    {selectedIntent.precision ? (selectedIntent.precision * 100).toFixed(1) : '—'}%
                  </span>
                </div>
                <div>
                  <span className="text-[10px] text-[#716A60] uppercase block tracking-wider">Recall</span>
                  <span className="text-sm font-bold font-mono text-[#26231F] tracking-wide">
                    {selectedIntent.recall ? (selectedIntent.recall * 100).toFixed(1) : '—'}%
                  </span>
                </div>
                <div>
                  <span className="text-[10px] text-[#716A60] uppercase block tracking-wider">Macro F1</span>
                  <span className="text-sm font-bold font-mono text-[#26231F] tracking-wide">
                    {selectedIntent.f1 ? (selectedIntent.f1 * 100).toFixed(1) : '—'}%
                  </span>
                </div>
              </div>

              {/* Inclusion vs Exclusion Criteria */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-[13px]">
                <div className="p-3.5 rounded-lg bg-decision-auto-bg/50 border border-decision-auto/20 space-y-1">
                  <span className="font-semibold text-decision-auto flex items-center gap-1 tracking-wide">
                    <CheckCircle className="w-3.5 h-3.5" />
                    Inclusion Criteria
                  </span>
                  <p className="text-[#716A60] text-[11px] leading-relaxed tracking-wide">
                    {selectedIntent.inclusion_criteria}
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-decision-esc-bg/50 border border-decision-esc/20 space-y-1">
                  <span className="font-semibold text-decision-esc flex items-center gap-1 tracking-wide">
                    <HelpCircle className="w-3.5 h-3.5" />
                    Exclusion Criteria
                  </span>
                  <p className="text-[#716A60] text-[11px] leading-relaxed tracking-wide">
                    {selectedIntent.exclusion_criteria}
                  </p>
                </div>
              </div>

              {/* Historical Support Examples */}
              <div className="space-y-2">
                <span className="text-[13px] font-bold font-serif text-[#26231F] block tracking-wide">
                  Ground Truth Dataset Examples
                </span>
                <div className="space-y-2">
                  {selectedIntent.examples.map((ex, i) => (
                    <div key={i} className="p-3 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] text-[13px] text-[#26231F] italic tracking-wide">
                      "{ex}"
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-[#716A60] text-[13px] tracking-wide">
              Select an intent to view full inclusion/exclusion specifications.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
