"""
Main application entry point for the CI/CD Log Task.

This module provides the main application entry point that sets up
all dependencies and runs the CI/CD log task using clean architecture principles.
"""

import logging
import sys
from tasks.ci_cd_log_task.infrastructure.github_api import GitHubAPI
from tasks.ci_cd_log_task.infrastructure.wiki_operations import WikiOperations
from tasks.ci_cd_log_task.domain.use_cases.fetch_commit_data import FetchCommitData
from tasks.ci_cd_log_task.domain.use_cases.fetch_contributors import FetchContributors
from tasks.ci_cd_log_task.domain.use_cases.create_log_message import CreateLogMessage
from tasks.ci_cd_log_task.presentation.bot_controller import BotController


def setup_logging():
    """
    Set up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_application() -> BotController:
    """
    Create and configure the application with all dependencies.

    Returns:
        BotController: Configured bot controller instance
    """
    # Create infrastructure layer instances
    github_api = GitHubAPI()
    wiki_operations = WikiOperations()

    # Create use case instances with dependencies
    fetch_commit_data = FetchCommitData(github_repository=github_api)
    fetch_contributors = FetchContributors(github_repository=github_api)
    create_log_message = CreateLogMessage()

    # Create presentation layer instance
    bot_controller = BotController(
        fetch_commit_data=fetch_commit_data,
        fetch_contributors=fetch_contributors,
        create_log_message=create_log_message,
        wiki_operations=wiki_operations
    )

    return bot_controller


def main():
    """
    Main application entry point.
    """
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting CI/CD Log Task Application")

        # Create and configure application
        logger.info("Initializing application components")
        bot_controller = create_application()

        # Display configuration
        config = bot_controller.get_configuration()
        logger.info("Application configuration:")
        for key, value in config.items():
            logger.info(f"  {key}: {value}")

        # Run the application
        logger.info("Running CI/CD log workflow")
        result = bot_controller.run()

        # Handle results
        if result['success']:
            logger.info("✅ CI/CD log workflow completed successfully!")

            # Log details
            if result['commit_info']:
                logger.info(f"📝 Commit: {result['commit_info'].commit_message[:50]}...")

            if result['contributors']:
                logger.info(f"👥 Contributors: {len(result['contributors'])}")

            if result['bot_log']:
                logger.info(f"📄 Log saved to: {result['bot_log'].get_page_title()}")

        else:
            logger.error("❌ CI/CD log workflow failed!")
            for error in result['errors']:
                logger.error(f"  Error: {error}")

            # Exit with error code
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("🛑 Application interrupted by user")
        sys.exit(130)

    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)


def main_with_detailed_reporting():
    """
    Main application entry point with detailed error reporting.
    """
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting CI/CD Log Task Application (detailed mode)")

        # Create and configure application
        logger.info("Initializing application components")
        bot_controller = create_application()

        # Display configuration
        config = bot_controller.get_configuration()
        logger.info("Application configuration:")
        for key, value in config.items():
            logger.info(f"  {key}: {value}")

        # Run the application with detailed reporting
        logger.info("Running CI/CD log workflow with detailed reporting")
        result = bot_controller.run_with_error_handling()

        # Handle detailed results
        if result['success']:
            logger.info("✅ CI/CD log workflow completed successfully!")

            # Log step results
            for step, step_result in result['step_results'].items():
                if step_result['success']:
                    logger.info(f"✅ {step}: Success")
                else:
                    logger.warning(f"⚠️  {step}: {step_result.get('error', 'Unknown error')}")

        else:
            logger.error("❌ CI/CD log workflow failed!")

            # Log errors
            for error in result['errors']:
                logger.error(f"  ❌ Error: {error}")

            # Log warnings
            for warning in result['warnings']:
                logger.warning(f"  ⚠️  Warning: {warning}")

            # Log step results
            for step, step_result in result['step_results'].items():
                if step_result['success']:
                    logger.info(f"✅ {step}: Success")
                else:
                    logger.error(f"❌ {step}: {step_result.get('error', 'Unknown error')}")

            # Exit with error code
            sys.exit(1)

        # Log warnings even if successful
        if result['warnings']:
            logger.warning("⚠️  Workflow completed with warnings:")
            for warning in result['warnings']:
                logger.warning(f"  ⚠️  {warning}")

    except KeyboardInterrupt:
        logger.info("🛑 Application interrupted by user")
        sys.exit(130)

    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--detailed":
        main_with_detailed_reporting()
    else:
        main()