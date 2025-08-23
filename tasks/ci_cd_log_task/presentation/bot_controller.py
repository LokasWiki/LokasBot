"""
Presentation layer for the CI/CD Log Task.

This module provides the main controller that orchestrates the entire
workflow of the CI/CD log task, following the Clean Architecture principles.
"""

import logging
import os
from typing import Dict, Any
from tasks.ci_cd_log_task.domain.entities.bot_log import BotLog
from tasks.ci_cd_log_task.domain.use_cases.fetch_commit_data import FetchCommitData
from tasks.ci_cd_log_task.domain.use_cases.fetch_contributors import FetchContributors
from tasks.ci_cd_log_task.domain.use_cases.create_log_message import CreateLogMessage


class BotController:
    """
    Main controller for the CI/CD Log Task.

    This class orchestrates the entire workflow, coordinating between
    use cases and handling configuration and errors.
    """

    def __init__(
        self,
        fetch_commit_data: FetchCommitData,
        fetch_contributors: FetchContributors,
        create_log_message: CreateLogMessage,
        wiki_operations
    ):
        """
        Initialize the BotController with dependencies.

        Args:
            fetch_commit_data (FetchCommitData): Use case for fetching commit data
            fetch_contributors (FetchContributors): Use case for fetching contributors
            create_log_message (CreateLogMessage): Use case for creating log messages
            wiki_operations: Wiki operations repository (injected at runtime)
        """
        self.fetch_commit_data = fetch_commit_data
        self.fetch_contributors = fetch_contributors
        self.create_log_message = create_log_message
        self.wiki_operations = wiki_operations
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.config = {}
        self._load_configuration()

    def _load_configuration(self):
        """
        Load configuration from environment variables.
        """
        self.config = {
            # 'tool_name': os.getenv('LOGNAME', 'غير متوفر'),
            'tool_name': 'LokasBot',
            'bot_version': '1.0.0',  # Could be made configurable
            'repo_owner': 'LokasWiki',  # Could be made configurable
            'repo_name': 'LokasBot',  # Could be made configurable
            'branch': 'main',  # Could be made configurable
            'site_name': 'ar'  # Could be made configurable
        }

        self.logger.info("Configuration loaded successfully")

    def run(self) -> Dict[str, Any]:
        """
        Execute the complete CI/CD log workflow.

        Returns:
            Dict[str, Any]: Result containing success status and details
        """
        result = {
            'success': False,
            'commit_info': None,
            'contributors': None,
            'bot_log': None,
            'errors': []
        }

        try:
            self.logger.info("Starting CI/CD log workflow")

            # Step 1: Fetch commit data
            self.logger.info("Step 1: Fetching commit data")
            commit_info = self.fetch_commit_data.execute(
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name'],
                branch=self.config['branch']
            )
            result['commit_info'] = commit_info

            # Step 2: Fetch contributors
            self.logger.info("Step 2: Fetching contributors")
            contributors = self.fetch_contributors.execute(
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name']
            )
            result['contributors'] = contributors

            # Step 3: Create log message
            self.logger.info("Step 3: Creating log message")
            bot_log = self.create_log_message.execute(
                tool_name=self.config['tool_name'],
                bot_version=self.config['bot_version'],
                commit_info=commit_info,
                contributors=contributors
            )
            result['bot_log'] = bot_log

            # Step 4: Save to wiki
            self.logger.info("Step 4: Saving log message to wiki")
            self.wiki_operations.save_log_message(bot_log)

            result['success'] = True
            self.logger.info("CI/CD log workflow completed successfully")

        except Exception as e:
            error_msg = f"CI/CD log workflow failed: {str(e)}"
            self.logger.error(error_msg)
            result['errors'].append(error_msg)

        return result

    def run_with_error_handling(self) -> Dict[str, Any]:
        """
        Execute the workflow with detailed error handling and reporting.

        Returns:
            Dict[str, Any]: Detailed result with error information
        """
        result = {
            'success': False,
            'step_results': {},
            'warnings': [],
            'errors': []
        }

        try:
            # Step 1: Fetch commit data with error info
            commit_info, commit_error = self.fetch_commit_data.execute_with_fallback(
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name'],
                branch=self.config['branch']
            )

            result['step_results']['commit_data'] = {
                'success': commit_error is None,
                'data': commit_info,
                'error': commit_error
            }

            if commit_error:
                result['warnings'].append(f"Commit data: {commit_error}")

            # Step 2: Fetch contributors with error info
            contributors, contributors_error = self.fetch_contributors.execute_with_fallback(
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name']
            )

            result['step_results']['contributors'] = {
                'success': contributors_error is None,
                'data': contributors,
                'error': contributors_error
            }

            if contributors_error:
                result['warnings'].append(f"Contributors: {contributors_error}")

            # Step 3: Create log message with validation
            bot_log, warnings = self.create_log_message.execute_with_validation(
                tool_name=self.config['tool_name'],
                bot_version=self.config['bot_version'],
                commit_info=commit_info,
                contributors=contributors
            )

            result['step_results']['log_message'] = {
                'success': True,
                'data': bot_log,
                'warnings': warnings
            }

            result['warnings'].extend(warnings)

            # Step 4: Save to wiki (with error handling)
            try:
                self.wiki_operations.save_log_message(bot_log)
                result['step_results']['wiki_save'] = {
                    'success': True,
                    'message': 'Log message saved successfully'
                }
                result['success'] = True

            except Exception as e:
                error_msg = f"Failed to save to wiki: {str(e)}"
                result['step_results']['wiki_save'] = {
                    'success': False,
                    'error': error_msg
                }
                result['errors'].append(error_msg)

        except Exception as e:
            error_msg = f"Unexpected error in workflow: {str(e)}"
            result['errors'].append(error_msg)
            self.logger.error(error_msg)

        return result

    def get_configuration(self) -> Dict[str, str]:
        """
        Get the current configuration.

        Returns:
            Dict[str, str]: Current configuration values
        """
        return self.config.copy()

    def update_configuration(self, **kwargs):
        """
        Update configuration values.

        Args:
            **kwargs: Configuration key-value pairs to update
        """
        self.config.update(kwargs)
        self.logger.info(f"Configuration updated: {kwargs}")