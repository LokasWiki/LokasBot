import copy
import logging
from abc import ABC, abstractmethod

import pywikibot
import wikitextparser as wtp

from core.utils.helpers import prepare_str


class TaskDescriptionInterface(ABC):
    """
    Interface for a task description.
    """

    @abstractmethod
    def get_description(self):
        """
        Retrieves the description for the object.

        Returns:
            str: The default description for the object.
        """
        pass


class TaskDescription(TaskDescriptionInterface):
    """
    Represents a task description object.

    Args:
        site (str): The site of the task.
        page_title (str): The title of the page.
        default_description (str): The default description.

    Attributes:
        site (str): The site of the task.
        page_title (str): The title of the page.
        default_description (str): The default description.

    Methods:
        get_description: Retrieves the description for the object.

    Usage:
        # Create a TaskDescription object
        site = pywikibot.Site()
        task_description = TaskDescription(site=site, page_title='Page 1', default_description='Default description')

        # Get the description
        description = task_description.get_description()
    """

    def __init__(self, site, page_title, default_description):
        self.site = site
        self.page_title = page_title
        self.default_description = default_description

    def get_description(self):
        """
        Retrieves the description for the object.

        Returns:
            str: The default description for the object.
        """
        try:
            page = pywikibot.Page(self.site, self.page_title)
            if page.exists() and page.text != "":
                parsed = wtp.parse(page.text)
                text = copy.deepcopy(page.text)
                for comment in parsed.comments:
                    text = str(text).replace(str(comment), "")
                self.default_description = str(text).strip()
        except Exception as e:
            print(e)
            logging.error(e)
        return self.default_description


class TaskOptionInterface(ABC):
    """
    Represents an interface for a task option object.
    """

    @abstractmethod
    def get_options(self):
        """
        Retrieves the options.

        Returns:
            dict: A dictionary containing the options and their values.
        """
        pass


class TaskOption(TaskOptionInterface):
    """
    Represents a task option object.

    Args:
        site (str): The site of the task.
        page_title (str): The title of the page.
        template_name (str): The name of the template.

    Attributes:
        site (str): The site of the task.
        page_title (str): The title of the page.
        template_name (str): The name of the template.

    Methods:
        get_options: Retrieves the options from the template on the page or the default options.

    """

    DEFAULT_OPTIONS = {
        'move-subpages': 'yes',
        'leave-redirect': 'yes',
        'leave-talk': 'yes',
        'move-talk': 'yes'
    }

    def __init__(self, site, page_title, template_name):
        self.site = site
        self.page_title = page_title
        self.template_name = template_name

    def get_options(self):
        """
        Retrieves the options from the template on the page or the default options.

        Returns:
            dict: A dictionary containing the options and their values.
        """
        options = self.DEFAULT_OPTIONS.copy()

        try:
            page = pywikibot.Page(self.site, self.page_title)
            parsed = wtp.parse(page.text)
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(self.template_name):
                    for arg in template.arguments:
                        options[prepare_str(arg.name)] = prepare_str(arg.value)
        except Exception as e:
            print(e)
            logging.error(e)

        return options


class BotRunnerInterface(ABC):
    """
    Represents an interface for a bot runner object.
    """

    @abstractmethod
    def can_run(self):
        """
        Checks if the bot can be run.

        Returns:
            bool: True if the bot can be run, False otherwise.
        """
        pass


class BotRunner(BotRunnerInterface):
    """
    Represents a bot runner object.

    Args:
        site (str): The site of the page.
        page_title (str): The title of the page.

    Attributes:
        site (str): The site of the page.
        page_title (str): The title of the page.

    Methods:
        can_run: Checks if the bot can be run based on the description and option of the page.

    Example:
        # Create a BotRunner object
        bot_runner = BotRunner(site='example.com', page_title='Page 1')

        # Check if the bot can be run
        can_run = bot_runner.can_run()

        if can_run:
            print("The bot can be run!")
        else:
            print("The bot cannot be run.")

    """

    def __init__(self, site, page_title):
        self.site = site
        self.page_title = page_title
        self.status = False
        self.yes_word = "نعم"

    def can_run(self):
        """
        Checks if the bot can be run based on the description and option of the page.

        Returns:
            bool: True if the bot can be run, False otherwise.
        """

        try:
            page = pywikibot.Page(self.site, self.page_title)
            if page.exists():
                text = page.text
                self.status = prepare_str(text) == prepare_str(self.yes_word)
        except Exception as e:
            print(e)
            logging.error(e)

        return self.status


class LastUserEditRoleInterface(ABC):
    """
    Represents an interface for checking the role of the last user who edited a page.
    """

    def __init__(self, page: pywikibot.Page, role: str):
        self.page = page
        self.role = role

    @abstractmethod
    def get_last_user_role(self) -> list:
        """
        Get the role of the last user who edited the page.
        Returns:
            list: The role of the last user who edited the page.
        """
        pass

    @abstractmethod
    def check_user_role(self) -> bool:
        """
        Checks if the user has the role of the last user who edited the page.
        Returns:
            bool: True if the user has the role of the last user who edited the page, False otherwise.
        """
        pass


class LastUserEditRoleChecker(LastUserEditRoleInterface):
    """
    Represents a class for checking the role of the last user who edited a page.
    """

    def __init__(self, page: pywikibot.Page, role: str):
        super().__init__(page=page, role=role)

    def get_last_user_role(self) -> list:
        """
        Get the role of the last user who edited the page.
        Returns:
            list: The role of the last user who edited the page.
        """
        try:
            last_user = self.page.lastNonBotUser()
            user = pywikibot.User(self.page.site, last_user)
            return user.groups()
        except Exception as e:
            print(e)
            logging.error(e)
            return []

    def check_user_role(self) -> bool:
        """
        Checks if the user has the role of the last user who edited the page.
        Returns:
            bool: True if the user has the role of the last user who edited the page, False otherwise.
        """
        return self.role in self.get_last_user_role()


class WikipediaTaskReader:
    """
        Represents a task reader for Wikipedia.

        Args:
            description (DescriptionInterface): The description object.
            option (OptionInterface): The option object.
            task (TaskInterface): The task object.
            last_user_edit_role (LastUserEditRoleInterface): The last user edit role object.
        Methods:
            can_run: Checks if the bot can be run based on the description, option, and task.

        Example:
            # Create description, option, and task objects
            description = DescriptionImpl()
            option = OptionImpl()
            task = TaskImpl()

            # Create a WikipediaTaskReader object
            task_reader = WikipediaTaskReader(description, option, task)

            # Check if the bot can be run
            can_run = task_reader.can_run()

            if can_run:
                print("The bot can be run!")
            else:
                print("The bot cannot be run.")
    """

    def __init__(self, site: pywikibot.Site, description: TaskDescriptionInterface, option: TaskOptionInterface,
                 task_stats: BotRunnerInterface, last_user_edit_role: LastUserEditRoleInterface):
        self.description = description
        self.option = option
        self.task_stats = task_stats
        self.site = site
        self.last_user_edit_role = last_user_edit_role

    def can_bot_run(self):
        """
        Check if the bot can run based on the status of the page.

        Returns:
            bool: True if the bot can run, False otherwise.
        """
        if self.task_stats.can_run():
            print("can run page status has true value")
            return True
        else:
            print("can run page status has false value")
            return False

    def check_user_role(self) -> bool:
        if self.last_user_edit_role.check_user_role():
            print("can run page status has true value")
            return True
        else:
            print("can run page status has false value")
            return False

    def read(self):
        """
        Reads and returns the task.

        Returns:
            TaskDescription: The task description.
        """
        return self.task
