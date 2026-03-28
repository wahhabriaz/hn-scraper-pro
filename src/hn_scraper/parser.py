from datetime import datetime, timezone
from bs4 import BeautifulSoup
from hn_scraper.models import Story
from hn_scraper.logger import get_logger

log = get_logger(__name__)


def _safe_int(text: str | None, default: int = 0) -> int:
    if not text:
        return default
    digits = "".join(c for c in text if c.isdigit())
    return int(digits) if digits else default


def _extract_domain(url: str | None) -> str | None:
    if not url:
        return None
    from urllib.parse import urlparse
    try:
        return urlparse(url).netloc.lstrip("www.")
    except Exception:
        return None


def parse_stories(html: str) -> list[Story]:
    soup = BeautifulSoup(html, "html.parser")
    stories: list[Story] = []
    now = datetime.now(tz=timezone.utc)

    # HN uses .athing for story rows
    for row in soup.select("tr.athing"):
        try:
            story_id = int(row.get("id", 0))
            rank_el = row.select_one(".rank")
            rank = _safe_int(rank_el.text if rank_el else "0")

            title_el = row.select_one(".titleline > a")
            if not title_el:
                continue
            title = title_el.text
            url = title_el.get("href")
            domain = _extract_domain(url)

            # Sub-row carries score/author/comments
            sub = row.find_next_sibling("tr")
            score_el = sub.select_one(".score") if sub else None
            author_el = sub.select_one(".hnuser") if sub else None
            comments_el = sub.select(".subline a")[-1] if sub else None

            story = Story(
                id=story_id,
                rank=rank,
                title=title,
                url=url,
                domain=domain,
                points=_safe_int(score_el.text if score_el else None),
                author=author_el.text if author_el else "unknown",
                comments=_safe_int(comments_el.text if comments_el else None),
                scraped_at=now,
            )
            stories.append(story)
        except Exception as exc:
            log.warning(f"Skipping story id={row.get('id')}: {exc}")

    log.info(f"Parsed {len(stories)} stories from page")
    return stories