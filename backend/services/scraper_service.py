import ipaddress
import logging
import re
import socket
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from core.config import settings

logger = logging.getLogger("veridex.scraper")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
MAX_REDIRECTS = 3


LIMITS = {"homepage": 1500, "pricing": 4500, "features": 2000, "about": 1000, "updates": 1000}


KEYWORDS = {
    "pricing": ["pricing", "plans", "price"],
    "features": ["features", "product", "platform"],
    "about": ["about", "about-us", "company"],
    "updates": ["changelog", "release-notes", "whats-new", "blog"],
}


FALLBACK_PATHS = {
    "pricing": ["/pricing", "/plans", "/price"],
    "features": ["/features", "/product"],
    "about": ["/about", "/company"],
    "updates": ["/changelog", "/blog"],
}

SECTION_TITLES = {
    "homepage": "HOMEPAGE",
    "pricing": "PRICING PAGE",
    "features": "FEATURES / PRODUCT PAGE",
    "about": "ABOUT PAGE",
    "updates": "CHANGELOG / BLOG PAGE",
}

_HOST_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$")


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------

def _normalize_domain(website: str) -> str:
    """Returns a clean domain like 'notion.so', or '' if the input isn't a valid public hostname."""
    if not website:
        return ""
    raw = website.strip().lower()
    if "://" not in raw:
        raw = "https://" + raw
    host = (urlparse(raw).hostname or "").strip(".")
    if host.startswith("www."):
        host = host[4:]
    return host if _HOST_RE.match(host) else ""


def _is_public_host(host: str) -> bool:
    """Blocks localhost, private networks and cloud metadata addresses (SSRF protection)."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        try:
            if not ipaddress.ip_address(info[4][0]).is_global:
                return False
        except ValueError:
            return False
    return True


def _safe_get(url: str) -> Optional[requests.Response]:
    """GET that checks every hop (including redirects) is a public address."""
    for _ in range(MAX_REDIRECTS + 1):
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or not _is_public_host(parsed.hostname):
            logger.warning("Blocked unsafe URL: %s", url)
            return None
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=False)
        except requests.RequestException as exc:
            logger.warning("Fetch failed for %s: %s", url, exc)
            return None

        if resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("Location")
            if not location:
                return None
            url = urljoin(url, location)
            continue
        if resp.status_code >= 400:
            return None
        return resp
    return None


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "svg", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(separator=" ", strip=True).split())

def _clean(text: str) -> str:
    text = text or ""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)          
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def scrape_page_text(url: str, max_chars: int = 6000) -> str:
    """Fetches a URL with a plain request and returns cleaned visible text (no JavaScript rendering)."""
    if not url.startswith("http"):
        url = f"https://{url}"
    resp = _safe_get(url)
    if resp is None:
        return ""
    return _html_to_text(resp.text)[:max_chars]


# ---------------------------------------------------------------------------
# Page discovery and extraction
# ---------------------------------------------------------------------------

def _discover_pages(html: str, base_url: str, domain: str) -> Dict[str, str]:
    """Finds the real pricing/features/about/updates links on the homepage."""
    soup = BeautifulSoup(html, "html.parser")
    found: Dict[str, str] = {}

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        url = urljoin(base_url, href).split("#")[0]
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        if host != domain and not host.endswith("." + domain):
            continue

        path = parsed.path.lower().rstrip("/")
        label = a.get_text(" ", strip=True).lower()
        for category, words in KEYWORDS.items():
            if category in found:
                continue
            if any(path == f"/{w}" or path.endswith(f"/{w}") or label == w for w in words):
                found[category] = url
    return found


def _extract_with_tavily(urls: List[str]) -> Dict[str, str]:
    """Reads pages (including JavaScript-rendered ones) through Tavily Extract. Returns {url: text}."""
    if not settings.TAVILY_API_KEY or not urls:
        return {}
    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        response = client.extract(urls=urls, extract_depth="advanced")
    except Exception as exc:
        logger.warning("Tavily extract failed, falling back to plain requests: %s", exc)
        return {}

    return {
        item.get("url", "").rstrip("/"): item.get("raw_content") or ""
        for item in response.get("results", [])
    }


def scrape_competitor_pages(website: str) -> str:
    """Collects homepage, pricing, features, about and updates pages for a company.
    Returns labelled text, each section tagged with its source URL."""
    domain = _normalize_domain(website)
    if not domain:
        return ""

    home_url = f"https://{domain}"
    home_resp = _safe_get(home_url)
    discovered = _discover_pages(home_resp.text, home_resp.url, domain) if home_resp is not None else {}

    candidates: List[Tuple[str, str]] = [("homepage", home_url)]
    for category in ("pricing", "features", "about", "updates"):
        if category in discovered:
            candidates.append((category, discovered[category]))
        else:
            candidates.extend((category, f"{home_url}{path}") for path in FALLBACK_PATHS[category])

    extracted = _extract_with_tavily([url for _, url in candidates])

    sections: Dict[str, Tuple[str, str]] = {}
    for category, url in candidates:
        if category in sections:
            continue
        text = extracted.get(url.rstrip("/"), "")
        if not text:
            text = scrape_page_text(url, LIMITS[category])  # plain-request fallback
        text = _clean(text)[: LIMITS[category]]
        if text:
            sections[category] = (url, text)

    parts = [
        f"{SECTION_TITLES[category]} (source: {url}) CONTENT:\n{text}"
        for category, (url, text) in sections.items()
    ]
    return "\n\n".join(parts)