import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from hn_scraper.models import Story
from hn_scraper.logger import get_logger
from hn_scraper import settings

log = get_logger(__name__)


def _output_dir() -> Path:
    p = Path(settings.output_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(stories: list[Story], filename: str = "stories.json") -> Path:
    path = _output_dir() / filename
    data = [s.model_dump(mode="json") for s in stories]
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    log.info(f"JSON → {path} ({len(stories)} records)")
    return path


def save_csv(stories: list[Story], filename: str = "stories.csv") -> Path:
    path = _output_dir() / filename
    if not stories:
        return path
    fields = list(stories[0].model_fields.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in stories:
            writer.writerow(s.model_dump(mode="json"))
    log.info(f"CSV  → {path} ({len(stories)} records)")
    return path


def save_sqlite(stories: list[Story], db_name: str = "scraper.db") -> Path:
    path = _output_dir() / db_name
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            rank INTEGER,
            title TEXT NOT NULL,
            url TEXT,
            domain TEXT,
            points INTEGER DEFAULT 0,
            author TEXT,
            comments INTEGER DEFAULT 0,
            scraped_at TEXT
        )
    """)
    cur.executemany(
        """INSERT OR REPLACE INTO stories
           (id, rank, title, url, domain, points, author, comments, scraped_at)
           VALUES (:id, :rank, :title, :url, :domain, :points, :author, :comments, :scraped_at)""",
        [s.model_dump(mode="json") for s in stories],
    )
    conn.commit()
    conn.close()
    log.info(f"SQLite → {path} ({len(stories)} records)")
    return path