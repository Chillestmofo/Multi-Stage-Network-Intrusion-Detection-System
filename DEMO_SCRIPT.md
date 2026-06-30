# 🎬 IDS Demonstration Script

Quick reference guide for demonstrating the Multi-Stage Intrusion Detection System.

## Pre-Demo Checklist

- [ ] Backend API running on http://127.0.0.1:8000
- [ ] Frontend dashboard open at http://localhost:5173
- [ ] Terminal windows ready (3 recommended)
- [ ] Browser positioned to show dashboard

## Terminal Setup

```powershell
# Terminal 1: Backend API
cd C:\Coding\IDS_DETECTION\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend Dashboard
cd C:\Coding\IDS_DETECTION\frontend
npm run dev

# Terminal 3: Attack Simulation / Real-time Sensor
cd C:\Coding\IDS_DETECTION\backend
.\.venv\Scripts\Activate.ps1
```

---

## Scenario 1: Normal Traffic Detection

**Objective**: Show the system correctly identifies benign traffic.

**Commands**:
```powershell
# Generate normal ICMP traffic
ping 8.8.8.8 -n 10

# Generate normal HTTP traffic (optional)
curl https://www.google.com
curl https://www.github.com
```

**Expected Result**:
- Dashboard shows "Benign" classifications
- Confidence: 90%+
- System health remains 100%
- No alerts triggered

**Talking Points**:
- "Stage 1 filter identifies normal patterns with 90%+ confidence"
- "This prevents false positives and reduces alert fatigue"

---

## Scenario 2: DoS Attack Detection

**Objective**: Demonstrate high-confidence DoS attack detection.

**Commands**:
```powershell
# Using unified script
python demo_attack.py 127.0.0.1 dos

# OR using individual script
python attack_dos.py 127.0.0.1
```

**Expected Result**:
- Red alert appears immediately
- Attack Type: **DoS**
- Confidence: **99%**
- AI Suggestion: "Enable rate limiting on port 1337"
- Threat page updates with critical severity

**Talking Points**:
- "Multi-stage pipeline identifies DoS with 99% confidence"
- "AI advisor provides actionable mitigation steps"
- "Attack persists in Threats page for forensic analysis"

---

## Scenario 3: Port Scanning Detection

**Objective**: Show reconnaissance activity detection.

**Command**:
```powershell
# Using unified script
python demo_attack.py 127.0.0.1 portscan

# OR using individual script
python attack_portscan.py 127.0.0.1
```

**Expected Result**:
- Attack Type: **PortScan**
- Confidence: 95%+
- AI Suggestion: "Implement port knocking or disable unused services"
- Flow shows multiple SYN packets

**Talking Points**:
- "System detects network reconnaissance attempts"
- "Flow-based features identify scanning patterns"
- "Early warning of potential attack preparation"

---

## Scenario 4: DDoS Attack Detection

**Objective**: Demonstrate distributed attack detection.

**Command**:
```powershell
# Using unified script
python demo_attack.py 127.0.0.1 ddos

# OR using individual script
python attack_ddos.py 127.0.0.1
```

**Expected Result**:
- Attack Type: **DDoS**
- Confidence: 97%+
- AI Suggestion: "Deploy DDoS mitigation (Cloudflare, AWS Shield)"

**Talking Points**:
- "Detects coordinated attacks from multiple sources"
- "Flow-based analysis identifies distributed patterns"

---

## Scenario 5: Web Attack Detection

**Objective**: Show SQL injection and XSS detection.

**Command**:
```powershell
# Using unified script
python demo_attack.py 127.0.0.1 webattack

# OR using individual script
python attack_webattack.py 127.0.0.1
```

**Expected Result**:
- Attack Type: **WebAttack**
- Confidence: 93%+
- AI Suggestion: "Deploy WAF (ModSecurity). Sanitize inputs."

**Talking Points**:
- "Identifies common web exploitation attempts"
- "Protects against OWASP Top 10 vulnerabilities"

---

## Scenario 6: Brute Force Detection

**Objective**: Demonstrate login attack detection.

**Command**:
```powershell
# Using unified script
python demo_attack.py 127.0.0.1 bruteforce

# OR using individual script
python attack_bruteforce.py 127.0.0.1
```

**Expected Result**:
- Attack Type: **BruteForce**
- Confidence: 94%+
- AI Suggestion: "Implement account lockout (fail2ban)"

**Talking Points**:
- "Detects rapid authentication attempts"
- "Protects against credential stuffing attacks"

---

## Scenario 7: All Attack Types (Stress Test)

**Objective**: Show system handling multiple simultaneous attacks.

**Commands** (run sequentially):
```powershell
# Run all attack types
python attack_dos.py 127.0.0.1
python attack_ddos.py 127.0.0.1
python attack_portscan.py 127.0.0.1
python attack_bruteforce.py 127.0.0.1
python attack_webattack.py 127.0.0.1

# OR using unified script
python demo_attack.py 127.0.0.1 dos
python demo_attack.py 127.0.0.1 ddos
python demo_attack.py 127.0.0.1 portscan
python demo_attack.py 127.0.0.1 bruteforce
python demo_attack.py 127.0.0.1 webattack
```

**Expected Result**:
- Multiple threat types displayed
- Dashboard shows increased attack rate
- Threats page accumulates all attacks
- System health decreases proportionally

**Talking Points**:
- "Real-world scenarios involve multiple attack vectors"
- "System maintains performance under load"
- "Circular buffer ensures memory efficiency"

---

## Scenario 8: Threats Intelligence Page

**Objective**: Show persistent threat storage and analysis.

**Navigation**:
1. Click "🚨 Threats" tab in the dashboard
2. Show severity classification (Critical/High/Medium)
3. Scroll through threat history
4. Point out mitigation strategies

**Talking Points**:
- "Stores up to 1,000 attacks for forensic analysis"
- "Severity-based classification for prioritization"
- "Attacks don't disappear like in real-time dashboard"

---

## Scenario 9: Real-Time Sensor (Advanced)

**Objective**: Show live packet capture and flow analysis.

**Setup** (requires Administrator):
```powershell
# Run as Administrator
cd C:\Coding\IDS_DETECTION\backend
.\.venv\Scripts\Activate.ps1
python -c "from app.realtime.sniffer import start_sniffing; start_sniffing()"
```

**Generate Traffic**:
```powershell
# In another terminal
ping 8.8.8.8 -t
```

**Expected Result**:
- Console shows captured flows
- Features extracted in real-time
- IDS results printed to console
- Dashboard updates automatically

**Talking Points**:
- "Uses Scapy for raw packet capture"
- "Flow-based aggregation (5-tuple)"
- "Real-time feature extraction (CICIDS-style)"

---

## Demo Tips

### Before Starting
1. Clear threats page: click "Clear Threats" button
2. Refresh browser to reset counters
3. Position windows: dashboard (main), terminal (side)

### During Demo
1. Explain what you're doing **before** running commands
2. Wait 2-3 seconds for dashboard to update
3. Highlight confidence scores and AI suggestions
4. Navigate between Dashboard and Threats pages

### Common Questions
- **"How fast can it detect?"**: < 100ms per flow
- **"What about encrypted traffic?"**: Flow-level features (packet sizes, timing) still work
- **"False positive rate?"**: < 5% with 90% confidence threshold
- **"Can it scale?"**: Yes, designed for distributed deployment

---

## Quick Reset Between Demos

```powershell
# Clear threats via API
curl -X DELETE http://127.0.0.1:8000/threats

# Or click "Clear Threats" button in UI
```

---

## Emergency Troubleshooting

**Dashboard not updating?**
```powershell
# Check backend is running
curl http://127.0.0.1:8000/

# Check CORS - should see detections
curl http://127.0.0.1:8000/detections
```

**Demo script fails?**
```powershell
# Check Python environment
cd backend
.\.venv\Scripts\Activate.ps1
python demo_attack.py 127.0.0.1 dos
```

**Port conflicts?**
```powershell
# Change backend port
uvicorn app.main:app --reload --port 8001

# Update frontend API_BASE in src/App.jsx
```
