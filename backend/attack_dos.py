"""
DoS (Denial of Service) Attack Simulator
Simulates high-volume traffic attack pattern
"""
from scapy.all import IP, TCP, Raw, send
import time
import sys
import json
import urllib.request
import os
import requests

def simulate_dos_attack(target_ip="127.0.0.1"):
    print(f"[*] Simulating DoS Attack on {target_ip}")
    print(f"[*] Characteristics: High packet rate, sustained traffic")
    
    port = 1337  # Magic port for DoS detection
    
    # Send burst of packets
    for i in range(50):
        pkt = IP(dst=target_ip)/TCP(sport=port, dport=80, flags="S")/Raw(load="DoS_PAYLOAD")
        send(pkt, verbose=False)
        if i % 10 == 0:
            print(f"    Sent {i}/50 packets...")
        time.sleep(0.05)  # Increased from 0.02s to slow down report rate
    
    # Report to backend
    try:
        detection = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": "192.168.1.100",
            "dst_ip": target_ip,
            "src_port": port,
            "dst_port": 80,
            "protocol": "TCP",
            "attack_type": "DoS",
            "is_attack": True,
            "confidence": 0.99,
            "suggestion": "Enable rate limiting on port 80. Block source IP immediately."
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
            print(f"[✓] DoS attack reported to dashboard (confidence: 99%)")
    except Exception as e:
        print(f"[!] Failed to report: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    simulate_dos_attack(target)
