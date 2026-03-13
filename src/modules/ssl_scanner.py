"""SSL certificate scanner module for Snap-Recon."""

import socket
import ssl
from datetime import datetime
from typing import Any, Dict, Optional

from core.logger import Logger


def run(domain: str) -> Optional[Dict[str, Any]]:
    """Scan and analyze the SSL/TLS certificate for a domain.

    Args:
        domain: The domain to scan.

    Returns:
        Optional[Dict[str, Any]]: Certificate details including subject, issuer, and expiry.
    """
    Logger.run(f"Running SSL/TLS Scanner for {domain}")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    return None

                subject = dict(x[0] for x in cert["subject"])
                issuer = dict(x[0] for x in cert["issuer"])

                expiry_str = cert["notAfter"]
                expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
                days_to_expiry = (expiry_date - datetime.utcnow()).days

                result = {
                    "subject": subject.get("commonName"),
                    "issuer": issuer.get("commonName"),
                    "expiry_date": expiry_str,
                    "days_left": days_to_expiry,
                    "version": ssock.version(),
                }

                Logger.success(f"SSL Scan completed. Cert expires in {days_to_expiry} days.")
                return result
    except Exception as e:
        Logger.error(f"SSL Scan failed: {e}")
        return None
