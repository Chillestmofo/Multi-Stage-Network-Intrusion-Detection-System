from scapy.all import IP, TCP, send
import time
import sys

def simulate_portscan(target_ip, start_port=1, end_port=100):
    print(f"[*] Starting PortScan simulation on {target_ip} (Ports {start_port}-{end_port})...")
    for port in range(start_port, end_port + 1):
        # Send SYN packet
        pkt = IP(dst=target_ip)/TCP(dport=port, flags="S")
        send(pkt, verbose=False)
        if port % 10 == 0:
            print(f"    Scanned up to port {port}...")
        time.sleep(0.1) # Small delay to avoid overwhelming local stack but fast enough for flow detection
    print("[*] PortScan simulation complete.")

if __name__ == "__main__":
    target = "127.0.0.1" # Target local loopback for safe simulation
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    simulate_portscan(target)
