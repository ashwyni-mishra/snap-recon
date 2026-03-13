"""DNS enumeration module for Snap-Recon."""

from typing import Dict, List

import dns.resolver

from core.logger import Logger


def run(domain: str) -> Dict[str, List[str]]:
    """Enumerate common DNS records for a domain.

    Args:
        domain: The domain to enumerate.

    Returns:
        Dict[str, List[str]]: Mapping of record types to lists of resolved records.
    """
    Logger.run(f"Running DNS enumeration for {domain}")
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    results = {}

    for qtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, qtype)
            results[qtype] = [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        except Exception as e:
            Logger.warning(f"Error resolving {qtype} for {domain}: {e}")

    if results:
        Logger.success("DNS enumeration completed")
    else:
        Logger.warning("No standard DNS records found")

    return results
