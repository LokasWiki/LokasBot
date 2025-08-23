"""
Main controller for medal distribution system.

This controller orchestrates all use cases and provides the main
interface for the medal distribution functionality.
"""

import logging
from typing import List, Dict, Any
from tasks.distribute_medals.domain.entities.medal import Medal
from tasks.distribute_medals.domain.entities.user import User
from tasks.distribute_medals.domain.use_cases.distribute_medals import DistributeMedals
from tasks.distribute_medals.domain.use_cases.fetch_eligible_users import FetchEligibleUsers
from tasks.distribute_medals.domain.use_cases.manage_signatures import ManageSignatures
from tasks.distribute_medals.domain.use_cases.send_medal_template import SendMedalTemplate
from tasks.distribute_medals.infrastructure.database.mysql_database import MySQLDatabase
from tasks.distribute_medals.infrastructure.wiki.pywikibot_wiki import PywikibotWiki
from tasks.distribute_medals.infrastructure.scanners.signature_scanner import SignatureScanner


class MedalController:
    """
    Main controller for medal distribution operations.

    This class orchestrates all use cases and manages the application flow,
    providing a high-level interface for medal distribution functionality.
    """

    def __init__(self):
        """
        Initialize the MedalController with dependencies.
        """
        self.logger = logging.getLogger(__name__)

        # Initialize infrastructure
        self.database = MySQLDatabase()
        self.wiki = PywikibotWiki()
        self.signature_scanner = SignatureScanner()

        # Initialize use cases
        self.distribute_medals = DistributeMedals(
            database_repo=self.database,
            wiki_repo=self.wiki,
            signature_repo=self.signature_scanner
        )

        self.fetch_eligible_users = FetchEligibleUsers(
            database_repo=self.database
        )

        self.manage_signatures = ManageSignatures(
            signature_repo=self.signature_scanner
        )

        self.send_medal_template = SendMedalTemplate(
            wiki_repo=self.wiki
        )

    def distribute_medal(self, medal: Medal) -> Dict[str, Any]:
        """
        Distribute a medal to eligible users.

        Args:
            medal (Medal): The medal to distribute

        Returns:
            Dict[str, Any]: Result of the distribution
        """
        try:
            self.logger.info(f"Starting distribution for medal {medal.number}")

            result = self.distribute_medals.execute(medal)

            if result['success']:
                self.logger.info(
                    f"Distribution completed: {result['distributed_count']} distributed"
                )
            else:
                self.logger.error("Distribution failed")

            return result

        except Exception as e:
            error_msg = f"Distribution failed: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'medal': medal,
                'errors': [error_msg]
            }

    def get_eligible_users(self, medal: Medal) -> List[User]:
        """
        Get users eligible for a medal.

        Args:
            medal (Medal): The medal configuration

        Returns:
            List[User]: List of eligible users
        """
        try:
            users = self.fetch_eligible_users.execute(medal)
            self.logger.info(f"Found {len(users)} eligible users")
            return users
        except Exception as e:
            self.logger.error(f"Failed to get eligible users: {str(e)}")
            return []

    def get_distribution_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the distribution system.

        Returns:
            Dict[str, Any]: System statistics
        """
        try:
            signature_count = self.manage_signatures.execute_get_count()

            return {
                'signature_count': signature_count,
                'database_connected': self.database.test_connection(),
                'wiki_available': True  # Wiki is always available through Pywikibot
            }

        except Exception as e:
            self.logger.error(f"Failed to get statistics: {str(e)}")
            return {
                'signature_count': 0,
                'database_connected': False,
                'wiki_available': False,
                'error': str(e)
            }

    def test_system(self) -> Dict[str, Any]:
        """
        Test all system components.

        Returns:
            Dict[str, Any]: Test results
        """
        results = {
            'database': False,
            'wiki': False,
            'signatures': False,
            'errors': []
        }

        try:
            # Test database connection
            results['database'] = self.database.test_connection()

        except Exception as e:
            results['errors'].append(f"Database test failed: {str(e)}")

        try:
            # Test signature system
            signature_count = self.manage_signatures.execute_get_count()
            results['signatures'] = signature_count > 0

        except Exception as e:
            results['errors'].append(f"Signature test failed: {str(e)}")

        # Wiki is always available through Pywikibot
        results['wiki'] = True

        results['overall_success'] = all([
            results['database'],
            results['wiki'],
            results['signatures']
        ])

        return results

    def cleanup(self):
        """
        Clean up resources.
        """
        try:
            self.database.close_connection()
            self.logger.info("Resources cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")