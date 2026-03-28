import json
from pathlib import Path
from hn_scraper.models import Story
from hn_scraper.logger import get_logger

log = get_logger(__name__)

SEEN_FILE = Path("data/.seen_fingerprints.json")


def _load_seen() -> set[str]:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def _save_seen(seen: set[str]) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2))


def deduplicate(stories: list[Story]) -> list[Story]:
    seen = _load_seen()
    unique: list[Story] = []

    for story in stories:
        fp = story.fingerprint()
        if fp not in seen:
            unique.append(story)
            seen.add(fp)

    dupes = len(stories) - len(unique)
    if dupes:
        log.info(f"Deduplicator: dropped {dupes} duplicate(s)")

    _save_seen(seen)
    log.info(f"Deduplicator: {len(unique)} unique stories retained")
    return unique