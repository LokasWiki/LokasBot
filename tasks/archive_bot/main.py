"""
Main entry point for the archive_bot task.

Scans Arabic Wikipedia user talk pages (namespace 3) that transclude
``{{أرشفة آلية}}`` and archives their old discussion threads.

Usage::

    uv run python -m tasks.archive_bot.main --dry-run
    uv run python -m tasks.archive_bot.main --page "نقاش المستخدم:Example"
"""

import argparse
import logging
import time
from typing import List

import pywikibot

from tasks.archive_bot.config.config_loader import ArchiveBotConfig, load_config
from tasks.archive_bot.data.pywikibot_wiki_repository import PywikibotWikiRepository
from tasks.archive_bot.domain.use_cases.archive_page import ArchivePage


def setup_logging() -> None:
    """Configure logging to a file and the console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("archive_bot.log"),
            logging.StreamHandler(),
        ],
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Archive old threads from {{أرشفة آلية}} talk pages."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute without saving anything.")
    parser.add_argument("--page", help="Archive a single page title.")
    parser.add_argument("--namespace", type=int, default=None,
                        help="Override the namespace to scan.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit the number of pages to process.")
    parser.add_argument("--sleep", type=float, default=None,
                        help="Override seconds to sleep between pages.")
    return parser


def collect_titles(args: argparse.Namespace, config: ArchiveBotConfig,
                   repository: PywikibotWikiRepository) -> List[str]:
    """Return the list of page titles to process."""
    namespace = args.namespace if args.namespace is not None else config.namespace

    if args.page:
        return [args.page]

    titles = repository.get_transcluded_pages(config.template_title, namespace)
    if args.limit is not None:
        titles = titles[: args.limit]
    return titles


def main() -> None:
    """Run the archive_bot task."""
    args = build_parser().parse_args()
    setup_logging()
    logger = logging.getLogger(__name__)

    config = load_config()
    site = pywikibot.Site(config.site_code, config.site_family)
    repository = PywikibotWikiRepository(site, max_history=config.max_history)
    use_case = ArchivePage(repository, config)

    sleep = args.sleep if args.sleep is not None else config.sleep_between_pages
    titles = collect_titles(args, config, repository)

    summary = {"archived": 0, "dry_run": 0, "skipped": 0, "failed": 0}

    for index, title in enumerate(titles):
        if args.page is None and "/" in title:
            logger.info("Skip subpage: %s", title)
            continue
        if repository.is_sysop_protected(title):
            logger.info("Skip sysop-protected page: %s", title)
            continue

        logger.info("Processing %s ...", title)
        result = use_case.execute(title, dry_run=args.dry_run)
        summary[result.status] = summary.get(result.status, 0) + 1
        logger.info("  -> %s (%s)", result.status,
                    result.reason or f"{result.archived_count} sections archived")

        if not args.dry_run and sleep > 0 and index < len(titles) - 1:
            time.sleep(sleep)

    logger.info("Finished: %s", summary)


if __name__ == "__main__":
    main()
