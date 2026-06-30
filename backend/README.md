# 🔧 IDS Detection - Backend API

FastAPI-powered backend with multi-stage ML detection engine and real-time packet analysis.

## ✨ Features

### 🤖 Multi-Stage Detection Engine
- **Stage 1**: High-speed normal traffic filter (Random Forest)
- **Stage 2**: Specialized attack classifiers (5 models)
- **Adaptive Thresholds**: Dynamic confidence scoring per attack type
- **Smart Decision Logic**: Fallback mechanisms for edge cases

### 📡 Real-Time Packet Capture
- **Scapy Integration**: Low-level packet sniffing
- **Flow Aggregation**: Bidirectional flow tracking (30-second windows)
- **Feature Extraction**: 78 CICIDS-2017 compliant features
- **Memory Management**: Automatic flow expiration

### 🛡️ Attack Simulators
- `demo_attack.py`: Unified attack simulation interface
- `attack_dos.py`: DoS attack generator
- `attack_ddos.py`: DDoS attack simulator
- `attack_portscan.py`: Port scanning simulation
- `attack_bruteforce.py`: Brute force attack generator
- `attack_webattack.py`: Web attack simulator
- `high_intensity_attack.py`: High-volume attack testing

### 🔐 Security Features
- **Token-Based Authentication**: Bearer token for protected endpoints
- **Environment Variables**: Secure token storage
- **CORS Protection**: Configurable origins
- **Rate Limiting Ready**: Infrastructure for future implementation

### 📊 AI-Powered Advisor
- Context-aware mitigation suggestions
- Port-specific recommendations
- NIST-aligned security best practices

---

## 🛠️ Tech Stack

- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server with hot reload
- **scikit-learn**: ML model training and inference
- **Scapy**: Packet manipulation and capture
- **Pandas/NumPy**: Data processing
- **Joblib**: Model serialization

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
Administrator/root privileges (for packet capture)
Npcap (Windows) / libpcap (Linux/Mac)
```

### Setup

```powershell
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Run API Server

```powershell
# Development mode
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Run Packet Sniffer (Administrator Required)

```powershell
python -c "from app.realtime.sniffer import start_sniffing; start_sniffing()"
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                # FastAPI application entry
│   ├── decision.py            # Multi-stage detection engine
│   ├── ai_advisor.py          # Mitigation advisor
│   ├── models_loader.py       # ML model initialization
│   ├── feature_mapper.py      # Feature engineering
│   ├── auth.py                # Authentication middleware
│   ├── config.py              # Configuration settings
│   │
│   ├── api/
│   │   ├── predict.py         # Prediction endpoints
│   │   └── realtime.py        # Real-time detection API
│   │
│   ├── realtime/
│   │   ├── sniffer.py         # Packet capture engine
│   │   ├── flow_table.py      # Flow aggregation logic
│   │   └── extractor.py       # CICIDS feature extraction
│   │
│   └── artifacts/
│       ├── model_metadata.json     # Model info & metrics
│       ├── feature_order.json      # Feature names
│       └── feature_stats.json      # Normalization stats
│
├── models/
│   ├── normal_filter.pkl           # Stage 1: Benign filter
│   ├── dos_classifier.pkl          # Stage 2: DoS detector
│   ├── ddos_classifier.pkl         # Stage 2: DDoS detector
│   ├── portscan_classifier.pkl     # Stage 2: PortScan detector
│   ├── bruteforce_classifier.pkl   # Stage 2: BruteForce detector
│   └── webattack_classifier.pkl    # Stage 2: WebAttack detector
│
├── attack_*.py              # Individual attack simulators
├── demo_attack.py           # Unified demo interface
├── simulate_attack.py       # General attack simulation
├── high_intensity_attack.py # High-volume testing
├── requirements.txt         # Python dependencies
└── DEMO_GUIDE.md           # Presentation guide
```

---

## 🔌 API Endpoints

### Health & Info

```http
GET / 
Response: { "status": "IDS backend running", "model_version": "1.0", "auth_enabled": true }
```

```http
GET /model-info
Response: { "model_version": "1.0", "accuracy": 96.2, "models": [...] }
```

### Detection Endpoints

```http
GET /detections
Description: Get last 500 detections
Response: [{ "timestamp": "...", "src_ip": "...", "attack_type": "...", ... }]
```

```http
GET /threats
Description: Get last 1000 attacks only
Response: [{ "timestamp": "...", "attack_type": "DoS", "confidence": 0.98, ... }]
```

```http
POST /predict
Description: Predict single flow
Body: { "Source Port": 443, "Destination Port": 80, ... }
Response: { "is_attack": true, "attack_type": "DoS", "confidence": 0.98 }
```

### Protected Endpoints (Require Authentication)

```http
POST /report
Description: Submit detection to storage
Headers: { "Authorization": "Bearer <token>" }
Body: { "attack_type": "DoS", "confidence": 0.99, ... }
```

```http
DELETE /threats
Description: Clear all stored threats
Headers: { "Authorization": "Bearer <token>" }
```

### API Documentation

Interactive API docs available at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🔐 Authentication Setup

### Set API Token

```powershell
# Windows PowerShell
$env:IDS_API_TOKEN = "your-secure-token-here"

# Linux/Mac
export IDS_API_TOKEN="your-secure-token-here"
```

### Generate Secure Token

```python
import secrets
token = secrets.token_urlsafe(32)
print(f"API Token: {token}")
```

### Making Authenticated Requests

```bash
curl -X POST http://127.0.0.1:8000/report \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"attack_type": "DoS", "confidence": 0.99}'
```

> 📖 See [AUTH_SETUP.md](../AUTH_SETUP.md) for complete guide

---

## 🎬 Attack Simulation

### Unified Demo Interface

```powershell
# Basic syntax
python demo_attack.py <target_ip> <attack_type> [intensity]

# Examples
python demo_attack.py 127.0.0.1 dos
python demo_attack.py 192.168.1.1 portscan 500
python demo_attack.py 127.0.0.1 ddos 1000
python demo_attack.py 127.0.0.1 webattack
python demo_attack.py 127.0.0.1 bruteforce
```

### Attack Types

| Command | Description | Default Intensity |
|---------|-------------|-------------------|
| `dos` | Denial of Service | 100 packets |
| `ddos` | Distributed DoS | 200 packets |
| `portscan` | Port scanning | 100 ports |
| `bruteforce` | Login attempts | 50 attempts |
| `webattack` | SQL injection/XSS | 30 requests |

### High-Intensity Testing

```powershell
python high_intensity_attack.py
# Runs multiple attack types simultaneously
```

> 📖 See [DEMO_GUIDE.md](DEMO_GUIDE.md) for presentation scripts

---

## 🧪 Testing

### Unit Tests (Future)

```bash
pytest tests/ -v
```

### Manual Testing

```bash
# Test API health
curl http://127.0.0.1:8000/

# Test prediction
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Source Port": 80, "Destination Port": 443, ...}'
```

---

## 🔧 Configuration

Edit `app/config.py` to adjust:

```python
# Detection thresholds
NORMAL_THRESHOLD = 0.85
ATTACK_THRESHOLDS = {
    "DoS": 0.75,
    "DDoS": 0.70,
    "PortScan": 0.80,
    "BruteForce": 0.75,
    "WebAttack": 0.70
}

# Margin for confidence scoring
MARGIN = 0.1

# Flow timeout (seconds)
FLOW_TIMEOUT = 30
```

---

## 📊 Model Information

### Training Dataset
- **CICIDS-2017**: 3,538,929 network flows
- **Features**: 78 flow-level features
- **Classes**: 7 (Benign + 6 attack types)

### Model Architecture
- **Stage 1**: Random Forest (Benign vs Attack)
- **Stage 2**: 5 specialized classifiers
  - Random Forest
  - Gradient Boosting
  - Feature engineering optimized per attack type

### Performance
- Overall accuracy: **96.2%**
- Average inference time: **2.5 ms/flow**
- Throughput: **400 flows/second**

---

## 🐛 Troubleshooting

### Packet Capture Issues

**Windows**:
```powershell
# Install Npcap with WinPcap compatibility
# Run Python as Administrator
```

**Linux**:
```bash
# Grant capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Or run with sudo
sudo python3 -c "from app.realtime.sniffer import start_sniffing; start_sniffing()"
```

### Module Import Errors

```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Model Loading Errors

```bash
# Check models directory
ls models/

# Ensure .pkl files exist
# Re-train models using IDS_final.ipynb if missing
```

---

## 📈 Performance Optimization

### Production Deployment

```bash
# Use Gunicorn with Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Enable logging
uvicorn app.main:app --log-level info --access-log
```

### Caching

Models are loaded once at startup and cached in memory.

### Concurrency

FastAPI handles concurrent requests asynchronously. Adjust workers based on CPU cores.

---

## 🤝 Contributing

When contributing to the backend:
1. Follow PEP 8 style guide
2. Add docstrings to functions
3. Update API documentation
4. Test endpoints with Swagger UI
5. Ensure models are backward compatible

---

## 📄 License

MIT License - see main project LICENSE

---

<div align="center">

**Part of the Multi-Stage IDS Detection System**

[Main Documentation](../README.md) | [Frontend](../frontend/) | [Setup Guide](../SETUP.md)

</div>
