"""CLI argument parsing for Snap-Recon."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the framework.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Snap-Recon - Rapid Reconnaissance Framework", add_help=False)
    parser.add_argument("-d", "--domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--help", action="store_true", help="Show detailed system help")
    parser.add_argument("-h", action="store_true", help="Alias for --help")
    parser.add_argument("--all", action="store_true", help="Run all modules")
    parser.add_argument("--whois", action="store_true", help="Run WHOIS lookup")
    parser.add_argument("--dns", action="store_true", help="Run DNS enumeration")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain discovery")
    parser.add_argument("--ports", action="store_true", help="Run port scanner")
    parser.add_argument("--tech", action="store_true", help="Run technology detection")
    parser.add_argument("--headers", action="store_true", help="Run security header inspection")
    parser.add_argument("--dirs", action="store_true", help="Run directory discovery")
    parser.add_argument("--ssl", action="store_true", help="Run SSL/TLS scanner")
    parser.add_argument("--wayback", action="store_true", help="Fetch URLs from Wayback Machine")
    parser.add_argument("--list-wordlists", action="store_true", help="List available wordlists in wordlists/")
    parser.add_argument("--download-wordlist", action="store_true", help="Download a larger professional wordlist")
    parser.add_argument(
        "-w",
        "--wordlist",
        default="wordlists/default.txt",
        help="Path to custom wordlist (can be multiple separated by comma)",
    )
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for concurrent tasks")
    return parser.parse_args()
