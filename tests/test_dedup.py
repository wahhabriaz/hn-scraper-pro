import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from hn_scraper.models import Story
from hn_scraper.dedup import deduplicate


def _story(n: int) -> Story:
    return Story(
        id=n, rank=n, title=f"Story {n}", url="https://example.com",
        domain="example.com", points=10, author="user",
        comments=5, scraped_at=datetime.now(tz=timezone.utc),
    )


@patch("hn_scraper.dedup._load_seen", return_value=set())
@patch("hn_scraper.dedup._save_seen")
def test_dedup_removes_duplicates(mock_save, mock_load):
    stories = [_story(1), _story(1), _story(2)]
    result = deduplicate(stories)
    assert len(result) == 2


@patch("hn_scraper.dedup._load_seen", return_value=set())
@patch("hn_scraper.dedup._save_seen")
def test_dedup_all_unique(mock_save, mock_load):
    stories = [_story(i) for i in range(5)]
    result = deduplicate(stories)
    assert len(result) == 5