"""Logging utility for Snap-Recon with colorized status icons."""

from rich.console import Console

console = Console()


class Logger:
    """Static logger class for standardized framework output."""

    @staticmethod
    def info(msg: str) -> None:
        """Print an informational message with a [+] prefix."""
        console.print(f"[bold blue][+][/bold blue] {msg}")

    @staticmethod
    def run(msg: str) -> None:
        """Print a task execution message with a [~] prefix."""
        console.print(f"[bold yellow][~][/bold yellow] {msg}")

    @staticmethod
    def success(msg: str) -> None:
        """Print a successful completion message with a [\u2713] prefix."""
        console.print(f"[bold green][\u2713][/bold green] {msg}")

    @staticmethod
    def warning(msg: str) -> None:
        """Print a warning message with a [!] prefix."""
        console.print(f"[bold magenta][!][/bold magenta] {msg}")

    @staticmethod
    def error(msg: str) -> None:
        """Print an error message with an [x] prefix."""
        console.print(f"[bold red][x][/bold red] {msg}")
