# 🔐 Authentication Setup Guide

Simple token-based authentication for securing the IDS API.

## Quick Setup

### 1. Set API Token (Environment Variable)

**Windows PowerShell**:
```powershell
$env:IDS_API_TOKEN = "your-secure-random-token-here"
uvicorn app.main:app --reload
```

**Linux/Mac**:
```bash
export IDS_API_TOKEN="your-secure-random-token-here"
uvicorn app.main:app --reload
```

**Generate Secure Token**:
```python
import secrets
token = secrets.token_urlsafe(32)
print(f"Your API token: {token}")
# Example output: "xK7n9mP2qL5vR8tY3wA6zB1cD4eF0gH_8iJ2kM5nP7qR"
```

### 2. Protected Endpoints

The following endpoints now require authentication:

- `POST /report` - Submit detections
- `DELETE /threats` - Clear threat storage

Public endpoints (no auth required):
- `GET /` - Health check
- `GET /detections` - View detections
- `GET /threats` - View threats
- `GET /model-info` - Model metadata

## Making Authenticated Requests

### Using curl

```bash
curl -X POST http://127.0.0.1:8000/report \
  -H "Authorization: Bearer your-secure-random-token-here" \
  -H "Content-Type: application/json" \
  -d '{"attack_type": "DoS", "confidence": 0.99}'
```

### Using Python

```python
import requests

API_TOKEN = "your-secure-random-token-here"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Submit detection
response = requests.post(
    "http://127.0.0.1:8000/report",
    headers=headers,
    json={
        "src_ip": "192.168.1.100",
        "dst_ip": "192.168.1.1",
        "attack_type": "DoS",
        "confidence": 0.99
    }
)
print(response.json())
```

### Using JavaScript (Frontend)

```javascript
const API_TOKEN = 'your-secure-random-token-here';

fetch('http://127.0.0.1:8000/report', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    src_ip: '192.168.1.100',
    dst_ip: '192.168.1.1',
    attack_type: 'DoS',
    confidence: 0.99
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## Error Responses

### Missing Token
```json
{
  "detail": "Missing authentication token"
}
```
**Status Code**: 401 Unauthorized

### Invalid Token
```json
{
  "detail": "Invalid authentication token"
}
```
**Status Code**: 403 Forbidden

## Production Deployment

### Best Practices

1. **Use Strong Tokens**:
   ```python
   # Generate 256-bit token
   import secrets
   token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits
   ```

2. **Store Securely**:
   - Use environment variables (never hardcode)
   - Add to `.env` file (gitignored)
   - Use secrets management (AWS Secrets Manager, Azure Key Vault)

3. **Rotate Regularly**:
   - Change tokens every 90 days
   - Immediate rotation if compromised

4. **HTTPS Only**:
   ```python
   # Enforce HTTPS in production
   if not request.url.scheme == "https":
       raise HTTPException(403, "HTTPS required")
   ```

5. **Rate Limiting**:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/report")
   @limiter.limit("100/minute")
   def report_detection(...):
       ...
   ```

### Docker Environment

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - IDS_API_TOKEN=${IDS_API_TOKEN}
    env_file:
      - .env
    ports:
      - "8000:8000"
```

**.env** (gitignored):
```
IDS_API_TOKEN=xK7n9mP2qL5vR8tY3wA6zB1cD4eF0gH_8iJ2kM5nP7qR
```

## Testing Authentication

### Test Script

```python
# test_auth.py
import requests

BASE_URL = "http://127.0.0.1:8000"
VALID_TOKEN = "your-secure-random-token-here"
INVALID_TOKEN = "wrong-token"

# Test 1: Missing token (should fail)
response = requests.post(f"{BASE_URL}/report", json={"test": "data"})
assert response.status_code == 401
print("✓ Test 1 passed: Missing token rejected")

# Test 2: Invalid token (should fail)
response = requests.post(
    f"{BASE_URL}/report",
    headers={"Authorization": f"Bearer {INVALID_TOKEN}"},
    json={"test": "data"}
)
assert response.status_code == 403
print("✓ Test 2 passed: Invalid token rejected")

# Test 3: Valid token (should succeed)
response = requests.post(
    f"{BASE_URL}/report",
    headers={"Authorization": f"Bearer {VALID_TOKEN}"},
    json={
        "src_ip": "192.168.1.1",
        "dst_ip": "192.168.1.2",
        "attack_type": "DoS",
        "confidence": 0.99,
        "is_attack": True
    }
)
assert response.status_code == 200
print("✓ Test 3 passed: Valid token accepted")

print("\nAll authentication tests passed!")
```

Run:
```bash
python test_auth.py
```

## Disabling Authentication (Development Only)

For local testing without auth:

1. **Don't set `IDS_API_TOKEN`** environment variable
2. Modify `backend/app/main.py`:
   ```python
   # Comment out authentication dependencies
   @app.post("/report")  # Remove: dependencies=[Depends(verify_token)]
   def report_detection(detection: dict):
       ...
   ```

**Warning**: Never deploy to production without authentication!

## Advanced: Multi-User Support

For multiple API users with different permissions:

```python
# backend/app/auth.py
import secrets
from typing import Dict

# Token -> User mapping
USERS = {
    "admin-token-here": {"username": "admin", "role": "admin"},
    "sensor-token-here": {"username": "sensor1", "role": "sensor"},
}

def verify_token_with_role(required_role: str = None):
    def verifier(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        user = USERS.get(token)
        
        if not user:
            raise HTTPException(403, "Invalid token")
        
        if required_role and user["role"] != required_role:
            raise HTTPException(403, f"Requires {required_role} role")
        
        return user
    
    return verifier

# Usage
@app.delete("/threats", dependencies=[Depends(verify_token_with_role("admin"))])
def clear_threats():
    ...  # Only admins can clear
```

## Troubleshooting

### Q: "Missing authentication token" even with token set

**Solution**: Check header format
```python
# Correct
headers = {"Authorization": "Bearer your-token"}

# Wrong
headers = {"Authorization": "your-token"}  # Missing "Bearer"
```

### Q: How to test auth in browser?

Use browser console:
```javascript
fetch('http://127.0.0.1:8000/report', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({...})
})
```

### Q: CORS issues with Authorization header?

Add to `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Ensures Authorization is allowed
)
```

## Security Checklist

Before deploying to production:

- [ ] Set strong API token (32+ bytes)
- [ ] Token stored in environment variable (not hardcoded)
- [ ] `.env` file added to `.gitignore`
- [ ] HTTPS enabled for all API calls
- [ ] Rate limiting implemented
- [ ] Token rotation schedule established (90 days)
- [ ] Access logs enabled
- [ ] Invalid token attempts monitored

## References

- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- OAuth2 Bearer Tokens: https://tools.ietf.org/html/rfc6750
- Python Secrets Module: https://docs.python.org/3/library/secrets.html
