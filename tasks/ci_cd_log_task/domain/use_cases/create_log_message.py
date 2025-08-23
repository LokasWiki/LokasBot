"""
Use case for creating bot log messages.

This use case encapsulates the business logic for creating
formatted bot log messages, following the Clean Architecture principles.
"""

import logging
from typing import List
from tasks.ci_cd_log_task.domain.entities.commit_info import CommitInfo
from tasks.ci_cd_log_task.domain.entities.bot_log import BotLog


class CreateLogMessage:
    """
    Use case for creating bot log messages.

    This class contains the business logic for creating formatted bot log messages
    with all necessary information including commit data and contributors.
    """

    def __init__(self):
        """
        Initialize the CreateLogMessage use case.

        This use case doesn't require external dependencies as it only
        formats data into the BotLog entity.
        """
        self.logger = logging.getLogger(__name__)

    def execute(
        self,
        tool_name: str,
        bot_version: str,
        commit_info: CommitInfo,
        contributors: List[str],
        timestamp: str = None
    ) -> BotLog:
        """
        Execute the use case to create a bot log message.

        Args:
            tool_name (str): Name of the tool/bot
            bot_version (str): Version of the bot
            commit_info (CommitInfo): Commit information
            contributors (List[str]): List of contributors
            timestamp (str, optional): Current timestamp, defaults to current time

        Returns:
            BotLog: Formatted bot log message
        """
        try:
            self.logger.info(f"Creating log message for tool: {tool_name}")

            bot_log = BotLog(
                tool_name=tool_name,
                bot_version=bot_version,
                commit_info=commit_info,
                contributors=contributors,
                timestamp=timestamp
            )

            self.logger.info("Successfully created log message")
            return bot_log

        except Exception as e:
            error_msg = f"Failed to create log message: {str(e)}"
            self.logger.error(error_msg)
            raise

    def execute_with_validation(
        self,
        tool_name: str,
        bot_version: str,
        commit_info: CommitInfo,
        contributors: List[str],
        timestamp: str = None
    ) -> tuple[BotLog, List[str]]:
        """
        Execute the use case with validation and return warnings.

        Args:
            tool_name (str): Name of the tool/bot
            bot_version (str): Version of the bot
            commit_info (CommitInfo): Commit information
            contributors (List[str]): List of contributors
            timestamp (str, optional): Current timestamp, defaults to current time

        Returns:
            tuple[BotLog, List[str]]: Bot log and list of warnings
        """
        warnings = []

        # Validate inputs
        if not tool_name or tool_name.strip() == "":
            warnings.append("Tool name is empty")

        if not bot_version or bot_version.strip() == "":
            warnings.append("Bot version is empty")

        if commit_info.commit_message == "غير متوفر":
            warnings.append("Commit information is not available")

        if not contributors or len(contributors) == 0:
            warnings.append("No contributors found")
        elif contributors == ["غير متوفر"]:
            warnings.append("Contributors information is not available")

        try:
            bot_log = BotLog(
                tool_name=tool_name,
                bot_version=bot_version,
                commit_info=commit_info,
                contributors=contributors,
                timestamp=timestamp
            )
            return bot_log, warnings

        except Exception as e:
            error_msg = f"Failed to create log message: {str(e)}"
            self.logger.error(error_msg)
            raise