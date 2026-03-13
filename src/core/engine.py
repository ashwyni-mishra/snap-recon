"""Core reconnaissance engine for Snap-Recon."""

import json
import os
import re
from typing import Any, Dict, List, Set, Union
from concurrent.futures import ThreadPoolExecutor

import requests
from rich.console import Console
from rich.table import Table

from core.logger import Logger
from modules import (
    dir_scan,
    dns_enum,
    port_scanner,
    security_checks,
    ssl_scanner,
    subdomain_enum,
    tech_detect,
    wayback_urls,
    whois_lookup,
)

console = Console()


class ReconEngine:
    """Orchestrates the execution of all reconnaissance modules and reporting."""

    def __init__(self, args: Any) -> None:
        """Initialize the engine with CLI arguments.

        Args:
            args: Parsed command-line arguments.
        """
        self.args = args
        self.domain: str = args.domain
        self.results: Dict[str, Any] = {}
        self.risk_score: int = 0
        self.recommendations: List[str] = []
        self.smart_words: Set[str] = set()

        # Resolve wordlists path relative to package
        self.package_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_wordlist_dir = os.path.join(self.package_dir, "wordlists")
        
        if not self.args.wordlist:
            self.wordlists = [os.path.join(self.default_wordlist_dir, "default.txt")]
        else:
            self.wordlists = [wl.strip() for wl in self.args.wordlist.split(",")]

    def run_all(self) -> None:
        """Execute all requested reconnaissance tasks."""
        if self.args.download_wordlist:
            self.download_seclist()
            return

        if self.args.list_wordlists:
            self.list_available_wordlists()
            return

        Logger.info(f"Starting rapid reconnaissance on {self.domain}")

        # 1. Standard lookups
        if self.args.whois or self.args.all:
            self.results["whois"] = whois_lookup.run(self.domain)

        if self.args.dns or self.args.all:
            self.results["dns"] = dns_enum.run(self.domain)

        if self.args.ssl or self.args.all:
            self.results["ssl"] = ssl_scanner.run(self.domain)

        # 2. Parallel Tasks
        tasks = []

        with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            if self.args.subdomains or self.args.all:
                for wl in self.wordlists:
                    tasks.append(
                        (
                            "subdomains",
                            executor.submit(subdomain_enum.run, self.domain, wl, self.args.threads),
                        )
                    )

            if self.args.ports or self.args.all:
                tasks.append(("ports", executor.submit(port_scanner.run, self.domain, self.args.threads)))

            if self.args.tech or self.args.all:
                tasks.append(("tech", executor.submit(tech_detect.run, self.domain)))

            if self.args.headers or self.args.all:
                tasks.append(("headers", executor.submit(security_checks.run, self.domain)))

            if self.args.dirs or self.args.all:
                for wl in self.wordlists:
                    tasks.append(("dirs", executor.submit(dir_scan.run, self.domain, wl, self.args.threads)))

            if self.args.wayback or self.args.all:
                tasks.append(("wayback", executor.submit(wayback_urls.run, self.domain)))

        for name, future in tasks:
            res = future.result()
            if name in self.results:
                if isinstance(self.results[name], list) and isinstance(res, list):
                    self.results[name].extend(res)
                # Keep unique
                if isinstance(self.results[name], list):
                    seen = set()
                    unique_res = []
                    for item in self.results[name]:
                        item_str = str(item)
                        if item_str not in seen:
                            unique_res.append(item)
                            seen.add(item_str)
                    self.results[name] = unique_res
            else:
                self.results[name] = res

        # 3. Smart Wordlist Expansion
        if "subdomains" in self.results:
            self.expand_wordlist(self.results["subdomains"])

        # 4. Final Processing
        self.display_summary()
        self.calculate_risk_score()
        self.generate_report()

    def download_seclist(self) -> None:
        """Download professional wordlist from SecLists repository."""
        Logger.info("Downloading professional wordlist from SecLists...")
        url = (
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/"
            "Web-Content/directory-list-2.3-small.txt"
        )
        save_path = os.path.join(self.default_wordlist_dir, "seclist_directories.txt")
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                os.makedirs(self.default_wordlist_dir, exist_ok=True)
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                Logger.success(f"Professional wordlist saved to {save_path}")
            else:
                Logger.error(f"Failed to download wordlist. Status code: {response.status_code}")
        except Exception as e:
            Logger.error(f"Error downloading wordlist: {e}")

    def list_available_wordlists(self) -> None:
        """List all files in the wordlists directory."""
        if os.path.exists(self.default_wordlist_dir):
            files = [f for f in os.listdir(self.default_wordlist_dir) if os.path.isfile(os.path.join(self.default_wordlist_dir, f))]
            table = Table(title="Available Wordlists")
            table.add_column("File Name", style="cyan")
            table.add_column("Full Path", style="green")
            for f in files:
                table.add_row(f, os.path.join(self.default_wordlist_dir, f))
            console.print(table)
        else:
            Logger.error("Wordlists directory not found")

    def expand_wordlist(self, subdomains: List[Dict[str, str]]) -> None:
        """Extract unique keywords from discovered subdomains for future discovery.

        Args:
            subdomains: List of discovered subdomain objects.
        """
        Logger.run("Performing Smart Wordlist Expansion")
        for sub in subdomains:
            name = sub["subdomain"].split(f".{self.domain}")[0]
            parts = re.split(r"[-._]", name)
            for p in parts:
                if p and len(p) > 2:
                    self.smart_words.add(p)

        if self.smart_words:
            Logger.success(f"Extracted {len(self.smart_words)} unique words for future brute-force expansion")

    def display_summary(self) -> None:
        """Print visual summary tables of the scan results."""
        if "ports" in self.results and self.results["ports"]:
            table = Table(title="Open Ports & Banners")
            table.add_column("Port", style="cyan")
            table.add_column("Service/Banner", style="green")
            for p in self.results["ports"]:
                table.add_row(str(p["port"]), p["banner"] if p["banner"] else "Unknown")
            console.print(table)

        if "subdomains" in self.results and self.results["subdomains"]:
            table = Table(title="Discovered Subdomains")
            table.add_column("Subdomain", style="blue")
            table.add_column("IP Address", style="magenta")
            table.add_column("CNAME", style="yellow")
            for sub in self.results["subdomains"]:
                table.add_row(sub["subdomain"], str(sub["ip"]), sub["cname"] if sub["cname"] else "-")
            console.print(table)

    def calculate_risk_score(self) -> None:
        """Calculate a security risk score based on findings."""
        score = 0
        if "ports" in self.results and self.results["ports"]:
            ports = [p["port"] for p in self.results["ports"]]
            if any(p in ports for p in [21, 23, 3389, 445, 3306]):
                score += 4
                self.recommendations.append("CRITICAL: Exposed management or DB services. Restrict access.")
            elif len(ports) > 0:
                score += 1

        if "headers" in self.results and self.results["headers"]:
            missing = len(self.results["headers"])
            score += min(missing, 3)
            if missing > 0:
                self.recommendations.append("Apply missing security headers (HSTS, CSP, etc.).")

        if "dirs" in self.results and self.results["dirs"]:
            success_dirs = [d for d in self.results["dirs"] if str(d["status"]).startswith("2")]
            if success_dirs:
                score += 2
                self.recommendations.append(f"Review {len(success_dirs)} publicly accessible directories.")

        if "subdomains" in self.results:
            takeover = [
                s
                for s in self.results["subdomains"]
                if s["cname"] and any(p in s["cname"] for p in ["github.io", "herokuapp", "cloudfront", "s3.amazonaws"])
            ]
            if takeover:
                score += 3
                self.recommendations.append("HIGH: Potential subdomain takeover detected.")

        self.risk_score = min(score, 10)
        console.print(f"\n[bold red]Risk Score: {self.risk_score} / 10[/bold red]")
        for rec in self.recommendations:
            Logger.warning(f"Recommendation: {rec}")

    def generate_report(self) -> None:
        """Generate a Markdown report containing all findings."""
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{self.domain}_report.md")

        with open(report_path, "w") as f:
            f.write(f"# Snap-Recon Report for {self.domain}\n\n")
            f.write(f"**Risk Score:** {self.risk_score} / 10\n\n")

            if self.recommendations:
                f.write("## Recommendations\n")
                for rec in self.recommendations:
                    f.write(f"- {rec}\n")
                f.write("\n")

            if self.smart_words:
                f.write("## Smart Wordlist Expansion\n")
                f.write(f"```\n{', '.join(sorted(list(self.smart_words)))}\n```\n\n")

            if "whois" in self.results and self.results["whois"]:
                f.write("## WHOIS Data\n")
                f.write(f"```json\n{json.dumps(self.results['whois'], indent=4, default=str)}\n```\n\n")

            if "dns" in self.results and self.results["dns"]:
                f.write("## DNS Records\n")
                for qtype, records in self.results["dns"].items():
                    f.write(f"### {qtype}\n")
                    for r in records:
                        f.write(f"- {r}\n")
                f.write("\n")

            if "ssl" in self.results and self.results["ssl"]:
                ssl_data = self.results["ssl"]
                f.write("## SSL/TLS Certificate Info\n")
                f.write(f"- **Subject:** {ssl_data['subject']}\n")
                f.write(f"- **Issuer:** {ssl_data['issuer']}\n")
                f.write(f"- **Version:** {ssl_data['version']}\n")
                f.write(f"- **Expiry Date:** {ssl_data['expiry_date']} ({ssl_data['days_left']} days left)\n\n")

            if "subdomains" in self.results and self.results["subdomains"]:
                f.write("## Subdomains\n| Subdomain | IP | CNAME |\n|-----------|----|-------|\n")
                for sub in self.results["subdomains"]:
                    f.write(f"| {sub['subdomain']} | {sub['ip']} | {sub['cname'] if sub['cname'] else '-'} |\n")
                f.write("\n")

            if "ports" in self.results and self.results["ports"]:
                f.write("## Open Ports\n| Port | Banner |\n|------|--------|\n")
                for p in self.results["ports"]:
                    f.write(f"| {p['port']} | {p['banner']} |\n")
                f.write("\n")

            if "tech" in self.results and self.results["tech"]:
                f.write("## Technologies\n")
                for t in self.results["tech"]:
                    f.write(f"- {t}\n")
                f.write("\n")

            if "headers" in self.results and self.results["headers"]:
                f.write("## Security Findings (Headers)\n")
                for h in self.results["headers"]:
                    f.write(f"- {h}\n")
                f.write("\n")

            if "wayback" in self.results and self.results["wayback"]:
                f.write("## Historical URLs (Wayback Machine)\n")
                for url in self.results["wayback"][:50]:
                    f.write(f"- {url}\n")
                if len(self.results["wayback"]) > 50:
                    f.write(f"\n*... and {len(self.results['wayback']) - 50} more URLs found.*\n")
                f.write("\n")

            if "dirs" in self.results and self.results["dirs"]:
                f.write("## Discovered Directories\n")
                for d in self.results["dirs"]:
                    f.write(f"- {d['url']} (Status: {d['status']})\n")
                f.write("\n")

        Logger.success(f"Report generated: {report_path}")
