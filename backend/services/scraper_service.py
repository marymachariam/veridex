import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("veridex.scraper")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def scrape_page_text(url: str, max_chars: int = 6000) -> str:
    """Fetches a URL and returns cleaned visible text, trimmed to max_chars."""
    if not url.startswith("http"):
        url = f"https://{url}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Scrape failed for %s: %s", url, exc)
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "svg", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return text[:max_chars]


def scrape_competitor_pages(website: str) -> str:
    """Scrapes the homepage and a guessed pricing page, combines the text."""
    if not website:
        return ""

    domain = website.replace("https://", "").replace("http://", "").rstrip("/")
    combined = []

    homepage_text = scrape_page_text(f"https://{domain}")
    if homepage_text:
        combined.append(f"HOMEPAGE CONTENT:\n{homepage_text}")

    for path in ["/pricing", "/plans", "/price"]:
        pricing_text = scrape_page_text(f"https://{domain}{path}", max_chars=4000)
        if pricing_text:
            combined.append(f"PRICING PAGE ({path}) CONTENT:\n{pricing_text}")
            break  # stop at the first pricing-like page that actually returns content

    return "\n\n".join(combined)