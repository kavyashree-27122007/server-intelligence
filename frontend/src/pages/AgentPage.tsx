import React, { useState } from 'react';
import { 
  Send, 
  Sparkles, 
  CheckCircle, 
  AlertTriangle, 
  Search, 
  Layers, 
  ShieldAlert, 
  ArrowRight,
  Clock,
  ExternalLink,
  ChevronRight,
  RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { AnalysisResult, EvidenceItem } from '../types';

export const AgentPage: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeEvidenceModal, setActiveEvidenceModal] = useState<EvidenceItem | null>(null);

  const demoExamples = [
    {
      label: 'Playback Crash on iOS',
      query: 'Spotify keeps pausing every 30 seconds when I lock my phone screen on iPhone 8 iOS 11. Super annoying please fix!!',
      tag: 'Routine Bug',
    },
    {
      label: 'Double Billing Dispute',
      query: 'I was charged twice this month for Spotify Family plan: $14.99 on Oct 1 and again on Oct 3. Please refund the extra charge!',
      tag: 'Financial Risk',
    },
    {
      label: 'Hacked Account Emergency',
      query: 'Someone in Russia logged into my account and changed the email address. I am locked out completely!!',
      tag: 'Security Threat',
    },
    {
      label: 'Sonos Speaker Handoff',
      query: "Spotify Connect doesn't detect my Sonos speakers anymore after updating my router.",
      tag: 'Hardware Integration',
    },
    {
      label: 'Airplane Offline Mode',
      query: "Downloaded songs won't play offline on airplane mode. It says I must connect to the internet.",
      tag: 'Offline DRM',
    },
    {
      label: 'Litigation Threat',
      query: 'I will contact my attorney and sue your company for unauthorized recurring credit card charges!!',
      tag: 'Legal Hard Trigger',
    },
    {
      label: 'Accidental Playlist Deletion',
      query: 'All my playlists disappeared overnight! 5 years of curated music just gone. Please tell me you can restore them!',
      tag: 'Library Recovery',
    },
    {
      label: 'Family Address Verification',
      query: "My brother can't join my Family Plan. It keeps saying 'You must live at the same address'. We live in the same house!",
      tag: 'Plan Admin',
    },
    {
      label: 'Vague Outreach',
      query: 'help',
      tag: 'Severe Brevity',
    },
    {
      label: 'Student Discount Renewal',
      query: "How do I cancel my student discount subscription before next month's renewal?",
      tag: 'Subscription FAQ',
    }
  ];

  const handleAnalyze = async (textToAnalyze?: string) => {
    const text = (textToAnalyze || inputMessage).trim();
    if (!text) return;

    setLoading(true);
    setError(null);

    try {
      const data = await api.analyze(text);
      setResult(data);
      if (textToAnalyze) setInputMessage(textToAnalyze);
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Demo Selector Bar */}
      <div className="bg-[#FAF8F3] rounded-2xl p-6 border border-[#DDD5C8] shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-[#716A60]">
          <span className="font-semibold text-[#26231F] flex items-center gap-2 text-sm">
            <Sparkles className="w-4 h-4 text-[#A89B8A]" />
            Try Dataset-Derived Evaluation Examples:
          </span>
          <span className="text-xs font-mono text-[#A89B8A]">Click to auto-populate & run full pipeline</span>
        </div>
        
        <div className="flex flex-wrap gap-3 pt-1">
          {demoExamples.map((ex, idx) => (
            <button
              key={idx}
              onClick={() => handleAnalyze(ex.query)}
              disabled={loading}
              className="text-left px-4 py-2.5 rounded-xl bg-[#F5EDE0] hover:bg-[#E8DDCC]/60 border border-[#DDD5C8] text-xs transition-all flex items-center gap-3 text-[#26231F] group disabled:opacity-50 shadow-xs"
            >
              <span className="font-medium text-[13px]">{ex.label}</span>
              <span className="text-[11px] text-[#716A60] font-mono px-2 py-0.5 rounded-md bg-[#FAF8F3] border border-[#DDD5C8] group-hover:border-[#A89B8A]">
                {ex.tag}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main 3-Column Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Customer Input (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-[#FAF8F3] rounded-2xl p-6 border border-[#DDD5C8] shadow-sm space-y-5">
            <div className="border-b border-[#DDD5C8] pb-4 space-y-1">
              <h2 className="text-base font-bold font-serif text-[#26231F] tracking-wide">Customer Support Input</h2>
              <p className="text-xs text-[#716A60] tracking-wide">Enter real or synthetic customer support tweet</p>
            </div>

            <div className="space-y-4">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="e.g. My music keeps stopping every 20 seconds on iPhone iOS 11..."
                rows={6}
                className="w-full text-xs sm:text-sm p-4 rounded-xl bg-[#F5EDE0] border border-[#DDD5C8] focus:outline-none focus:border-[#26231F] focus:ring-2 focus:ring-[#C4B49A]/40 transition-all text-[#26231F] resize-none placeholder:text-[#A89B8A]/70 leading-relaxed font-sans"
              />

              <button
                onClick={() => handleAnalyze()}
                disabled={loading || !inputMessage.trim()}
                className="w-full py-3.5 px-5 rounded-xl bg-[#26231F] text-[#FAF8F3] text-xs sm:text-sm font-semibold hover:bg-black transition-all flex items-center justify-center gap-2.5 disabled:opacity-50 shadow-md tracking-wider"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    Processing Pipeline...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    Analyze & Ground Response
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="p-4 rounded-xl bg-[#FDF1EE] border border-[#9E4A3B]/30 text-[#9E4A3B] text-xs flex items-start gap-2.5">
                <AlertTriangle className="w-4.5 h-4.5 shrink-0 mt-0.5" />
                <span className="leading-relaxed">{error}</span>
              </div>
            )}
          </div>

          {/* Pipeline Stages Legend */}
          <div className="bg-[#FAF8F3]/80 rounded-2xl p-6 border border-[#DDD5C8] text-xs space-y-4">
            <div className="font-bold font-serif text-[#26231F] text-sm tracking-wide">Pipeline Architecture Stages</div>
            <div className="space-y-3.5 text-[#716A60] text-xs">
              <div className="flex items-center gap-3.5">
                <span className="w-6 h-6 rounded-full bg-[#E8DDCC] text-[#26231F] font-mono text-xs flex items-center justify-center font-bold shrink-0">1</span>
                <span className="tracking-wide">Calibrated Intent Classifier (9 intents)</span>
              </div>
              <div className="flex items-center gap-3.5">
                <span className="w-6 h-6 rounded-full bg-[#E8DDCC] text-[#26231F] font-mono text-xs flex items-center justify-center font-bold shrink-0">2</span>
                <span className="tracking-wide">Hybrid Vector Retrieval (top-5 precedents)</span>
              </div>
              <div className="flex items-center gap-3.5">
                <span className="w-6 h-6 rounded-full bg-[#E8DDCC] text-[#26231F] font-mono text-xs flex items-center justify-center font-bold shrink-0">3</span>
                <span className="tracking-wide">Evidence-Grounded Reply Synthesizer</span>
              </div>
              <div className="flex items-center gap-3.5">
                <span className="w-6 h-6 rounded-full bg-[#E8DDCC] text-[#26231F] font-mono text-xs flex items-center justify-center font-bold shrink-0">4</span>
                <span className="tracking-wide">Multi-Factor Risk Check & Escalation Gate</span>
              </div>
            </div>
          </div>
        </div>

        {/* Center Column: Pipeline Analysis & Response (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Pipeline Progression Tracker */}
              <div className="bg-[#FAF8F3] rounded-2xl p-6 border border-[#DDD5C8] shadow-sm space-y-4">
                <div className="flex items-center justify-between text-xs font-mono text-[#716A60] pb-4 border-b border-[#DDD5C8]">
                  <span>LATENCY: {result.latency_ms}ms</span>
                  <span>REQUEST ID: {result.request_id.slice(0, 8)}</span>
                </div>
                
                <div className="grid grid-cols-3 gap-3 pt-1 text-center">
                  <div className="p-3.5 rounded-xl bg-[#F5EDE0] border border-[#DDD5C8] space-y-1.5">
                    <span className="text-[11px] text-[#716A60] uppercase tracking-wider block font-semibold">Predicted Intent</span>
                    <span className="text-xs sm:text-sm font-bold text-[#26231F] truncate block">
                      {result.intent.name}
                    </span>
                    <span className="text-[11px] text-[#A89B8A] font-mono block">
                      {(result.intent.confidence * 100).toFixed(1)}% conf
                    </span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#F5EDE0] border border-[#DDD5C8] space-y-1.5">
                    <span className="text-[11px] text-[#716A60] uppercase tracking-wider block font-semibold">Evidence Match</span>
                    <span className="text-xs sm:text-sm font-bold text-[#26231F] block">
                      {result.evidence.length} Precedents
                    </span>
                    <span className="text-[11px] text-[#A89B8A] font-mono block">
                      Max Sim: {result.evidence.length > 0 ? (result.evidence[0].similarity * 100).toFixed(0) : 0}%
                    </span>
                  </div>

                  <div className={`p-3.5 rounded-xl border space-y-1.5 ${
                    result.decision === 'AUTO_HANDLE' 
                      ? 'bg-[#EAF3ED] border-[#3B6E52]/30 text-[#3B6E52]' 
                      : 'bg-[#FDF1EE] border-[#9E4A3B]/30 text-[#9E4A3B]'
                  }`}>
                    <span className="text-[11px] uppercase tracking-wider block font-semibold">Action</span>
                    <span className="text-xs sm:text-sm font-bold block">
                      {result.decision === 'AUTO_HANDLE' ? '✓ Auto-Handle' : '! Escalate'}
                    </span>
                    <span className="text-[11px] font-mono block">
                      {(result.decision_confidence * 100).toFixed(1)}% conf
                    </span>
                  </div>
                </div>
              </div>

              {/* Draft Response Card */}
              <div className="bg-[#FAF8F3] rounded-2xl p-6 border border-[#DDD5C8] shadow-sm space-y-5">
                <div className="flex items-center justify-between flex-wrap gap-3 pb-3 border-b border-[#DDD5C8]">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold font-serif text-[#26231F]">AI Grounded Draft</span>
                    <span className="text-[11px] px-3 py-1 rounded-md bg-[#E8DDCC]/70 border border-[#DDD5C8] text-[#26231F] font-semibold tracking-wide">
                      Grounded in TWCS Precedents
                    </span>
                  </div>
                  <span className="text-xs text-[#716A60] font-mono font-medium">
                    Match Strength: {result.evidence.length > 0 ? Math.round(result.evidence[0].similarity * 100) : 0}%
                  </span>
                </div>

                <div className="p-4 sm:p-5 rounded-xl bg-[#F5EDE0] border border-[#DDD5C8] text-xs sm:text-sm text-[#26231F] leading-relaxed font-sans font-normal italic">
                  "{result.draft_reply}"
                </div>

                {/* Evidence Strength Bar */}
                <div className="space-y-2 pt-1">
                  <div className="flex justify-between text-xs text-[#716A60]">
                    <span className="tracking-wide">Historical Precedent Similarity</span>
                    <span className="font-mono font-semibold">
                      {result.evidence.length > 0 ? Math.round(result.evidence[0].similarity * 100) : 0}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-[#F5EDE0] rounded-full overflow-hidden border border-[#DDD5C8]">
                    <div 
                      className="h-full bg-[#26231F] transition-all duration-500 rounded-full"
                      style={{ width: `${result.evidence.length > 0 ? result.evidence[0].similarity * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-[#E8DDCC]/30 border border-[#DDD5C8] text-xs text-[#716A60] space-y-1.5 leading-relaxed">
                  <div className="font-semibold text-[#26231F]">Why this response?</div>
                  <p>
                    {result.evidence.length > 0
                      ? `Synthesized directly from ${result.evidence.length} historically verified ${result.intent.name} resolutions in the Twitter support corpus.`
                      : 'No high-confidence historical resolution found. Standard safety guidance applied.'}
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-[#FAF8F3]/60 rounded-2xl p-14 border border-[#DDD5C8] border-dashed text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-[#E8DDCC]/60 text-[#A89B8A] flex items-center justify-center mx-auto">
                <Search className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold font-serif text-[#26231F]">No Analysis Active</h3>
              <p className="text-xs sm:text-sm text-[#716A60] max-w-sm mx-auto leading-relaxed">
                Type an inquiry on the left or select any sample dataset button to trace the full pipeline in real time.
              </p>
            </div>
          )}
        </div>

        {/* Right Column: Evidence Inspection & Audit Decision (3 Cols) */}
        <div className="lg:col-span-3 space-y-6">
          {result ? (
            <div className="space-y-6">
              {/* Escalation Audit Card */}
              <div className={`rounded-2xl p-6 border shadow-sm space-y-4 ${
                result.decision === 'AUTO_HANDLE'
                  ? 'bg-[#FAF8F3] border-[#DDD5C8]'
                  : 'bg-[#FDF1EE] border-[#9E4A3B]/30'
              }`}>
                <div className="flex items-center gap-2.5">
                  {result.decision === 'AUTO_HANDLE' ? (
                    <CheckCircle className="w-5 h-5 text-[#3B6E52]" />
                  ) : (
                    <ShieldAlert className="w-5 h-5 text-[#9E4A3B]" />
                  )}
                  <span className={`text-xs font-bold font-serif tracking-wider uppercase ${
                    result.decision === 'AUTO_HANDLE' ? 'text-[#3B6E52]' : 'text-[#9E4A3B]'
                  }`}>
                    {result.decision === 'AUTO_HANDLE' ? 'AUTO-HANDLE APPROVED' : 'ESCALATE TO HUMAN'}
                  </span>
                </div>

                <p className="text-xs text-[#716A60] leading-relaxed tracking-wide">
                  {result.reason}
                </p>

                {result.risk_factors.length > 0 && (
                  <div className="pt-3 border-t border-[#DDD5C8] space-y-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#716A60] block">
                      Active Risk Signals ({result.risk_factors.length})
                    </span>
                    <ul className="space-y-1.5">
                      {result.risk_factors.map((rf, i) => (
                        <li key={i} className="text-xs text-[#9E4A3B] flex items-start gap-2">
                          <span className="text-xs mt-0.5">•</span>
                          <span>{rf}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Historical Evidence Drawer */}
              <div className="bg-[#FAF8F3] rounded-2xl p-6 border border-[#DDD5C8] shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b border-[#DDD5C8] pb-3">
                  <span className="text-xs font-bold font-serif text-[#26231F] tracking-wide">
                    Historical Precedents ({result.evidence.length})
                  </span>
                  <span className="text-[11px] text-[#716A60] font-mono">TWCS Corpus</span>
                </div>

                <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
                  {result.evidence.map((item, idx) => (
                    <div 
                      key={idx}
                      onClick={() => setActiveEvidenceModal(item)}
                      className="p-3.5 rounded-xl bg-[#F5EDE0] hover:bg-[#E8DDCC]/50 border border-[#DDD5C8] transition-all cursor-pointer space-y-2 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] font-mono font-semibold text-[#716A60]">
                          #{item.conversation_id || idx + 1}
                        </span>
                        <span className="text-[11px] font-mono px-2 py-0.5 rounded-md bg-[#FAF8F3] border border-[#DDD5C8] font-bold text-[#26231F]">
                          {(item.similarity * 100).toFixed(0)}% match
                        </span>
                      </div>
                      <p className="text-xs text-[#26231F] line-clamp-2 leading-relaxed">
                        "{item.customer_message}"
                      </p>
                      <div className="flex items-center justify-between text-[11px] text-[#A89B8A] pt-1 font-medium">
                        <span>Brand response available</span>
                        <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-[#FAF8F3]/60 rounded-2xl p-8 border border-[#DDD5C8] border-dashed text-center text-xs text-[#716A60]">
              Evidence inspection drawer will appear here upon query execution.
            </div>
          )}
        </div>
      </div>

      {/* Evidence Detail Modal */}
      {activeEvidenceModal && (
        <div className="fixed inset-0 bg-[#26231F]/50 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-fadeIn">
          <div className="bg-[#FAF8F3] rounded-2xl max-w-lg w-full p-8 border border-[#DDD5C8] shadow-2xl space-y-5">
            <div className="flex items-center justify-between border-b border-[#DDD5C8] pb-4">
              <div>
                <h3 className="text-base font-bold font-serif text-[#26231F]">Historical Conversation Detail</h3>
                <span className="text-xs text-[#716A60] font-mono">ID #{activeEvidenceModal.conversation_id}</span>
              </div>
              <span className="text-xs px-3 py-1 rounded-lg bg-[#E8DDCC] font-mono font-bold text-[#26231F]">
                {(activeEvidenceModal.similarity * 100).toFixed(1)}% Match
              </span>
            </div>

            <div className="space-y-4 text-xs sm:text-sm">
              <div className="p-4 rounded-xl bg-[#F5EDE0] border border-[#DDD5C8] space-y-1.5">
                <span className="text-[11px] font-bold text-[#716A60] uppercase tracking-wider block">Historical Customer Asked</span>
                <p className="text-[#26231F] italic leading-relaxed">"{activeEvidenceModal.customer_message}"</p>
              </div>

              <div className="p-4 rounded-xl bg-[#E8DDCC]/30 border border-[#DDD5C8] space-y-1.5">
                <span className="text-[11px] font-bold text-[#716A60] uppercase tracking-wider block">SpotifyCares Historical Response</span>
                <p className="text-[#26231F] font-medium leading-relaxed">"{activeEvidenceModal.brand_response}"</p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setActiveEvidenceModal(null)}
                className="px-5 py-2.5 rounded-xl bg-[#26231F] text-[#FAF8F3] text-xs font-semibold hover:bg-black transition-all"
              >
                Close Inspection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
