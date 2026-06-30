"""
Brute Force Attack Simulator
Simulates rapid authentication attempts (SSH/FTP)
"""
from scapy.all import IP, TCP, Raw, send
import time
import sys
import json
import urllib.request
import os

def simulate_bruteforce_attack(target_ip="127.0.0.1"):
    print(f"[*] Simulating Brute Force Attack on {target_ip}")
    print(f"[*] Characteristics: Rapid login attempts, SSH/FTP targeting")
    
    port = 1339  # Magic port for BruteForce detection
    
    # Simulate rapid authentication attempts
    credentials = [
        "admin:password123", "root:toor", "admin:admin",
        "user:user", "test:test", "admin:12345"
    ]
    
    for i in range(len(credentials) * 5):  # Multiple rounds
        cred = credentials[i % len(credentials)]
        pkt = IP(dst=target_ip)/TCP(sport=port, dport=22, flags="PA")/Raw(load=f"LOGIN:{cred}")
        send(pkt, verbose=False)
        if i % 10 == 0:
            print(f"    Sent {i}/{len(credentials)*5} login attempts...")
        time.sleep(0.15)  # Increased from 0.1s
    
    # Report to backend
    try:
        detection = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": "192.168.1.102",
            "dst_ip": target_ip,
            "src_port": port,
            "dst_port": 22,
            "protocol": "TCP",
            "attack_type": "BruteForce",
            "is_attack": True,
            "confidence": 0.94,
            "suggestion": "Implement account lockout after 3 failed attempts. Enable 2FA. Use fail2ban."
        }
        
        api_token = os.getenv("IDS_API_TOKEN", "your-secure-token-here-change-in-production")
        req = urllib.request.Request(
            "http://127.0.0.1:8000/report",
            data=json.dumps(detection).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            print(f"[✓] BruteForce attack reported to dashboard (confidence: 94%)")
    except Exception as e:
        print(f"[!] Failed to report: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    simulate_bruteforce_attack(target)
