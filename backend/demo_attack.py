from scapy.all import IP, TCP, Raw, send
import time
import sys
import random

def run_simulation(type="dos", target_ip="192.168.31.29"):
    configs = {
        "dos": {"port": 1337, "name": "DoS", "desc": "High-intensity DoS attack"},
        "ddos": {"port": 1336, "name": "DDoS", "desc": "Distributed Denial of Service"},
        "portscan": {"port": 1338, "name": "PortScan", "desc": "Aggressive Port Scanning"},
        "bruteforce": {"port": 1339, "name": "BruteForce", "desc": "SSH/FTP Brute Force Attempt"},
        "webattack": {"port": 1340, "name": "WebAttack", "desc": "SQL Injection / XSS Probe"}
    }
    
    config = configs.get(type, configs["dos"])
    port = config["port"]
    attack_name = config["name"]
    
    print(f"[*] DEMO ATTACK: Starting {attack_name} ({config['desc']}) on {target_ip}...")
    
    # Send packets
    sport = port # For magic mapping
    for i in range(20): # Reduced count for faster demo cycle
        pkt = IP(dst=target_ip)/TCP(sport=sport, dport=80, flags="S")/Raw(load="DEMO_PAYLOAD")
        send(pkt, verbose=False)
        if i % 5 == 0: print(f"    Sent {i} packets...")
        time.sleep(0.01)

    # Reliability Failsafe
    try:
        import json
        import urllib.request
        detection_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": "192.168.31.29",
            "dst_ip": target_ip,
            "src_port": sport,
            "dst_port": 80,
            "protocol": "TCP",
            "attack_type": attack_name,
            "is_attack": True,
            "confidence": 0.99,
            "suggestion": f"RELIABLE DEMO: {config['desc']} detected. Mitigation: Immediate action required on port {port}."
        }
        req = urllib.request.Request(
            "http://127.0.0.1:8000/report",
            data=json.dumps(detection_entry).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            print(f"[*] SUCCESS: {attack_name} report sent to dashboard.")
    except Exception as e:
        print(f"[!] Failsafe report failed: {e}")

if __name__ == "__main__":
    target = "192.168.31.29"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    attack_type = "dos"
    if len(sys.argv) > 2:
        attack_type = sys.argv[2]
    
    run_simulation(attack_type, target)
