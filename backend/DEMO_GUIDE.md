# 🛡️ IDS Project Demonstration Guide

This guide provides a structured flow for presenting the **Multi-Stage Intrusion Detection System** to your teacher.

---

## 🚀 Step 1: System Initialization
Start all three components in separate terminals to show the "full-stack" nature of the project.

1.  **Backend API**: 
    ```powershell
    cd backend
    .\.venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
    ```
2.  **Network Sniffer**:
    ```powershell
    cd backend
    .\.venv\Scripts\python.exe -c "from app.realtime.sniffer import start_sniffing; start_sniffing()"
    ```
3.  **Frontend Dashboard**:
    ```powershell
    cd frontend
    npm run dev
    ```
    *Open [http://localhost:5173](http://localhost:5173) in your browser.*

---

## 🟢 Step 2: Showcasing "Normal" Traffic
Demonstrate that the system can distinguish benign activity from threats.

1.  **Idle State**: Show the dashboard with a "Healthy" status.
2.  **Generate Traffic**: Open a new browser tab and visit any website (e.g., google.com).
3.  **Observe**: Watch the dashboard update with **"Normal"** classifications (Confidence ~0.90+).
4.  **Explain**: *"The system uses a Stage-1 ML filter to identify known safe patterns, ensuring low latency for standard traffic."*

---

## 🔴 Step 3: High-Confidence Attack Simulations
Use the `demo_attack.py` script to trigger specific, high-confidence alerts.

### A. Denial of Service (DoS)
- **Command**: `python demo_attack.py 127.0.0.1 dos`
- **Result**: Immediate red alert for **DoS** with **0.99 Confidence**.
- **Highlight**: The AI mitigation suggestion: *"Enable rate limiting on port 1337."*

### B. Port Scanning
- **Command**: `python demo_attack.py 127.0.0.1 portscan`
- **Result**: Alert for **PortScan**.
- **Highlight**: Explain how the sniffer tracks SYN packets to detect mapping attempts.

### C. Brute Force Attempt
- **Command**: `python demo_attack.py 127.0.0.1 bruteforce`
- **Result**: Alert for **BruteForce**.
- **Highlight**: Mention that the system detects rapid login-like patterns.

---

## 🤖 Step 4: The AI Advisor & Decision Logic
Explain the "Magic" behind the detection.

1.  **Explain the 2-Stage Process**:
    - **Stage 1**: Filters normal traffic.
    - **Stage 2**: Classifies specific attack types (DoS, PortScan, etc.).
2.  **Show the AI Suggestion**: Click on an attack row in the dashboard to show the detailed mitigation steps provided by the `ai_advisor`.
3.  **Explain Safe Thresholds**: Point out that low-confidence anomalies are automatically labeled as **"Safe"** to prevent bothering the admin with false alarms.

---

## 🏁 Conclusion
- **Scalability**: Mention the backend can handle 500+ events in its history.
- **Accuracy**: Highlight the 95%+ confidence scores for core attack types.
- **Interactivity**: Invite the teacher to run a simulation command themselves!
