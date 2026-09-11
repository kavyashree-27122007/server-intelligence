import React from 'react';
import { ShieldCheck, Sparkles, LogOut } from 'lucide-react';

interface HeaderProps {
  onLogout?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  return (
    <header className="border-b border-[#DDD5C8] bg-[#E8DDCC]/50 backdrop-blur-sm sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-8 py-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#26231F] flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-[#F5EDE0]" />
            </div>
            <span className="text-xl font-bold tracking-wide text-[#26231F] font-serif">
              Support Intelligence
            </span>
            <span className="text-[11px] px-2.5 py-1 rounded-full bg-[#E8DDCC]/60 text-[#26231F] font-semibold border border-[#DDD5C8] flex items-center gap-1.5 tracking-wider">
              <ShieldCheck className="w-3 h-3 text-[#A89B8A]" />
              TWCS Benchmark
            </span>
          </div>
          <p className="text-xs text-[#A89B8A] mt-1.5 tracking-wide">
            Evidence-grounded AI for customer support  ·  Target Brand: <span className="font-semibold text-[#26231F]">SpotifyCares</span>
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <div className="text-xs font-semibold text-[#26231F] tracking-wide">Zero-Hallucination Pipeline</div>
            <div className="text-[11px] text-[#A89B8A] tracking-wider">Classify  ·  Retrieve  ·  Ground  ·  Escalate</div>
          </div>
          <div className="h-8 w-px bg-[#DDD5C8] hidden sm:block"></div>
          <span className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-[#FAF8F3] border border-[#DDD5C8] text-xs font-semibold text-[#26231F] shadow-sm tracking-wide">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            System Live
          </span>
          {onLogout && (
            <button
              onClick={onLogout}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#FAF8F3] border border-[#DDD5C8] text-xs font-medium text-[#716A60] hover:text-[#26231F] hover:bg-[#E8DDCC]/40 transition-all tracking-wide"
            >
              <LogOut className="w-3.5 h-3.5" />
              Sign Out
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
