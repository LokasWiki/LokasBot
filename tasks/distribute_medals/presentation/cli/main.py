"""
Main CLI entry point for medal distribution system.

This module provides the command-line interface for the medal distribution
application, supporting both production and testing modes.
"""

import logging
import sys
from typing import List

import pywikibot
from tasks.distribute_medals.presentation.controllers.medal_controller import MedalController
from tasks.distribute_medals.domain.entities.medal import Medal


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_test_medal() -> Medal:
    """
    Create a test medal configuration.

    Returns:
        Medal: Test medal configuration
    """
    return Medal(
        number=150000,
        query="""select 'Dr-Taher' as 'actor_name', 150000 as 'sum_yc', 150000 as 'sum_tc' from actor limit 1""",
        template_stub="{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}",
        description="Test medal for 150,000 edits"
    )


def run_test_mode() -> int:
    """
    Run the application in test mode.

    Returns:
        int: Exit code
    """
    print("Running in TEST mode...")

    try:
        # Initialize controller
        controller = MedalController()

        # Test system components
        print("Testing system components...")
        test_results = controller.test_system()

        if not test_results['overall_success']:
            print("❌ System tests failed!")
            for error in test_results['errors']:
                print(f"  - {error}")
            return 1

        print("✅ All system tests passed!")

        # Create test medal
        medal = create_test_medal()

        # Run distribution
        print(f"Running test distribution for medal {medal.number}...")
        result = controller.distribute_medal(medal)

        if result['success']:
            print("✅ Test distribution completed successfully!")
            print(f"   Distributed: {result.get('distributed_count', 0)}")
            print(f"   Skipped: {result.get('skipped_count', 0)}")
        else:
            print("❌ Test distribution failed!")
            for error in result.get('errors', []):
                print(f"  - {error}")
            return 1

        # Cleanup
        controller.cleanup()

        return 0

    except Exception as e:
        print(f"❌ Test mode failed: {str(e)}")
        logging.exception(e)
        return 1


def run_production_mode() -> int:
    """
    Run the application in production mode.

    Returns:
        int: Exit code
    """
    print("Running in PRODUCTION mode...")

    try:
        # For now, we'll use the existing data structure
        # TODO: Migrate to configuration-based approach
        from tasks.distribute_medals.data import list_of_distribute_medals

        # Initialize controller
        controller = MedalController()

        # Test system before starting
        print("Testing system components...")
        test_results = controller.test_system()

        if not test_results['overall_success']:
            print("❌ System tests failed! Cannot proceed in production mode.")
            for error in test_results['errors']:
                print(f"  - {error}")
            return 1

        print("✅ All system tests passed!")

        # Process each medal
        total_distributed = 0
        total_skipped = 0

        for medal_data in list_of_distribute_medals:
            try:
                print(f"Processing medal {medal_data['number']}...")

                # Create medal entity
                medal = Medal(
                    number=medal_data['number'],
                    query=medal_data['query'],
                    template_stub=medal_data['template_stub']
                )

                # Distribute medal
                result = controller.distribute_medal(medal)

                if result['success']:
                    distributed = result.get('distributed_count', 0)
                    skipped = result.get('skipped_count', 0)
                    total_distributed += distributed
                    total_skipped += skipped

                    print(f"  ✅ Medal {medal.number}: {distributed} distributed, {skipped} skipped")
                else:
                    print(f"  ❌ Medal {medal.number}: Failed")
                    for error in result.get('errors', []):
                        print(f"    - {error}")

            except Exception as e:
                print(f"  ❌ Medal {medal_data['number']}: Error - {str(e)}")
                logging.exception(e)

        print("\n📊 Production run completed!")
        print(f"   Total distributed: {total_distributed}")
        print(f"   Total skipped: {total_skipped}")

        # Cleanup
        controller.cleanup()

        return 0

    except Exception as e:
        print(f"❌ Production mode failed: {str(e)}")
        logging.exception(e)
        return 1


def main(*args: str) -> int:
    """
    Main entry point for the medal distribution application.

    Args:
        *args: Command line arguments

    Returns:
        int: Exit code
    """
    setup_logging()

    # Check if running in test mode
    if '--test' in args or len(sys.argv) > 1 and sys.argv[1] == '--test':
        return run_test_mode()
    else:
        return run_production_mode()


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))