from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

from utils.banner import build_banner
from core.parser import parse_log_file
from core.analyzer import analyze_logs
from core.reporter import (
    print_summary,
    print_top_ips,
    print_top_ports,
    print_suspicious_ips,
    print_port_scan_candidates,
    save_report,
)


console = Console()


def run_analysis(log_file: str) -> None:
    try:
        entries = parse_log_file(log_file)

        if not entries:
            console.print(
                Panel(
                    f"[yellow]No valid log entries found in:[/yellow] {log_file}",
                    border_style="yellow",
                    title="Warning",
                )
            )
            return

        result = analyze_logs(entries)

        console.clear()
        console.print(build_banner())
        console.print(
            Panel(
                f"[bold white]Analyzing file:[/bold white] [cyan]{log_file}[/cyan]",
                border_style="blue",
                title="Analysis Target",
            )
        )

        print_summary(console, result)
        print_top_ips(console, result)
        print_top_ports(console, result)
        print_suspicious_ips(console, result)
        print_port_scan_candidates(console, result)

        save_choice = Prompt.ask(
            "[bold green]Do you want to save this report?[/bold green]",
            choices=["y", "n"],
            default="y",
        )

        if save_choice == "y":
            output_path = save_report(result)
            console.print(
                Panel(
                    f"[green]Report saved successfully:[/green]\n[white]{output_path}[/white]",
                    border_style="green",
                    title="Saved",
                )
            )

    except FileNotFoundError as exc:
        console.print(Panel(f"[red]{exc}[/red]", border_style="red", title="Error"))
    except Exception as exc:
        console.print(
            Panel(f"[red]Unexpected error:[/red] {exc}", border_style="red", title="Crash")
        )


def main() -> None:
    console.clear()
    console.print(build_banner())

    while True:
        console.print(
            Panel(
                "[bold cyan]1[/bold cyan] Analyze default sample log\n"
                "[bold cyan]2[/bold cyan] Analyze custom log file\n"
                "[bold cyan]3[/bold cyan] Exit",
                border_style="bright_blue",
                title="Main Menu",
            )
        )

        choice = Prompt.ask("Select an option", choices=["1", "2", "3"], default="1")

        if choice == "1":
            run_analysis("sample.log")

        elif choice == "2":
            log_file = Prompt.ask("Enter log file path")
            run_analysis(log_file)

        elif choice == "3":
            console.print(
                Panel(
                    "[bold green]Exiting NetGuard Analyzer. Goodbye.[/bold green]",
                    border_style="green",
                    title="Exit",
                )
            )
            break

        again = Prompt.ask(
            "\n[bold yellow]Return to main menu?[/bold yellow]",
            choices=["y", "n"],
            default="y",
        )

        if again != "y":
            console.print(
                Panel(
                    "[bold green]Session ended.[/bold green]",
                    border_style="green",
                    title="Done",
                )
            )
            break

        console.clear()
        console.print(build_banner())


if __name__ == "__main__":
    main()