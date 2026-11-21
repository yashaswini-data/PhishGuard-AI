import React, { useState } from 'react';
import { ShieldCheck, Zap, Lock, Database, AlertCircle } from 'lucide-react';
import URLAnalyzer from '../components/URLAnalyzer';
import ResultCard from '../components/ResultCard';
import FeatureBreakdown from '../components/FeatureBreakdown';
import api from '../services/api';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (url) => {
    setLoading(true);
    setError(null);
    setResult(null);

    const response = await api.predictUrl(url);
    if (response.success) {
      setResult(response.data);
    } else {
      setError(response.error);
    }
    setLoading(false);
  };

  const scrollToFeatures = () => {
    const el = document.getElementById('feature-matrix');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      {/* Metrics Banner */}
      <div className="grid-cols-4" style={{ marginBottom: '2rem' }}>
        <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(56, 189, 248, 0.1)', padding: '0.75rem', borderRadius: '10px' }}>
            <Zap size={22} color="var(--accent-cyan)" />
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>30</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
              Engineered Features
            </div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '0.75rem', borderRadius: '10px' }}>
            <ShieldCheck size={22} color="#10b981" />
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>99.84%</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
              Test Accuracy
            </div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(147, 51, 234, 0.1)', padding: '0.75rem', borderRadius: '10px' }}>
            <Database size={22} color="#a855f7" />
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>11,055</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
              Verified Records
            </div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: '0.75rem', borderRadius: '10px' }}>
            <Lock size={22} color="#f59e0b" />
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>0 ms</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
              Zero Network Risk
            </div>
          </div>
        </div>
      </div>

      {/* Main URL Input Card */}
      <URLAnalyzer onAnalyze={handleAnalyze} loading={loading} />

      {/* Error Alert */}
      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '12px',
          padding: '1.25rem',
          marginBottom: '2rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          color: '#fca5a5'
        }}>
          <AlertCircle size={20} color="#ef4444" style={{ flexShrink: 0 }} />
          <div>
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {/* Results View */}
      {result && (
        <>
          <ResultCard result={result} onScrollToFeatures={scrollToFeatures} />
          <FeatureBreakdown categories={result.categories} features={result.features} />
        </>
      )}
    </div>
  );
}
