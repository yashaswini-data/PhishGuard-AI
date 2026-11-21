import React, { useState } from 'react';
import { Layers, Check, AlertCircle, Info, Shield, Filter } from 'lucide-react';

const FEATURE_DESCRIPTIONS = {
  url_length: 'Total character length of the complete URL string.',
  hostname_length: 'Character count of the domain / netloc portion.',
  path_length: 'Length of the path following domain name.',
  count_dots: 'Total number of dot (.) characters in the entire URL.',
  count_subdomains: 'Number of subdomain levels preceding the primary domain.',
  count_directories: 'Directory depth determined by slash (/) characters in the path.',
  count_params: 'Count of distinct query string parameters.',
  has_fragment: 'Presence of URL fragment (#) anchor identifier.',
  has_ip_address: 'Direct IPv4/IPv6 address used in place of domain name.',
  has_at_symbol: 'Presence of @ symbol, which causes browsers to ignore preceding text.',
  is_shortened: 'Use of URL shortening redirection service (e.g. bit.ly, tinyurl).',
  count_suspicious_words: 'Occurrences of sensitive credential/banking target keywords.',
  count_hyphens: 'Count of hyphen (-) characters, often used in brand typo-squatting.',
  has_double_slash_redirect: 'Double slash (//) redirect evasion pattern in the path.',
  has_consecutive_dots: 'Consecutive dots (..) indicating path traversal or malformed host.',
  is_https: 'Encrypted HTTPS protocol usage vs unencrypted HTTP.',
  has_suspicious_port: 'Non-standard network port explicitly specified in the URL.',
  has_numeric_hostname: 'Presence of numeric digits within the domain hostname.',
  count_digits_hostname: 'Total quantity of numeric digits in the hostname.',
  has_hyphen_in_domain: 'Hyphen separator inside the hostname string.',
  count_tld_in_subdomain: 'Deceptive Top-Level Domain embedded inside a subdomain.',
  has_non_ascii: 'Punycode (xn--) or non-ASCII characters (IDN homograph attack).',
  has_hex_chars: 'Presence of hexadecimal encodings (0x... or %XX).',
  count_encoded_chars: 'Count of percent (%) encoded characters.',
  has_query_string: 'Presence of query parameters appended with question mark (?).',
  count_special_chars: 'Tilde, semicolon, dollar, and other unusual symbols in URL.',
  has_suspicious_extension: 'Executable or script file extension (.exe, .php, .scr, etc.).',
  digit_ratio: 'Proportion of numeric digits to total URL characters.',
  char_entropy: 'Shannon information entropy measuring character randomness.',
  ratio_digits_to_letters: 'Ratio of numeric digits to alphabetic characters.'
};

export default function FeatureBreakdown({ categories, features }) {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  if (!categories || !features) return null;

  const categoryNames = ['All', ...Object.keys(categories)];

  // Helper to determine if a value is suspicious
  const isFeatureSuspicious = (name, val) => {
    if (name === 'is_https' && val === 0) return true;
    if (name === 'is_https' && val === 1) return false;
    if (name === 'has_ip_address' && val === 1) return true;
    if (name === 'has_at_symbol' && val === 1) return true;
    if (name === 'is_shortened' && val === 1) return true;
    if (name === 'has_double_slash_redirect' && val === 1) return true;
    if (name === 'has_consecutive_dots' && val === 1) return true;
    if (name === 'has_suspicious_port' && val === 1) return true;
    if (name === 'count_tld_in_subdomain' && val === 1) return true;
    if (name === 'has_non_ascii' && val === 1) return true;
    if (name === 'has_suspicious_extension' && val === 1) return true;
    if (name === 'count_suspicious_words' && val > 0) return true;
    if (name === 'count_hyphens' && val >= 3) return true;
    if (name === 'url_length' && val > 75) return true;
    if (name === 'count_dots' && val >= 4) return true;
    if (name === 'count_subdomains' && val >= 2) return true;
    return false;
  };

  // Format value display
  const formatValue = (name, val) => {
    if (typeof val === 'number' && !Number.isInteger(val)) {
      return val.toFixed(4);
    }
    if (name.startsWith('has_') || name.startsWith('is_')) {
      return val === 1 ? '1 (Yes)' : '0 (No)';
    }
    return String(val);
  };

  // Filter features
  const allFeaturesList = [];
  Object.entries(categories).forEach(([catName, catFeats]) => {
    Object.entries(catFeats).forEach(([featName, featVal]) => {
      allFeaturesList.push({
        category: catName,
        name: featName,
        value: featVal,
        description: FEATURE_DESCRIPTIONS[featName] || 'Engineered URL characteristic.',
        suspicious: isFeatureSuspicious(featName, featVal)
      });
    });
  });

  const filteredFeatures = allFeaturesList.filter((item) => {
    const matchesCat = selectedCategory === 'All' || item.category === selectedCategory;
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div id="feature-matrix" className="glass-card" style={{ padding: '2rem', marginBottom: '2rem' }}>
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '1rem',
        marginBottom: '1.5rem',
        borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
        paddingBottom: '1rem'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Layers size={22} color="var(--accent-cyan)" />
            <h2 style={{ fontSize: '1.4rem', fontWeight: 700 }}>
              Engineered Feature Matrix (30 Features)
            </h2>
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
            Full breakdown of lexical, structural, and statistical characteristics passed into the Random Forest model.
          </p>
        </div>

        {/* Search */}
        <input
          type="text"
          placeholder="Filter features..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '8px',
            padding: '0.45rem 0.85rem',
            color: 'var(--text-main)',
            fontSize: '0.85rem',
            outline: 'none',
            minWidth: '220px'
          }}
        />
      </div>

      {/* Category Pills */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.5rem' }}>
        {categoryNames.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              background: selectedCategory === cat ? 'rgba(56, 189, 248, 0.2)' : 'rgba(255, 255, 255, 0.04)',
              border: `1px solid ${selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
              color: selectedCategory === cat ? 'var(--accent-cyan)' : 'var(--text-muted)',
              padding: '0.4rem 0.85rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'all 0.15s'
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Feature Grid */}
      <div className="grid-cols-2" style={{ gap: '1rem' }}>
        {filteredFeatures.map((item) => (
          <div
            key={item.name}
            style={{
              background: item.suspicious ? 'rgba(239, 68, 68, 0.04)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${item.suspicious ? 'rgba(239, 68, 68, 0.25)' : 'var(--border-subtle)'}`,
              borderRadius: '10px',
              padding: '1rem',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              transition: 'all 0.2s'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <div>
                <div style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.9rem',
                  fontWeight: 600,
                  color: item.suspicious ? '#fca5a5' : 'var(--text-main)'
                }}>
                  {item.name}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginTop: '1px' }}>
                  {item.category}
                </div>
              </div>
              <div style={{
                background: item.suspicious ? 'rgba(239, 68, 68, 0.15)' : 'rgba(56, 189, 248, 0.1)',
                color: item.suspicious ? '#ef4444' : 'var(--accent-cyan)',
                fontFamily: 'var(--font-mono)',
                fontWeight: 700,
                fontSize: '0.9rem',
                padding: '0.2rem 0.6rem',
                borderRadius: '6px',
                border: `1px solid ${item.suspicious ? 'rgba(239, 68, 68, 0.3)' : 'rgba(56, 189, 248, 0.2)'}`
              }}>
                {formatValue(item.name, item.value)}
              </div>
            </div>

            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
              {item.description}
            </div>

            {item.suspicious && (
              <div style={{
                marginTop: '0.5rem',
                fontSize: '0.75rem',
                color: '#ef4444',
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem'
              }}>
                <AlertCircle size={13} />
                <span>Anomalous flag triggered</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
