import React, { useState, useEffect } from 'react';
import './Admin.css';

function Admin({ isLocked, threatLevel, aiThoughts }) {
  const [threats, setThreats] = useState([
    { id: 1, ip: '192.168.1.1', status: 'TRAPPED', time: '18:05:12' },
    { id: 2, ip: '45.122.10.1', status: 'INTERCEPTED', time: '18:08:45' }
  ]);

  const handleReset = async () => {
    try {
      await fetch('http://localhost:8000/unlock', { method: 'POST' });
    } catch (e) {
      console.error("Failed to unlock");
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      const newThreat = {
        id: Date.now(),
        ip: `172.20.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
        status: 'TRAPPED',
        time: new Date().toLocaleTimeString()
      };
      setThreats(prev => [newThreat, ...prev].slice(0, 4));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="admin-body">
      {isLocked && (
        <div className="lock-overlay">
          <div className="warning-box">
            <span className="warning-icon">⚠️</span>
            <h1>CRITICAL BREACH</h1>
            <p>PHYSICAL AUTHENTICATION REQUIRED AT TERMINAL 01</p>
            <div className="loading-bar"></div>
          </div>
        </div>
      )}

      <div className="admin-container">
        <header className="admin-header">
          <h2>BAKERY_VAULT_v4.0</h2>
          <button 
            onClick={handleReset} 
            style={{ background: '#7D5A50', color: 'white', padding: '5px 15px', borderRadius: '8px', cursor: 'pointer', border: 'none', fontWeight: 'bold' }}
          >
            RESET SYSTEM
          </button>
          <div className="system-status">● SYSTEM ACTIVE</div>
        </header>

        <div className="admin-grid">
          <div className="stat-card">
            <h3>Honeypot Strength</h3>
            <div className="gauge">98%</div>
          </div>
          <div className="stat-card">
            <h3>Oven Temp</h3>
            <div className="gauge">350°F</div>
          </div>

          <div className="log-panel">
            <h3>Live Interception Feed</h3>
            {threats.map(t => (
              <div key={t.id} className="log-entry">
                <code>
                  [{t.time}] INTRUDER_DETECTED: {t.ip} {"->"}
                  <span className={`status-${t.status.toLowerCase()}`}> {t.status}</span>
                </code>
              </div>
            ))}
          </div>

          <div className="stat-card ai-thoughts-box">
            <h3>Aegis AI Sentry Analysis</h3>
            <p style={{ color: '#E890A2', fontWeight: 'bold', fontSize: '0.9rem', marginTop: '10px' }}>
              {aiThoughts || "Waiting for data..."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Admin;