import React, { useState, useEffect } from 'react';
import { AlertTriangle, Shield, Trash2, Clock, Target, Activity } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

function Threats() {
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    critical: 0,
    high: 0,
    medium: 0
  });

  const fetchThreats = async () => {
    try {
      const response = await fetch(`${API_BASE}/threats`);
      const data = await response.json();
      setThreats(data.reverse()); // Newest first

      // Calculate severity stats
      const critical = data.filter(t => t.confidence > 0.9).length;
      const high = data.filter(t => t.confidence > 0.7 && t.confidence <= 0.9).length;
      const medium = data.filter(t => t.confidence <= 0.7).length;

      setStats({
        total: data.length,
        critical,
        high,
        medium
      });
    } catch (error) {
      console.error('Error fetching threats:', error);
    }
  };

  const clearThreats = async () => {
    if (window.confirm('Clear all stored threats? This cannot be undone.')) {
      try {
        await fetch(`${API_BASE}/threats`, { method: 'DELETE' });
        fetchThreats();
      } catch (error) {
        console.error('Error clearing threats:', error);
      }
    }
  };

  useEffect(() => {
    fetchThreats();
    const interval = setInterval(fetchThreats, 3000);
    return () => clearInterval(interval);
  }, []);

  const getSeverityColor = (confidence) => {
    if (confidence > 0.9) return 'var(--accent-red)';
    if (confidence > 0.7) return '#ff6b35';
    return '#ffa500';
  };

  const getSeverityLabel = (confidence) => {
    if (confidence > 0.9) return 'CRITICAL';
    if (confidence > 0.7) return 'HIGH';
    return 'MEDIUM';
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="title-group">
          <h1>🚨 Threat Intelligence Center</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Attack Detection History & Analysis
          </p>
        </div>
        <button 
          onClick={clearThreats} 
          className="clear-btn"
          style={{
            padding: '0.5rem 1rem',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid var(--accent-red)',
            borderRadius: '6px',
            color: 'var(--accent-red)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.875rem'
          }}
        >
          <Trash2 size={16} />
          Clear Threats
        </button>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Threats</div>
          <div className="stat-value">{stats.total}</div>
          <Shield size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: 'var(--accent-red)' }} />
        </div>
        <div className="stat-card">
          <div className="stat-label">Critical Severity</div>
          <div className="stat-value" style={{ color: 'var(--accent-red)' }}>{stats.critical}</div>
          <AlertTriangle size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: 'var(--accent-red)' }} />
        </div>
        <div className="stat-card">
          <div className="stat-label">High Severity</div>
          <div className="stat-value" style={{ color: '#ff6b35' }}>{stats.high}</div>
          <Target size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: '#ff6b35' }} />
        </div>
        <div className="stat-card">
          <div className="stat-label">Medium Severity</div>
          <div className="stat-value" style={{ color: '#ffa500' }}>{stats.medium}</div>
          <Activity size={24} style={{ marginTop: '0.5rem', opacity: 0.5, color: '#ffa500' }} />
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Severity</th>
              <th>Timestamp</th>
              <th>Attack Type</th>
              <th>Source → Target</th>
              <th>Protocol</th>
              <th>Confidence</th>
              <th>AI Mitigation Strategy</th>
            </tr>
          </thead>
          <tbody>
            {threats.length === 0 ? (
              <tr>
                <td colSpan="7" className="empty-state">
                  <Shield size={48} style={{ marginBottom: '1rem', opacity: 0.2, color: 'var(--accent-green)' }} />
                  <p>No threats detected. System is secure.</p>
                </td>
              </tr>
            ) : (
              threats.map((threat, i) => (
                <tr key={i} style={{ borderLeft: `3px solid ${getSeverityColor(threat.confidence)}` }}>
                  <td>
                    <span 
                      style={{
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontSize: '11px',
                        fontWeight: 'bold',
                        background: `${getSeverityColor(threat.confidence)}22`,
                        color: getSeverityColor(threat.confidence),
                        border: `1px solid ${getSeverityColor(threat.confidence)}`
                      }}
                    >
                      {getSeverityLabel(threat.confidence)}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Clock size={12} style={{ opacity: 0.5 }} />
                      {threat.timestamp}
                    </div>
                  </td>
                  <td>
                    <span className="attack-pill is-attack">
                      <AlertTriangle size={12} style={{ marginRight: '4px' }} />
                      {threat.attack_type}
                    </span>
                  </td>
                  <td>
                    <div style={{ fontSize: '0.875rem', fontFamily: 'monospace' }}>
                      {threat.src_ip}:{threat.src_port} → {threat.dst_ip}:{threat.dst_port}
                    </div>
                  </td>
                  <td>{threat.protocol}</td>
                  <td>
                    <div style={{ 
                      fontWeight: 'bold', 
                      color: getSeverityColor(threat.confidence) 
                    }}>
                      {(threat.confidence * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td>
                    <div className="suggestion-text" style={{ maxWidth: '400px' }}>
                      {threat.suggestion}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem', 
        background: 'rgba(59, 130, 246, 0.05)',
        border: '1px solid rgba(59, 130, 246, 0.2)',
        borderRadius: '8px',
        fontSize: '0.875rem',
        color: 'var(--text-secondary)'
      }}>
        <strong>ℹ️ Note:</strong> This page stores up to 1,000 detected threats. 
        Real-time detections (including normal traffic) are shown on the main dashboard with a 500-event limit.
        Both use circular buffers - oldest entries are removed when limits are reached.
      </div>
    </div>
  );
}

export default Threats;
