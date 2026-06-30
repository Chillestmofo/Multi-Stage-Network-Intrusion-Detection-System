def get_suggestion(attack_type, dst_port):
    suggestions = {
        "Normal": "System Secure. Traffic appears benign.",
        "DoS": f"Potential Denial of Service detected on port {dst_port}. Mitigation: Enable rate limiting and check for volumetric anomalies.",
        "DDoS": f"Distributed Denial of Service attack signature identified on port {dst_port}. Mitigation: Deploy cloud-based scrubbing or blackhole routing if necessary.",
        "PortScan": f"Port scanning activity detected from source. Mitigation: Cloak common ports and implement temporary IP blocking for rapid scanners.",
        "BruteForce": f"Brute force attempt detected on port {dst_port}. Mitigation: Enforce multi-factor authentication and temporary account lockout.",
        "WebAttack": f"Web application attack detected on port {dst_port}. Mitigation: Review WAF logs and sanitize input fields for SQLi/XSS.",
        "Unknown": f"Unidentified anomalous traffic detected on port {dst_port}. Mitigation: Investigate flow details and monitor for further suspicious patterns."
    }
    return suggestions.get(attack_type, "Unrecognized activity. Recommendation: Manual traffic analysis required.")
