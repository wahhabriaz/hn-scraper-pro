import asyncio
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from hn_scraper import settings
from hn_scraper.scraper import scrape_pages
from hn_scraper.parser import parse_stories
from hn_scraper.dedup import deduplicate
from hn_scraper.storage import save_json, save_csv, save_sqlite

console = Console()


async def _run(pages: int, formats: list[str], no_dedup: bool) -> None:
    all_stories = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scraping Hacker News...", total=pages)
        async for html in scrape_pages(max_pages=pages):
            stories = parse_stories(html)
            all_stories.extend(stories)
            progress.advance(task)

    if not no_dedup:
        all_stories = deduplicate(all_stories)

    console.print(f"\n[green]✓[/green] Collected [bold]{len(all_stories)}[/bold] stories\n")

    if "json" in formats:
        save_json(all_stories)
    if "csv" in formats:
        save_csv(all_stories)
    if "sqlite" in formats:
        save_sqlite(all_stories)

    # Pretty preview table
    table = Table(title="Top 10 Stories", show_lines=False, highlight=True)
    table.add_column("Rank", style="dim", width=5)
    table.add_column("Title", min_width=40)
    table.add_column("Points", justify="right")
    table.add_column("Author", style="cyan")
    table.add_column("Domain", style="dim")

    for s in sorted(all_stories, key=lambda x: x.points, reverse=True)[:10]:
        table.add_row(str(s.rank), s.title[:60], str(s.points), s.author, s.domain or "")

    console.print(table)


@click.command()
@click.option("--pages", "-p", default=settings.max_pages, show_default=True,
              help="Number of HN pages to scrape.")
@click.option("--format", "-f", "formats", multiple=True,
              type=click.Choice(["json", "csv", "sqlite"], case_sensitive=False),
              default=["json", "csv", "sqlite"], show_default=True,
              help="Output format(s). Repeatable.")
@click.option("--no-dedup", is_flag=True, default=False,
              help="Disable deduplication.")
@click.version_option("0.1.0", prog_name="hn-scraper")
def main(pages: int, formats: tuple[str, ...], no_dedup: bool) -> None:
    """HN Scraper Pro — async Hacker News data pipeline."""
    console.rule("[bold]HN Scraper Pro[/bold]")
    asyncio.run(_run(pages, list(formats), no_dedup))