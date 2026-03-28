# hn-scraper-pro

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Async](https://img.shields.io/badge/async-aiohttp-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> A production-grade async web scraper for Hacker News with rate limiting,
> deduplication, Pydantic validation, and multi-format export.

## Features

- Async HTTP with `aiohttp` and configurable rate limiting
- HTML parsing with `BeautifulSoup4` + `Pydantic v2` validation
- SHA-256 fingerprint deduplication across runs
- Export to JSON, CSV, and SQLite
- Rich CLI with live progress bar and results table
- Rotating file + console logging
- Fully tested with `pytest`

## Quick start

```bash
git clone https://github.com/wahhabriaz/hn-scraper-pro
cd hn-scraper-pro
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
hn-scraper --pages 3 --format json --format csv
```

## CLI options

| Option       | Default | Description         |
| ------------ | ------- | ------------------- |
| `--pages`    | 3       | Pages to scrape     |
| `--format`   | all     | json / csv / sqlite |
| `--no-dedup` | off     | Skip deduplication  |

## Project structure

src/hn_scraper/
├── cli.py # Click CLI entry point
├── scraper.py # Async HTTP engine
├── parser.py # BeautifulSoup HTML parser
├── models.py # Pydantic v2 data models
├── dedup.py # SHA-256 deduplication
├── storage.py # JSON / CSV / SQLite writer
└── logger.py # Rich + rotating file logger
