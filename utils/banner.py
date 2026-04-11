from rich.panel import Panel
from rich.align import Align


def build_banner() -> Panel:
    title = """
███    ██ ███████ ████████  ██████  ██    ██  █████  ██████  ██████
████   ██ ██         ██    ██       ██    ██ ██   ██ ██   ██ ██   ██
██ ██  ██ █████      ██    ██   ███ ██    ██ ███████ ██████  ██   ██
██  ██ ██ ██         ██    ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
██   ████ ███████    ██     ██████   ██████  ██   ██ ██   ██ ██████
"""
    subtitle = "[bold cyan]NetGuard Analyzer[/bold cyan]\n[white]Blue Team Log Analysis Toolkit[/white]"
    return Panel(
        Align.center(f"[green]{title}[/green]\n{subtitle}"),
        border_style="bright_blue",
        padding=(1, 2),
        title="[bold magenta]v1.0[/bold magenta]",
    )