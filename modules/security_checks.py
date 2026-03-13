"""Security header inspection module for Snap-Recon."""

from typing import List

import requests

from core.logger import Logger


def run(domain: str) -> List[str]:
    """Inspect HTTPS response headers for security misconfigurations.

    Args:
        domain: The domain to check.

    Returns:
        List[str]: List of missing or insecure security headers.
    """
    Logger.run(f"Running Security Header Inspection for {domain}")
    findings = []
    url = f"https://{domain}"
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        security_headers = {
            "Strict-Transport-Security": "Missing HSTS header",
            "Content-Security-Policy": "Missing CSP header",
            "X-Frame-Options": "Missing X-Frame-Options header (Clickjacking risk)",
            "X-Content-Type-Options": "Missing X-Content-Type-Options header",
        }

        for header, msg in security_headers.items():
            if header not in headers:
                findings.append(msg)

        Logger.success(f"Completed security checks, found {len(findings)} issues")
        return findings
    except requests.RequestException as e:
        Logger.error(f"Security checks failed: {e}")
        return ["Unable to connect via HTTPS"]
