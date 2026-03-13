from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_detailed_help():
    panel = Panel(
        "[bold cyan]Snap-Recon: Professional Reconnaissance Framework[/bold cyan]\n"
        "Developed by syn9 | GitHub: ashwyni-mishra\n\n"
        "This framework is designed for deep intelligence gathering across digital surfaces.\n"
        "It supports multi-threaded discovery, automated reporting, and expert wordlists.",
        title="[bold green]System Help[/bold green]",
        border_style="blue"
    )
    console.print(panel)

    table = Table(title="Module Documentation", box=None)
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("--whois", "Queries the WHOIS registry for domain ownership, registration, and registrar info.")
    table.add_row("--dns", "Resolves common DNS records (A, AAAA, MX, NS, TXT) using high-speed resolver threads.")
    table.add_row("--subdomains", "Active brute-force for subdomains. Identifies potential CNAME takeovers automatically.")
    table.add_row("--ports", "Multithreaded port scanner. Identifies services and attempts to grab banners for fingerprinting.")
    table.add_row("--tech", "Web application stack discovery. Fingerprints servers, CMS, and web application generators.")
    table.add_row("--headers", "Inspects HTTPS response headers for missing security controls (HSTS, CSP, etc.).")
    table.add_row("--dirs", "Rapid directory and file discovery hunting for hidden content like .env, .git, or admin panels.")
    table.add_row("--ssl", "Comprehensive certificate analysis (Subject, Issuer, Expiry, Version).")
    table.add_row("--wayback", "Historical URL extraction from the Wayback Machine archives.")
    table.add_row("--all", "Executes the full chain of modules. Recommended for thorough surface analysis.")

    console.print(table)

    console.print("\n[bold yellow]Utility Commands:[/bold yellow]")
    console.print("  [cyan]--download-wordlist[/cyan]  Fetches the SecLists professional wordlist for directory discovery.")
    console.print("  [cyan]--list-wordlists[/cyan]     Lists all available files in the wordlists/ directory.")
    console.print("  [cyan]-w, --wordlist[/cyan]      Provide custom wordlist(s). Supports comma-separated paths.")
    console.print("  [cyan]-t, --threads[/cyan]       Adjust the concurrency of the engine (Default: 10, Recommended: 20-50).")

    console.print("\n[bold green]Example Run:[/bold green]")
    console.print("  [white]snap-recon -d example.com --all -t 30[/white]")
    
    console.print("\n[bold blue]Documentation:[/bold blue]")
    console.print("  Run [italic]man snap-recon[/italic] for full system manual after installation.")
