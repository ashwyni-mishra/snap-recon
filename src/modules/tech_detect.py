"""Technology detection module for Snap-Recon."""

from typing import List

import requests
from bs4 import BeautifulSoup

from core.logger import Logger


def run(domain: str) -> List[str]:
    """Detect technologies used by a web application.

    Args:
        domain: The domain to analyze.

    Returns:
        List[str]: Detected technologies (e.g., Server, Powered-By).
    """
    Logger.run(f"Running Technology Detection for {domain}")
    techs = []
    url = f"http://{domain}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        headers = response.headers

        server = headers.get("Server")
        if server:
            techs.append(f"Server: {server}")

        x_powered_by = headers.get("X-Powered-By")
        if x_powered_by:
            techs.append(f"X-Powered-By: {x_powered_by}")

        soup = BeautifulSoup(response.text, "html.parser")
        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and generator.get("content"):
            techs.append(f"Generator: {generator.get('content')}")

        Logger.success(f"Detected {len(techs)} technologies")
        return techs
    except requests.RequestException as e:
        Logger.error(f"Technology detection failed: {e}")
        return []
