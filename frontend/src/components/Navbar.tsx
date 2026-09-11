import React from 'react';
import { 
  LayoutDashboard, 
  Bot, 
  Layers, 
  Search, 
  BarChart3, 
  AlertTriangle, 
  BookOpen 
} from 'lucide-react';

export type TabType = 
  | 'dashboard' 
  | 'agent' 
  | 'intents' 
  | 'retrieval' 
  | 'evaluation' 
  | 'failures' 
  | 'decisions';

interface NavbarProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard' as TabType, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'agent' as TabType, label: 'AI Support Agent', icon: Bot },
    { id: 'intents' as TabType, label: 'Intent Explorer', icon: Layers },
    { id: 'retrieval' as TabType, label: 'Evidence & Search', icon: Search },
    { id: 'evaluation' as TabType, label: 'Evaluation & Baselines', icon: BarChart3 },
    { id: 'failures' as TabType, label: 'Failure Analysis', icon: AlertTriangle },
    { id: 'decisions' as TabType, label: 'Decision Log', icon: BookOpen },
  ];

  return (
    <nav className="bg-[#F0E6D6] border-b border-[#DDD5C8] px-8">
      <div className="max-w-7xl mx-auto flex items-center gap-1.5 overflow-x-auto py-3 scrollbar-none">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-2.5 px-4 py-2.5 rounded-lg text-[13px] font-medium transition-all whitespace-nowrap tracking-wide ${
                isActive
                  ? 'bg-[#FAF8F3] text-[#26231F] shadow-sm border border-[#DDD5C8] font-semibold'
                  : 'text-[#716A60] hover:text-[#26231F] hover:bg-[#FAF8F3]/60'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-[#26231F]' : 'text-[#A89B8A]'}`} />
              {item.label}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
