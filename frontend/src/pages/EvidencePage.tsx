import React, { useState } from 'react';
import { Search, History, ArrowRight, CheckCircle2, ChevronRight, Layers } from 'lucide-react';
import { api } from '../services/api';
import { EvidenceItem } from '../types';

export const EvidencePage: React.FC = () => {
  const [query, setQuery] = useState('My playlist vanished after updating the app');
  const [results, setResults] = useState<EvidenceItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (overrideQuery?: string) => {
    const q = (overrideQuery || query).trim();
    if (!q) return;

    setLoading(true);
    try {
      const data = await api.retrieve(q, 5);
      setResults(data);
      setSearched(true);
      if (overrideQuery) setQuery(overrideQuery);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    'My playlist vanished after updating the app',
    'Charged twice on credit card this week',
    'Songs skipping midway on desktop Windows',
    'Cannot connect to Sonos via Spotify Connect',
    'How to cancel student discount subscription',
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Search Header */}
      <div className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-4">
        <div>
          <h1 className="text-xl font-bold font-serif text-[#26231F] tracking-wide">Historical Evidence Retrieval Explorer</h1>
          <p className="text-[13px] text-[#716A60] mt-1 tracking-wide leading-relaxed">
            Query the vector index (6,400 indexed training pairs from TWCS) to inspect how past brand resolutions are discovered and weighted.
          </p>
        </div>

        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-[#A89B8A] absolute left-3.5 top-3" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search historical support precedents..."
              className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] text-[13px] text-[#26231F] tracking-wide focus:outline-none focus:border-[#26231F] focus:ring-1 focus:ring-[#26231F]"
            />
          </div>
          <button
            onClick={() => handleSearch()}
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-[#26231F] text-[#FAF8F3] text-[13px] font-medium tracking-wide hover:bg-black transition-all flex items-center gap-1.5 shadow-sm disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Search Index'}
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-2 pt-1 text-[13px] text-[#716A60] tracking-wide">
          <span className="text-[11px] font-medium text-[#26231F] tracking-wide">Try search examples:</span>
          {sampleQueries.map((sq, i) => (
            <button
              key={i}
              onClick={() => handleSearch(sq)}
              className="px-2.5 py-1 rounded bg-[#F5EDE0] hover:bg-[#E8DDCC]/40 border border-[#DDD5C8] text-[11px] text-[#26231F] tracking-wide transition-colors"
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Results Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-[13px] text-[#716A60] tracking-wide">
          <span className="font-medium text-[#26231F] tracking-wide">
            {searched ? `Found ${results.length} Matching Historical Precedents` : 'Awaiting Query'}
          </span>
          <span className="font-mono text-[11px] tracking-wide">Index: 6,400 Train Pairs (Held-Out Eval)</span>
        </div>

        {results.length > 0 ? (
          <div className="space-y-3">
            {results.map((item, idx) => (
              <div 
                key={idx}
                className="bg-[#FAF8F3] rounded-2xl p-8 border border-[#DDD5C8] shadow-sm space-y-3 hover:border-[#A89B8A]/60 transition-all"
              >
                <div className="flex items-center justify-between border-b border-[#DDD5C8] pb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold font-mono px-2 py-0.5 rounded bg-[#F5EDE0] border border-[#DDD5C8] text-[#26231F] tracking-wide">
                      Rank #{idx + 1}
                    </span>
                    <span className="text-[13px] text-[#716A60] font-mono tracking-wide">
                      Conversation ID: #{item.conversation_id}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] text-[#716A60] tracking-wide">Cosine Match:</span>
                    <span className="text-[13px] font-mono font-bold px-2 py-0.5 rounded bg-[#E8DDCC]/50 text-[#26231F] border border-[#DDD5C8] tracking-wide">
                      {(item.similarity * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[13px] tracking-wide">
                  <div className="p-3.5 rounded-lg bg-[#F5EDE0] border border-[#DDD5C8] space-y-1">
                    <span className="text-[10px] font-semibold text-[#716A60] uppercase tracking-wider block">
                      Historical Customer Message
                    </span>
                    <p className="text-[#26231F] italic leading-relaxed tracking-wide">
                      "{item.customer_message}"
                    </p>
                  </div>

                  <div className="p-3.5 rounded-lg bg-[#E8DDCC]/20 border border-[#DDD5C8] space-y-1">
                    <span className="text-[10px] font-semibold text-[#716A60] uppercase tracking-wider block">
                      SpotifyCares Historical Resolution
                    </span>
                    <p className="text-[#26231F] font-medium leading-relaxed tracking-wide">
                      "{item.brand_response}"
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : searched ? (
          <div className="bg-[#FAF8F3] rounded-2xl p-12 border border-[#DDD5C8] text-center text-[13px] text-[#716A60] tracking-wide shadow-sm">
            No historical precedents found above similarity threshold for this query.
          </div>
        ) : (
          <div className="bg-[#FAF8F3] rounded-2xl p-12 border border-[#DDD5C8] text-center text-[13px] text-[#716A60] tracking-wide shadow-sm">
            Click any query example above or type a search to inspect matched evidence.
          </div>
        )}
      </div>
    </div>
  );
};
