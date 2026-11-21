import React, { useEffect, useState } from 'react';
import { Shield, ShieldAlert, CheckCircle2, Activity, Cpu, Info } from 'lucide-react';
import api from '../services/api';

export default function Navbar({ activeTab, setActiveTab }) {
  const [serverHealth, setServerHealth] = useState({ online: false, checking: true });

  useEffect(() => {
    async function checkBackend() {
      const res = await api.checkHealth();
      if (res.success && res.data.status === 'healthy') {
        setServerHealth({ online: true, checking: false });
      } else {
        setServerHealth({ online: false, checking: false });
      }
    }
    checkBackend();
    const timer = setInterval(checkBackend, 30000);
    return () => clearInterval(timer);
  }, []);

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <div style={{
          background: 'linear-gradient(135deg, #0284c7, #2563eb)',
          padding: '0.5rem',
          borderRadius: '10px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 16px rgba(56, 189, 248, 0.4)'
        }}>
          <Shield size={24} color="#ffffff" />
        </div>
        <div>
          <span style={{ fontWeight: 800, letterSpacing: '-0.03em' }}>PhishGuard</span>
          <span style={{ color: 'var(--accent-cyan)', fontWeight: 400, marginLeft: '4px' }}>AI</span>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: '-2px' }}>
            Risk Intelligence Engine
          </div>
        </div>
      </div>

      <ul className="nav-links">
        <li>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
            style={{ background: 'none', border: 'none' }}
          >
            Dashboard
          </button>
        </li>
        <li>
          <button
            onClick={() => setActiveTab('model')}
            className={`nav-link ${activeTab === 'model' ? 'active' : ''}`}
            style={{ background: 'none', border: 'none' }}
          >
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}>
              <Cpu size={16} /> Model Architecture
            </span>
          </button>
        </li>
        <li>
          <button
            onClick={() => setActiveTab('about')}
            className={`nav-link ${activeTab === 'about' ? 'active' : ''}`}
            style={{ background: 'none', border: 'none' }}
          >
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}>
              <Info size={16} /> Methodology & About
            </span>
          </button>
        </li>
      </ul>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div className={`badge ${serverHealth.online ? 'badge-safe' : 'badge-warning'}`}>
          <span style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: serverHealth.online ? '#10b981' : '#f59e0b',
            display: 'inline-block'
          }}></span>
          <span>{serverHealth.online ? 'API Online (Port 8000)' : 'API Degraded'}</span>
        </div>
      </div>
    </nav>
  );
}
