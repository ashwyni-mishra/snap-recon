"""WHOIS lookup module for Snap-Recon."""

from typing import Any, Dict, Optional

import whois

from core.logger import Logger


def run(domain: str) -> Optional[Dict[str, Any]]:
    """Perform a WHOIS lookup for the given domain.

    Args:
        domain: The domain to query.

    Returns:
        Optional[Dict[str, Any]]: WHOIS results including registrar and dates, or None on failure.
    """
    Logger.run(f"Running WHOIS lookup for {domain}")
    try:
        w = whois.whois(domain)
        result = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
        }
        Logger.success("WHOIS lookup completed")
        return result
    except Exception as e:
        Logger.error(f"WHOIS lookup failed: {e}")
        return None
