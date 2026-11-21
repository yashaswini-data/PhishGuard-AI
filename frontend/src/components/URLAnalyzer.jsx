import React, { useState } from 'react';
import { Search, Loader2, Sparkles, AlertCircle, Globe, Terminal } from 'lucide-react';

export default function URLAnalyzer({ onAnalyze, loading }) {
  const [inputUrl, setInputUrl] = useState('');
  const [validationError, setValidationError] = useState('');

  const samplePresets = [
    {
      label: 'Legitimate Domain',
      type: 'safe',
      url: 'https://www.google.com/search?q=machine+learning+cybersecurity'
    },
    {
      label: 'IP Obfuscated Attack',
      type: 'danger',
      url: 'http://188.128.111.33/iptv/login.php?update=verify&token=0x41'
    },
    {
      label: 'Credential Harvester',
      type: 'danger',
      url: 'http://secure-login.paypal.com.verify-account-update.xyz/login.php?token=admin'
    },
    {
      label: 'Deceptive Redirect',
      type: 'danger',
      url: 'http://att-verification-center.weeblysite.com/signin?ref=login.yahoo.com'
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = inputUrl.trim();
    if (!trimmed) {
      setValidationError('Please enter or paste a URL to analyze.');
      return;
    }
    setValidationError('');
    onAnalyze(trimmed);
  };

  const handlePresetSelect = (url) => {
    setInputUrl(url);
    setValidationError('');
    onAnalyze(url);
  };

  return (
    <div className="glass-card" style={{ padding: '2rem', marginBottom: '2rem' }}>
      <div style={{ textAlign: 'center', maxWidth: '720px', margin: '0 auto 1.75rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(56, 189, 248, 0.1)',
          color: 'var(--accent-cyan)',
          padding: '0.35rem 0.85rem',
          borderRadius: '9999px',
          fontSize: '0.8rem',
          fontWeight: 600,
          marginBottom: '1rem',
          border: '1px solid rgba(56, 189, 248, 0.2)'
        }}>
          <Sparkles size={14} /> Random Forest ML Risk Classification (99.8% Test Accuracy)
        </div>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.2, marginBottom: '0.75rem' }}>
          Real-Time Phishing Threat Detection
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1rem', lineHeight: 1.6 }}>
          Submit any suspicious link for instant heuristic analysis. PhishGuard AI evaluates 30 structural,
          domain, lexical, and statistical characteristics completely offline without visiting untrusted servers.
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{ maxWidth: '820px', margin: '0 auto' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          background: '#090d16',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          borderRadius: '12px',
          padding: '0.5rem 0.75rem',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
          position: 'relative'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0 0.75rem',
            color: 'var(--accent-cyan)',
            borderRight: '1px solid rgba(255, 255, 255, 0.1)',
            fontWeight: 600,
            fontSize: '0.85rem'
          }}>
            <Globe size={18} />
            <span>URL</span>
          </div>

          <input
            type="text"
            value={inputUrl}
            onChange={(e) => {
              setInputUrl(e.target.value);
              if (validationError) setValidationError('');
            }}
            placeholder="Paste or enter URL (e.g., https://example.com/account/login)..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-main)',
              fontSize: '1rem',
              padding: '0.75rem 1rem',
              fontFamily: 'inherit'
            }}
            disabled={loading}
          />

          {inputUrl && (
            <button
              type="button"
              onClick={() => setInputUrl('')}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-dim)',
                cursor: 'pointer',
                marginRight: '0.5rem',
                fontSize: '0.85rem'
              }}
            >
              Clear
            </button>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !inputUrl.trim()}
            style={{ padding: '0.75rem 1.75rem', borderRadius: '8px' }}
          >
            {loading ? (
              <>
                <Loader2 size={18} className="spinner" />
                <span>Extracting Features...</span>
              </>
            ) : (
              <>
                <Search size={18} />
                <span>Analyze Risk</span>
              </>
            )}
          </button>
        </div>

        {validationError && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            color: 'var(--status-danger)',
            fontSize: '0.85rem',
            marginTop: '0.75rem',
            paddingLeft: '0.5rem'
          }}>
            <AlertCircle size={16} />
            <span>{validationError}</span>
          </div>
        )}

        {/* Quick Test Presets */}
        <div style={{ marginTop: '1.25rem' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
            Quick Sample Test Inputs:
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {samplePresets.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handlePresetSelect(preset.url)}
                disabled={loading}
                style={{
                  background: preset.type === 'safe' ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.08)',
                  border: `1px solid ${preset.type === 'safe' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.25)'}`,
                  color: preset.type === 'safe' ? 'var(--status-safe)' : 'var(--status-danger)',
                  padding: '0.35rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 500,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.35rem',
                  transition: 'all 0.15s'
                }}
              >
                <span>{preset.label}</span>
              </button>
            ))}
          </div>
        </div>
      </form>
    </div>
  );
}
