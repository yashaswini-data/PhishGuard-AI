import React from 'react';
import { Shield, Code2, AlertOctagon } from 'lucide-react';

export default function Footer() {
  return (
    <footer style={{
      borderTop: '1px solid var(--border-subtle)',
      background: 'rgba(11, 15, 25, 0.95)',
      padding: '2.5rem 2rem 1.5rem',
      color: 'var(--text-dim)',
      fontSize: '0.85rem'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1.5rem',
          marginBottom: '1.75rem',
          borderBottom: '1px solid rgba(255, 255, 255, 0.06)',
          paddingBottom: '1.5rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              background: 'linear-gradient(135deg, #0284c7, #2563eb)',
              padding: '0.35rem',
              borderRadius: '8px'
            }}>
              <Shield size={20} color="#ffffff" />
            </div>
            <div>
              <span style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '1rem' }}>PhishGuard AI</span>
              <span style={{ marginLeft: '8px', fontSize: '0.75rem', background: 'rgba(56, 189, 248, 0.1)', color: 'var(--accent-cyan)', padding: '2px 8px', borderRadius: '4px' }}>
                Major Project Portfolio
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Code2 size={16} color="var(--accent-cyan)" />
              Built with React • FastAPI • Scikit-Learn
            </span>
          </div>
        </div>

        {/* Disclaimer Notice */}
        <div style={{
          background: 'rgba(245, 158, 11, 0.05)',
          border: '1px solid rgba(245, 158, 11, 0.15)',
          borderRadius: '8px',
          padding: '0.75rem 1rem',
          marginBottom: '1.25rem',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '0.65rem',
          color: '#fef3c7',
          fontSize: '0.8rem',
          lineHeight: 1.5
        }}>
          <AlertOctagon size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Cybersecurity Advisory & Operational Boundary:</strong> PhishGuard AI provides machine learning-driven risk classification based on mathematical and lexical URL features. A Legitimate assessment indicates absence of recognizable phishing patterns but does not guarantee the destination server is impervious or safe from zero-day exploits. Never execute untrusted files or share credentials without verification.
          </div>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
          <div>
            © {new Date().getFullYear()} PhishGuard AI – Intelligent Phishing Detection & Risk Analysis.
          </div>
          <div>
            Computer Science & Engineering Major Project Portfolio
          </div>
        </div>
      </div>
    </footer>
  );
}
