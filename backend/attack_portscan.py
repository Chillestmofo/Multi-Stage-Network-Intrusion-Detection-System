"""
Port Scan Attack Simulator
Simulates network reconnaissance via port scanning
"""
from scapy.all import IP, TCP, send
import time
import sys
import json
import urllib.request
import os

def simulate_portscan_attack(target_ip="127.0.0.1"):
    print(f"[*] Simulating Port Scan on {target_ip}")
    print(f"[*] Characteristics: Sequential port probing, SYN flags")
    
    port = 1338  # Magic port for PortScan detection
    
    # Scan common ports
    common_ports = [21, 22, 23, 25, 80, 443, 445, 3306, 3389, 8080]
    
    for i, target_port in enumerate(common_ports * 3):  # Scan each port 3 times
        pkt = IP(dst=target_ip)/TCP(sport=port, dport=target_port, flags="S")
        send(pkt, verbose=False)
        if i % 10 == 0:
            print(f"    Scanned {i}/{len(common_ports)*3} ports...")
        time.sleep(0.1)  # Increased from 0.05s
    
    # Report to backend
    try:
        detection = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": "192.168.1.101",
            "dst_ip": target_ip,
            "src_port": port,
            "dst_port": 80,
            "protocol": "TCP",
            "attack_type": "PortScan",
            "is_attack": True,
            "confidence": 0.95,
            "suggestion": "Implement port knocking. Disable unused services. Enable IDS/IPS rules."
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
            print(f"[✓] PortScan attack reported to dashboard (confidence: 95%)")
    except Exception as e:
        print(f"[!] Failed to report: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    simulate_portscan_attack(target)
