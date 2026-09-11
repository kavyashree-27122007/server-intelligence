import React, { useState } from 'react';
import { Header } from './components/Header';
import { Navbar, TabType } from './components/Navbar';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { AgentPage } from './pages/AgentPage';
import { IntentExplorerPage } from './pages/IntentExplorerPage';
import { EvidencePage } from './pages/EvidencePage';
import { EvaluationPage } from './pages/EvaluationPage';
import { FailureAnalysisPage } from './pages/FailureAnalysisPage';
import { DecisionLogPage } from './pages/DecisionLogPage';

export const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="min-h-screen bg-[#F5EDE0] text-[#26231F] flex flex-col selection:bg-[#E8DDCC] selection:text-[#26231F]">
      <Header onLogout={() => setIsLoggedIn(false)} />
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-8 py-10">
        {activeTab === 'dashboard' && <DashboardPage onNavigate={setActiveTab} />}
        {activeTab === 'agent' && <AgentPage />}
        {activeTab === 'intents' && <IntentExplorerPage />}
        {activeTab === 'retrieval' && <EvidencePage />}
        {activeTab === 'evaluation' && <EvaluationPage />}
        {activeTab === 'failures' && <FailureAnalysisPage />}
        {activeTab === 'decisions' && <DecisionLogPage />}
      </main>

      <footer className="border-t border-[#DDD5C8] py-8 bg-[#E8DDCC]/40 text-center text-xs text-[#A89B8A]">
        <div className="max-w-7xl mx-auto px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="font-serif tracking-wide">Support Intelligence Platform  ·  Hiver SDE Intern Assignment</span>
          <span className="font-mono text-[11px] tracking-wider">TWCS Benchmark  ·  Reproducible Random Seed = 42</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
