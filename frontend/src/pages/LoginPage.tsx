import React, { useState } from 'react';
import { Sparkles, Lock, Mail, Eye, EyeOff, ArrowRight, Shield } from 'lucide-react';

interface LoginPageProps {
  onLogin: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Please enter your email and password.');
      return;
    }
    setLoading(true);
    setTimeout(() => { setLoading(false); onLogin(); }, 900);
  };

  const handleDemo = () => {
    setEmail('demo@hiver.com');
    setPassword('spotify2024');
    setLoading(true);
    setTimeout(() => { setLoading(false); onLogin(); }, 700);
  };

  return (
    <div className="min-h-screen bg-[#F5EDE0] flex">
      {/* Left Brand Panel */}
      <div className="hidden lg:flex lg:w-[52%] bg-gradient-to-br from-[#E8DDCC] via-[#F0E6D6] to-[#DDD0BC] flex-col justify-between p-14 relative overflow-hidden">
        <div className="absolute -top-28 -left-28 w-[420px] h-[420px] rounded-full bg-[#C4B49A]/20" />
        <div className="absolute -bottom-36 -right-20 w-[340px] h-[340px] rounded-full bg-[#C4B49A]/15" />
        <div className="absolute top-1/2 left-1/3 w-72 h-72 rounded-full bg-[#F5EDE0]/50 blur-3xl" />

        <div className="relative z-10 flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-[#26231F] flex items-center justify-center shadow-lg">
            <Sparkles className="w-5 h-5 text-[#F5EDE0]" />
          </div>
          <span className="font-serif font-bold text-xl text-[#26231F] tracking-wide">
            Support Intelligence
          </span>
        </div>

        <div className="relative z-10 space-y-8">
          <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-[#FAF8F3]/70 border border-[#DDD5C8] text-xs font-semibold text-[#716A60] tracking-widest uppercase">
            <Shield className="w-3.5 h-3.5 text-[#A89B8A]" />
            Hiver SDE Intern Assignment
          </div>

          <h1 className="text-[2.75rem] leading-[1.15] font-bold font-serif text-[#26231F] tracking-tight">
            From noisy<br />conversations to<br />
            <span className="text-[#8B7D6B]">trustworthy</span> support<br />decisions.
          </h1>

          <p className="text-sm text-[#716A60] leading-[1.8] max-w-md tracking-wide">
            AI-powered customer support agent built on 43,000+ real Twitter interactions from SpotifyCares — classified, retrieved, grounded, and evaluated.
          </p>

          <div className="grid grid-cols-3 gap-5 pt-2">
            {[
              { label: 'Intent F1', value: '68.1%' },
              { label: 'Recall@5', value: '97.5%' },
              { label: 'Hallucination', value: '0.0%' },
            ].map((s) => (
              <div key={s.label} className="bg-[#FAF8F3]/80 backdrop-blur-sm rounded-2xl p-5 border border-[#DDD5C8] text-center space-y-1.5 shadow-sm">
                <div className="text-2xl font-bold font-serif text-[#26231F] tracking-tight">{s.value}</div>
                <div className="text-[11px] text-[#A89B8A] tracking-widest uppercase font-medium">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative z-10 text-[11px] text-[#A89B8A] tracking-widest font-medium">
          TWCS Benchmark  ·  Seed = 42  ·  SpotifyCares
        </div>
      </div>

      {/* Right Login Form */}
      <div className="w-full lg:w-[48%] flex items-center justify-center px-8 py-14 bg-[#FAF8F3]">
        <div className="w-full max-w-[420px] space-y-10">
          <div className="lg:hidden flex items-center gap-3 mb-4">
            <div className="w-9 h-9 rounded-xl bg-[#26231F] flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-[#F5EDE0]" />
            </div>
            <span className="font-serif font-bold text-lg text-[#26231F]">Support Intelligence</span>
          </div>

          <div className="space-y-3">
            <h2 className="text-3xl font-bold font-serif text-[#26231F] tracking-tight">
              Welcome back
            </h2>
            <p className="text-sm text-[#716A60] leading-relaxed tracking-wide">
              Sign in to access the AI support platform and benchmark dashboard.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2.5">
              <label className="text-[11px] font-bold text-[#26231F] tracking-[0.15em] uppercase block">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[#A89B8A]" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  className="w-full pl-11 pr-4 py-3.5 rounded-xl border border-[#DDD5C8] bg-white text-[#26231F] text-sm placeholder:text-[#A89B8A]/70 focus:outline-none focus:ring-2 focus:ring-[#C4B49A]/50 focus:border-[#A89B8A] transition-all tracking-wide"
                />
              </div>
            </div>

            <div className="space-y-2.5">
              <label className="text-[11px] font-bold text-[#26231F] tracking-[0.15em] uppercase block">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[#A89B8A]" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-11 pr-12 py-3.5 rounded-xl border border-[#DDD5C8] bg-white text-[#26231F] text-sm placeholder:text-[#A89B8A]/70 focus:outline-none focus:ring-2 focus:ring-[#C4B49A]/50 focus:border-[#A89B8A] transition-all tracking-wide"
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-[#A89B8A] hover:text-[#26231F] transition-colors">
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="text-xs text-red-700 bg-red-50 border border-red-200 rounded-xl px-4 py-3 tracking-wide">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-6 rounded-xl bg-[#26231F] text-[#FAF8F3] text-sm font-semibold tracking-widest flex items-center justify-center gap-2.5 hover:bg-black disabled:opacity-50 transition-all shadow-md"
            >
              {loading ? (
                <span className="flex items-center gap-2.5">
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                  Signing in...
                </span>
              ) : (
                <>
                  Sign In
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="flex items-center gap-4">
            <div className="flex-1 h-px bg-[#DDD5C8]" />
            <span className="text-[11px] text-[#A89B8A] tracking-[0.2em] uppercase font-medium">or</span>
            <div className="flex-1 h-px bg-[#DDD5C8]" />
          </div>

          <button
            onClick={handleDemo}
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-xl bg-[#E8DDCC] border border-[#DDD5C8] text-[#26231F] text-sm font-semibold tracking-wide hover:bg-[#DDD0BC] transition-all flex items-center justify-center gap-2.5 disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4 text-[#A89B8A]" />
            Continue with Demo Access
          </button>

          <p className="text-center text-[11px] text-[#A89B8A] leading-[1.8] tracking-wide">
            Demo credentials are pre-filled automatically.<br />
            Any valid email + password also works in demo mode.
          </p>
        </div>
      </div>
    </div>
  );
};
