import React, { useState, useEffect } from 'react';
import { Shield, Activity, Share2, AlertTriangle, CheckCircle2, Server, Terminal, X } from 'lucide-react';
import Threats from './Threats';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [detections, setDetections] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [criticalAlerts, setCriticalAlerts] = useState([]);
  const [stats, setStats] = useState({
    totalPackets: 0,
    attacksDetected: 0,
    health: 100
  });
  const [shownAlertTimestamps, setShownAlertTimestamps] = useState(new Set());

  const fetchDetections = async () => {
    try {
      const response = await fetch(`${API_BASE}/detections`);
      const data = await response.json();
      setDetections(data.reverse()); // Newest first

      const attacks = data.filter(d => d.is_attack).length;
      setStats({
        totalPackets: data.length,
        attacksDetected: attacks,
        health: data.length > 0 ? Math.max(0, 100 - (attacks / data.length) * 100).toFixed(1) : 100
      });

      // Detect critical threats (confidence > 0.9) and avoid re-showing same detection
      const newCritical = data.filter(d => d.is_attack && d.confidence > 0.9);
      if (newCritical.length > 0) {
        const latest = newCritical[0];
        const detectionId = `${latest.timestamp}-${latest.src_ip}-${latest.attack_type}`;

        // Only show alert if this specific detection hasn't been shown before
        if (!shownAlertTimestamps.has(detectionId)) {
          setShownAlertTimestamps(prev => new Set([...prev, detectionId]));
          const alert = {
            id: `${detectionId}-${Date.now()}`,
            ...latest,
            createdAt: Date.now()
          };
          setCriticalAlerts(prev => [alert, ...prev].slice(0, 3)); // Keep max 3 alerts
        }
      }
    } catch (error) {
      console.error('Error fetching detections:', error);
    }
  };

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_BASE}/model-info`);
      const data = await response.json();
      setModelInfo(data);
    } catch (error) {
      console.error('Error fetching model info:', error);
    }
  };

  const dismissAlert = (alertId) => {
    setCriticalAlerts(prev => prev.filter(a => a.id !== alertId));
  };

  useEffect(() => {
    fetchModelInfo();
    
    if (currentPage === 'dashboard') {
      fetchDetections();
      const interval = setInterval(fetchDetections, 3000); // 3s interval instead of 2s
      return () => clearInterval(interval);
    }
  }, [currentPage]);

  if (currentPage === 'threats') {
    return (
      <div>
        <nav className="nav-bar">
          <button onClick={() => setCurrentPage('dashboard')} className="nav-btn">
            📊 Dashboard
          </button>
          <button onClick={() => setCurrentPage('threats')} className="nav-btn active">
            🚨 Threats
          </button>
        </nav>
        <Threats />
      </div>
    );
  }

  return (
    <div>
      <nav className="nav-bar">
        <button onClick={() => setCurrentPage('dashboard')} className="nav-btn active">
          📊 Dashboard
        </button>
        <button onClick={() => setCurrentPage('threats')} className="nav-btn">
          🚨 Threats
        </button>
        {modelInfo && (
          <div style={{
            marginLeft: 'auto',
            fontSize: '0.75rem',
            color: 'var(--text-secondary)',
            padding: '0.5rem 1rem',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '0.5rem'
          }}>
            Model v{modelInfo.model_version}
          </div>
        )}
      </nav>
      
      {/* Critical Alert Notifications */}
      <div className="alert-container">
        {criticalAlerts.map(alert => (
          <div key={alert.id} className="critical-alert">
            <AlertTriangle size={20} style={{ color: 'var(--accent-red)', flexShrink: 0 }} />
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
                CRITICAL: {alert.attack_type} Detected
              </div>
              <div style={{ fontSize: '0.875rem', opacity: 0.9 }}>
                {alert.src_ip}:{alert.src_port} → {alert.dst_ip}:{alert.dst_port}
              </div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.25rem', opacity: 0.7 }}>
                Confidence: {(alert.confidence * 100).toFixed(1)}% | {alert.suggestion}
              </div>
            </div>
            <button 
              onClick={() => dismissAlert(alert.id)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                padding: '0.5rem',
                opacity: 0.7
              }}
            >
              <X size={18} />
            </button>
          </div>
        ))}
      </div>
      
      <div className="dashboard">
      <header className="dashboard-header">
        <div className="title-group">
          <h1>AI-Driven Intrusion Detection System</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Real-time Network Monitoring & AI Remediation</p>
        </div>
        <div className="status-badge">
          <div className="pulse"></div>
          <span>IDS Sensor Active</span>
        </div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">System Health</div>
          <div className="stat-value" style={{ color: stats.health > 90 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
            {stats.health}%
          </div>
          <Activity size={24} style={{ marginTop: '0.5rem', opacity: 0.5 }} />
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Flows Analyzed</div>
          <div className="stat-value">{stats.totalPackets}</div>
          <Server size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: 'var(--accent-blue)' }} />
        </div>
        <div className="stat-card">
          <div className="stat-label">Attacks Blocked</div>
          <div className="stat-value" style={{ color: stats.attacksDetected > 0 ? 'var(--accent-red)' : 'inherit' }}>
            {stats.attacksDetected}
          </div>
          <Shield size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: 'var(--accent-red)' }} />
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Network Flow (Src → Dst)</th>
              <th>Protocol</th>
              <th>IDS Result</th>
              <th>AI Suggestion</th>
            </tr>
          </thead>
          <tbody>
            {detections.length === 0 ? (
              <tr>
                <td colSpan="5" className="empty-state">
                  <Terminal size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                  <p>Monitoring network traffic... No flows detected yet.</p>
                </td>
              </tr>
            ) : (
              detections.map((d, i) => (
                <tr key={i}>
                  <td>{d.timestamp ? d.timestamp.split(' ')[1] : '-'}</td>
                  <td>
                    <div className="ip-flow">
                      <span title={`${d.src_ip}:${d.src_port}`}>{d.src_ip}</span>
                      <Share2 size={12} style={{ opacity: 0.3 }} />
                      <span title={`${d.dst_ip}:${d.dst_port}`}>
                        {d.dst_ip} <strong style={{ color: 'var(--accent-blue)' }}>:{d.dst_port}</strong>
                      </span>
                    </div>
                  </td>
                  <td>{d.protocol}</td>
                  <td>
                    <span className={`attack-pill ${d.is_attack ? 'is-attack' : 'is-normal'}`}>
                      {d.is_attack ? (
                        <><AlertTriangle size={12} style={{ marginRight: '4px' }} /> {d.attack_type}</>
                      ) : (
                        <><CheckCircle2 size={12} style={{ marginRight: '4px' }} /> Benign</>
                      )}
                    </span>
                    <div style={{ fontSize: '10px', marginTop: '4px', opacity: 0.5 }}>
                      Conf: {((d.confidence || 0) * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td>
                    <div className="suggestion-text">{d.suggestion}</div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
    </div>
  );
}

export default App;
