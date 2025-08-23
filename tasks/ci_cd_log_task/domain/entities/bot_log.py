"""
Domain entity representing bot log message for wiki.

This entity encapsulates the core data and behavior related to
bot log messages, following Domain-Driven Design principles.
"""

from datetime import datetime
from typing import List, Optional
from tasks.ci_cd_log_task.domain.entities.commit_info import CommitInfo


class BotLog:
    """
    Represents a bot log message for wiki posting.

    Attributes:
        tool_name (str): Name of the tool/bot
        bot_version (str): Version of the bot
        commit_info (CommitInfo): Commit information
        contributors (List[str]): List of contributors
        timestamp (str): Current timestamp
    """

    def __init__(
        self,
        tool_name: str,
        bot_version: str,
        commit_info: CommitInfo,
        contributors: List[str],
        timestamp: Optional[str] = None
    ):
        """
        Initialize a new BotLog entity.

        Args:
            tool_name (str): Name of the tool/bot
            bot_version (str): Version of the bot
            commit_info (CommitInfo): Commit information
            contributors (List[str]): List of contributors
            timestamp (Optional[str]): Current timestamp, defaults to current time
        """
        self.tool_name = tool_name
        self.bot_version = bot_version
        self.commit_info = commit_info
        self.contributors = contributors
        self.timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        """String representation of the BotLog entity."""
        contributor_count = len(self.contributors)
        return f"BotLog(tool='{self.tool_name}', contributors={contributor_count})"

    def __repr__(self) -> str:
        """Detailed string representation of the BotLog entity."""
        return (
            f"BotLog(tool_name='{self.tool_name}', "
            f"bot_version='{self.bot_version}', "
            f"commit_info={self.commit_info}, "
            f"contributors={self.contributors}, "
            f"timestamp='{self.timestamp}')"
        )

    def format_wiki_message(self) -> str:
        """
        Format the bot log as a wiki message.

        Returns:
            str: Formatted wiki message
        """
        # Format contributors list
        contributors_list = '\n'.join(f'* {contributor}' for contributor in self.contributors)

        # Format the complete wiki message
        message = f'''\
== إشعار تحديث البوت ({self.tool_name}) ==
مرحبًا!

نود إبلاغكم بأن البوت قد تم تحديثه وهو يعمل الآن للمرة الأولى بعد سحب التحديثات الجديدة.

=== تفاصيل التحديث ===
{{| class="wikitable sortable mw-collapsible"
|+ تفاصيل التحديث
|-
! القسم !! التفاصيل
|-
| اسم الأداة || {self.tool_name}
|-
| نسخة البوت || {self.bot_version}
|-
| آخر تحديث || {self.commit_info.commit_message}
|-
| رابط التحديث || [رابط التحديث]({self.commit_info.commit_html_url})
|-
| تاريخ ووقت آخر تحديث || {self.commit_info.format_commit_date()}
|-
| تاريخ ووقت التشغيل || {self.timestamp}
|-
|}}

=== المساهمون ===
{contributors_list}

=== ملاحظات ===
* نشكر جميع المساهمين في هذا التحديث.
* لمزيد من المعلومات أو المساعدة، يمكنكم زيارة [مستندات الدعم](https://example.com/support).

مع أطيب التحيات،
~~~~
'''
        return message

    def get_page_title(self) -> str:
        """
        Get the wiki page title for this log.

        Returns:
            str: Wiki page title
        """
        return f'مستخدم:CI-CD log/{self.tool_name}'

    @classmethod
    def create_with_defaults(
        cls,
        tool_name: str,
        bot_version: str,
        commit_info: Optional[CommitInfo] = None,
        contributors: Optional[List[str]] = None,
        timestamp: Optional[str] = None
    ) -> 'BotLog':
        """
        Create a BotLog instance with default values.

        Args:
            tool_name (str): Name of the tool/bot
            bot_version (str): Version of the bot
            commit_info (Optional[CommitInfo]): Commit information, defaults to unavailable
            contributors (Optional[List[str]]): List of contributors, defaults to unavailable
            timestamp (Optional[str]): Current timestamp, defaults to current time

        Returns:
            BotLog: A BotLog instance with default values
        """
        default_commit = commit_info or CommitInfo.create_unavailable()
        default_contributors = contributors or ["غير متوفر"]

        return cls(
            tool_name=tool_name,
            bot_version=bot_version,
            commit_info=default_commit,
            contributors=default_contributors,
            timestamp=timestamp
        )