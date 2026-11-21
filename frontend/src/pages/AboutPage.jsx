import React from 'react';
import { Shield, BookOpen, AlertOctagon, HelpCircle, CheckCircle, Terminal, Cpu } from 'lucide-react';

export default function AboutPage() {
  const interviewQuestions = [
    {
      q: '1. What problem does PhishGuard AI solve?',
      a: 'Phishing attacks remain the leading root-cause vector for cyber intrusions and credential harvesting. Traditional blacklist mechanisms (such as Google Safe Browsing or DNS blocklists) fail against zero-hour phishing links because new phishing domains have an active lifespan of only 4 to 8 hours before being abandoned. PhishGuard AI extracts 30 mathematical, structural, and lexical features directly from the URL string to predict phishing probability in real-time (<5ms) without risky web crawling.'
    },
    {
      q: '2. Why did you choose Random Forest over single Decision Trees or Deep Learning?',
      a: 'Random Forest is an ensemble learning method combining multiple decision trees using Bagging (Bootstrap Aggregation) and random feature subsets. It overcomes single Decision Trees\' tendency to overfit high-dimensional data. Compared to Deep Learning (LSTMs/Transformers), Random Forest offers lightning-fast CPU inference (<5ms), lower memory footprint, complete interpretability via Gini feature importances, and immunity to monotonic feature scaling without requiring GPU infrastructure.'
    },
    {
      q: '3. Why is feature engineering necessary instead of feeding raw character sequences?',
      a: 'Feature engineering translates raw strings into structured domain knowledge. Cybersecurity indicators (like IP addresses used as hosts, excessive subdomains, brand typo-squatting, Shannon character entropy, and fake TLDs in subdomains) are mathematically encoded so the classifier learns genuine threat patterns rather than memorizing specific domain names.'
    },
    {
      q: '4. How did you extract all 30 features locally and safely?',
      a: 'Using Python\'s standard urllib.parse, regular expressions, and mathematical entropy calculations. Every feature is computed offline purely from the URL text string. Untrusted links are NEVER opened, downloaded, or connected to, preventing payload detonation and bot-detection triggers.'
    },
    {
      q: '5. How was the dataset selected and verified?',
      a: 'We verified and utilized a balanced 11,055-record benchmark corpus consisting of 5,528 active phishing links gathered from global threat feeds (Phishing.Database, OpenPhish) and 5,527 reputable domains from the Tranco Top 1M list. In addition, the project documents and benchmarks the classic academic UCI 11,055-record phishing website dataset (Mohammad et al., 2015).'
    },
    {
      q: '6. What is Data Leakage and how did you prevent it?',
      a: 'Data leakage occurs when information outside the training dataset is used to train the model, resulting in overly optimistic test scores that fail in production. We prevented leakage by performing stratified train/test splitting before hyperparameter tuning, fitting all transformations strictly on the training fold, and ensuring no duplicate records crossed the train/test boundary.'
    },
    {
      q: '7. What is Overfitting and how is it mitigated in your pipeline?',
      a: 'Overfitting occurs when a model memorizes noise in the training set rather than generalizing. In our Random Forest pipeline, overfitting was mitigated through 5-fold cross-validation, limiting maximum tree depth (max_depth=15), setting minimum samples per leaf (min_samples_leaf=1), and bagging 200 diverse decision trees.'
    },
    {
      q: '8. How do Precision and Recall differ in cybersecurity detection?',
      a: 'Precision = TP / (TP + FP). High precision means when the system flags a URL as Phishing, it is almost certainly malicious (our model achieves 99.90% precision with only 1 false positive). Recall = TP / (TP + FN). High recall means almost no real phishing links slip through unnoticed (our model achieves 99.80% recall with only 2 false negatives out of 991 test phish).'
    },
    {
      q: '9. How do React and FastAPI communicate?',
      a: 'The frontend sends an asynchronous HTTP POST request with a JSON payload { "url": "..." } via Axios to FastAPI\'s /predict endpoint. FastAPI validates the payload using Pydantic, calls the PredictionService singleton, computes the feature vector, executes model.predict_proba(), and returns a JSON response. CORS middleware permits secure cross-origin communication between localhost:5173 and localhost:8000.'
    },
    {
      q: '10. What are the limitations and future improvements?',
      a: 'Limitations: 1) Sophisticated zero-day phishing on legitimately compromised high-reputation domains (e.g. google.com/forms) can mimic legitimate structures; 2) Shortened URLs hide their final destination unless expanded. Future improvements include: 1) Safe headless HTTP header probing (inspecting SSL certificates and HTTP status codes via sandboxed egress); 2) Integration with threat intelligence feeds; 3) Browser extension for real-time protection.'
    }
  ];

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      {/* Overview */}
      <div className="glass-card" style={{ padding: '2.5rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--accent-cyan)', marginBottom: '0.5rem' }}>
          <BookOpen size={24} />
          <span style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '0.85rem' }}>
            System Architecture & Technical Documentation
          </span>
        </div>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '1rem' }}>
          About PhishGuard AI
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1rem', lineHeight: 1.7, marginBottom: '1rem' }}>
          PhishGuard AI is an intelligent risk analysis system engineered for modern cybersecurity operations.
          Unlike traditional static domain blacklists that suffer from severe zero-hour detection gaps,
          PhishGuard AI analyzes the fundamental syntactic, structural, and statistical properties of URLs.
        </p>
        <p style={{ color: 'var(--text-muted)', fontSize: '1rem', lineHeight: 1.7 }}>
          By processing 30 distinct engineered characteristics through a tuned Random Forest ensemble,
          the system flags deceptive intent—such as IP-based hostnames, excessive subdomains, brand typo-squatting,
          and abnormal character entropy—without ever establishing a connection to untrusted malicious web servers.
        </p>
      </div>

      {/* 3 Pillars */}
      <div className="grid-cols-3" style={{ marginBottom: '2.5rem' }}>
        <div className="glass-card" style={{ padding: '1.75rem' }}>
          <div style={{
            background: 'rgba(56, 189, 248, 0.1)',
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <Shield size={22} color="var(--accent-cyan)" />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Safe Heuristic Inspection
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Never crawls or opens untrusted links. All 30 features are computed strictly from lexical URL text, protecting analysis infrastructure from drive-by payloads.
          </p>
        </div>

        <div className="glass-card" style={{ padding: '1.75rem' }}>
          <div style={{
            background: 'rgba(16, 185, 129, 0.1)',
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <Cpu size={22} color="#10b981" />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Ensemble Machine Learning
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            200 Decision Trees with Bootstrap Aggregation. Evaluates complex non-linear feature interactions with calibrated probability scoring and Gini importance metrics.
          </p>
        </div>

        <div className="glass-card" style={{ padding: '1.75rem' }}>
          <div style={{
            background: 'rgba(147, 51, 234, 0.1)',
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <Terminal size={22} color="#a855f7" />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Microservice Integration
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Decoupled React.js frontend communicating with a high-performance Python FastAPI backend via REST APIs and Pydantic schemas.
          </p>
        </div>
      </div>

      {/* Placement & Technical Interview Section */}
      <div className="glass-card" style={{ padding: '2.5rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.5rem' }}>
          <HelpCircle size={22} />
          <span style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '0.85rem' }}>
            College Major Project & Technical Interview Master Guide
          </span>
        </div>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '1.5rem' }}>
          Key Technical Interview Questions & Answers
        </h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {interviewQuestions.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '10px',
                padding: '1.25rem'
              }}
            >
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--accent-cyan)', marginBottom: '0.5rem' }}>
                {item.q}
              </h4>
              <p style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: 1.65 }}>
                {item.a}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
