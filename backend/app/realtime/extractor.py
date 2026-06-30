def extract_features(flow, dport, sport=0):
    duration = flow["last_seen"] - flow["start_time"]

    if duration <= 0:
        duration = 0.0001

    return {
        "Source Port": sport,
        "Destination Port": dport,
        "Flow Duration": duration * 1e6,  # microseconds
        "Total Fwd Packets": flow["fwd_packets"],
        "Total Backward Packets": flow["bwd_packets"],
        "Total Length of Fwd Packets": flow["fwd_bytes"],
        "Total Length of Bwd Packets": flow["bwd_bytes"],
        "Flow Packets/s": flow["packets"] / duration,
        "Flow Bytes/s": flow["bytes"] / duration,
        "Packet Length Mean": flow["bytes"] / max(flow["packets"], 1),
        "Down/Up Ratio": (
            flow["bwd_packets"] / max(flow["fwd_packets"], 1)
        ),
    }
