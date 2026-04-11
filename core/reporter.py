import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def risk_style(risk_level: str) -> str:
    mapping = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "red",
    }
    return mapping.get(risk_level.upper(), "white")


def print_summary(console: Console, result: dict) -> None:
    style = risk_style(result["risk_level"])
    summary = (
        f"[bold]Total Log Entries:[/bold] {result['total_entries']}\n"
        f"[bold]Suspicious IPs:[/bold] {len(result['suspicious_ips'])}\n"
        f"[bold]Port Scan Candidates:[/bold] {len(result['port_scan_candidates'])}\n"
        f"[bold]Risk Level:[/bold] [{style}]{result['risk_level']}[/{style}]"
    )
    console.print(Panel(summary, title="Summary", border_style=style))


def print_top_ips(console: Console, result: dict) -> None:
    table = Table(title="Top Active IPs", border_style="cyan")
    table.add_column("IP Address", style="bold white")
    table.add_column("Events", justify="right", style="green")

    for ip, count in result["top_talkers"]:
        table.add_row(ip, str(count))

    console.print(table)


def print_top_ports(console: Console, result: dict) -> None:
    table = Table(title="Top Targeted Ports", border_style="magenta")
    table.add_column("Port", style="bold white")
    table.add_column("Hits", justify="right", style="yellow")

    for port, count in result["top_ports"]:
        table.add_row(str(port), str(count))

    console.print(table)


def print_suspicious_ips(console: Console, result: dict) -> None:
    table = Table(title="Suspicious IPs", border_style="red")
    table.add_column("IP Address", style="bold white")
    table.add_column("Failed Attempts", justify="right", style="red")
    table.add_column("Total Attempts", justify="right", style="yellow")

    if not result["suspicious_ips"]:
        table.add_row("None", "-", "-")
    else:
        for item in result["suspicious_ips"]:
            table.add_row(
                item["ip"],
                str(item["failed_attempts"]),
                str(item["total_attempts"]),
            )

    console.print(table)


def print_port_scan_candidates(console: Console, result: dict) -> None:
    table = Table(title="Port Scan Candidates", border_style="bright_red")
    table.add_column("IP Address", style="bold white")
    table.add_column("Unique Ports", justify="right", style="yellow")
    table.add_column("Ports", style="cyan")

    if not result["port_scan_candidates"]:
        table.add_row("None", "-", "-")
    else:
        for item in result["port_scan_candidates"]:
            ports = ", ".join(str(p) for p in item["ports"])
            table.add_row(
                item["ip"],
                str(item["unique_ports_targeted"]),
                ports,
            )

    console.print(table)


def save_report(result: dict) -> str:
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = reports_dir / f"report_{timestamp}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    return str(output_file)