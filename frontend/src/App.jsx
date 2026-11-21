import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import ModelInfoPage from './pages/ModelInfoPage';
import AboutPage from './pages/AboutPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'model' && <ModelInfoPage />}
        {activeTab === 'about' && <AboutPage />}
      </main>

      <Footer />
    </div>
  );
}
