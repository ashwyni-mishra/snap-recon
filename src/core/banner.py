"""Banner module for displaying Snap-Recon project identity."""

from rich.console import Console

console = Console()


def show_banner() -> None:
    """Display the Snap-Recon startup banner in the console."""
    banner_text = """
Snap-Recon
Rapid Reconnaissance Framework
Developed by syn9
Version 1.0
"""
    console.print(f"[bold cyan]{banner_text}[/bold cyan]")
