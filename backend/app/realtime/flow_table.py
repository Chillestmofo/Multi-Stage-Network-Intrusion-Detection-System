from collections import defaultdict
import time

FLOW_TIMEOUT = 10  # seconds

flows = defaultdict(lambda: {
    "start_time": None,
    "last_seen": None,
    "fwd_packets": 0,
    "bwd_packets": 0,
    "fwd_bytes": 0,
    "bwd_bytes": 0,
    "packets": 0,
    "bytes": 0,
})

def get_flow_key(pkt):
    proto = pkt.payload.name
    src = pkt["IP"].src
    dst = pkt["IP"].dst

    sport = pkt.sport if hasattr(pkt, "sport") else 0
    dport = pkt.dport if hasattr(pkt, "dport") else 0

    return (src, dst, sport, dport, proto)

def update_flow(pkt):
    if not pkt.haslayer("IP"):
        return

    key = get_flow_key(pkt)
    now = time.time()
    size = len(pkt)

    flow = flows[key]

    if flow["start_time"] is None:
        flow["start_time"] = now

    flow["last_seen"] = now
    flow["packets"] += 1
    flow["bytes"] += size

    # Direction heuristic
    if pkt["IP"].src == key[0]:
        flow["fwd_packets"] += 1
        flow["fwd_bytes"] += size
    else:
        flow["bwd_packets"] += 1
        flow["bwd_bytes"] += size

def expire_flows():
    now = time.time()
    expired = []

    for key, flow in list(flows.items()):
        if now - flow["last_seen"] > FLOW_TIMEOUT:
            expired.append((key, flow))
            del flows[key]

    return expired
