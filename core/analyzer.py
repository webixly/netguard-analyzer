from collections import Counter, defaultdict


def calculate_risk_level(suspicious_count: int, port_scan_count: int) -> str:
    score = suspicious_count * 2 + port_scan_count * 3

    if score >= 6:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"


def analyze_logs(entries: list[dict]) -> dict:
    ip_counter = Counter()
    failed_counter = Counter()
    ports_by_ip = defaultdict(set)
    ports_counter = Counter()

    for entry in entries:
        src_ip = entry["src_ip"]
        status = entry["status"]
        dst_port = entry["dst_port"]

        ip_counter[src_ip] += 1
        ports_by_ip[src_ip].add(dst_port)
        ports_counter[dst_port] += 1

        if status.upper() == "FAILED":
            failed_counter[src_ip] += 1

    suspicious_ips = []
    port_scan_candidates = []

    for ip, total_attempts in ip_counter.items():
        failed_attempts = failed_counter[ip]
        unique_ports = len(ports_by_ip[ip])

        if failed_attempts >= 3:
            suspicious_ips.append(
                {
                    "ip": ip,
                    "failed_attempts": failed_attempts,
                    "total_attempts": total_attempts,
                }
            )

        if unique_ports >= 4:
            port_scan_candidates.append(
                {
                    "ip": ip,
                    "unique_ports_targeted": unique_ports,
                    "ports": sorted(ports_by_ip[ip]),
                }
            )

    suspicious_ips.sort(key=lambda x: x["failed_attempts"], reverse=True)
    port_scan_candidates.sort(key=lambda x: x["unique_ports_targeted"], reverse=True)

    risk_level = calculate_risk_level(
        suspicious_count=len(suspicious_ips),
        port_scan_count=len(port_scan_candidates),
    )

    return {
        "total_entries": len(entries),
        "top_talkers": ip_counter.most_common(),
        "top_ports": ports_counter.most_common(),
        "suspicious_ips": suspicious_ips,
        "port_scan_candidates": port_scan_candidates,
        "risk_level": risk_level,
    }