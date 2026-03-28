import asyncio
import aiohttp
from typing import AsyncIterator
from hn_scraper import settings
from hn_scraper.logger import get_logger

log = get_logger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; HNScraperPro/1.0; "
        "+https://github.com/yourhandle/hn-scraper-pro)"
    )
}


async def fetch_page(session: aiohttp.ClientSession, page: int) -> str | None:
    url = settings.base_url if page == 1 else f"{settings.base_url}/news?p={page}"
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
            r.raise_for_status()
            log.info(f"Fetched page {page} → HTTP {r.status}")
            return await r.text()
    except aiohttp.ClientError as exc:
        log.error(f"Failed to fetch page {page}: {exc}")
        return None


async def scrape_pages(max_pages: int | None = None) -> AsyncIterator[str]:
    """Yields raw HTML for each page with rate-limiting between requests."""
    pages = max_pages or settings.max_pages

    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        for page in range(1, pages + 1):
            html = await fetch_page(session, page)
            if html:
                yield html
            if page < pages:
                log.debug(f"Rate limit: sleeping {settings.rate_limit}s")
                await asyncio.sleep(settings.rate_limit)