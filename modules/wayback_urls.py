"""Historical URL discovery module via Wayback Machine for Snap-Recon."""

from typing import List

import requests

from core.logger import Logger


def run(domain: str, limit: int = 100) -> List[str]:
    """Fetch historical URLs for a domain from the Wayback Machine.

    Args:
        domain: The domain to search.
        limit: Maximum number of URLs to fetch.

    Returns:
        List[str]: List of unique historical URLs found.
    """
    Logger.run(f"Fetching URLs from Wayback Machine for {domain}")
    try:
        url = (
            f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*"
            f"&output=json&collapse=urlkey&limit={limit}"
        )
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                urls = list(set([row[2] for row in data[1:]]))
                Logger.success(f"Discovered {len(urls)} historical URLs")
                return urls
            Logger.warning("No historical URLs found")
            return []
        Logger.error(f"Wayback request failed: HTTP {response.status_code}")
        return []
    except Exception as e:
        Logger.error(f"Wayback Machine lookup failed: {e}")
        return []
