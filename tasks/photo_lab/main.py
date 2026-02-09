"""
Main entry point for the photo_lab task.

This module provides a clean interface to the photo lab archiving
application using Clean Architecture principles.

Usage:
    # Production mode
    python -m tasks.photo_lab.main

    # Dry run mode (test without making changes)
    python -m tasks.photo_lab.main --dry-run

    # Verbose logging
    python -m tasks.photo_lab.main --verbose
"""

import argparse
import logging
import sys
from datetime import datetime

from tasks.photo_lab.infrastructure.wiki.pywikibot_wiki import PywikibotWiki
from tasks.photo_lab.presentation.controllers.photo_lab_controller import PhotoLabController


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: If True, set log level to DEBUG
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'photo_lab_{datetime.now().strftime("%Y%m%d")}.log')
        ]
    )


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Photo Lab Archiving Bot - Archives completed photo workshop requests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tasks.photo_lab.main              # Run in production mode
  python -m tasks.photo_lab.main --dry-run    # Test without making changes
  python -m tasks.photo_lab.main --verbose    # Enable debug logging
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry mode without making any changes to the wiki'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose (debug) logging'
    )
    
    return parser.parse_args()


def print_results(results: dict) -> None:
    """
    Print the results of the archiving operation.
    
    Args:
        results: Dictionary containing operation results
    """
    print("\n" + "=" * 50)
    print("PHOTO LAB ARCHIVING RESULTS")
    print("=" * 50)
    
    print(f"\nSuccess: {'Yes' if results['success'] else 'No'}")
    print(f"Total Requests Found: {results['total_requests']}")
    print(f"Requests Ready for Archive: {results['archivable_requests']}")
    
    if results.get('archive_page_number'):
        print(f"Archive Page Used: ويكيبيديا:ورشة الصور/أرشيف {results['archive_page_number']}")
    
    print(f"\nArchived: {len(results['archived'])}")
    for page_name in results['archived']:
        print(f"  ✓ {page_name}")
    
    if results['failed']:
        print(f"\nFailed: {len(results['failed'])}")
        for page_name in results['failed']:
            print(f"  ✗ {page_name}")
    
    if results['skipped']:
        print(f"\nSkipped: {len(results['skipped'])}")
        for page_name in results['skipped']:
            print(f"  - {page_name}")
    
    if results.get('errors'):
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  ! {error}")
    
    print("\n" + "=" * 50)


def main() -> int:
    """
    Main entry point for the photo lab task.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("Photo Lab Archiving Bot started")
    logger.info(f"Mode: {'Dry Run' if args.dry_run else 'Production'}")
    
    try:
        # Initialize the wiki repository
        logger.info("Initializing wiki repository...")
        wiki_repository = PywikibotWiki()
        
        # Initialize the controller
        controller = PhotoLabController(wiki_repository)
        
        # Run the workflow
        if args.dry_run:
            results = controller.run_dry_mode()
        else:
            results = controller.run()
        
        # Print results
        print_results(results)
        
        # Return appropriate exit code
        if results['success']:
            logger.info("Photo Lab Archiving Bot completed successfully")
            return 0
        else:
            logger.warning("Photo Lab Archiving Bot completed with errors")
            return 1
            
    except Exception as e:
        logger.exception("Fatal error occurred")
        print(f"\nFatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
