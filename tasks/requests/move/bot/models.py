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


class TaskOption:
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


class WikipediaTaskReader:
    """
    Reads tasks from Wikipedia.

    Attributes:
        task (TaskDescription): The task description.

    Methods:
        read: Reads and returns the task.
    """

    def __init__(self, task_description):
        """
        Initializes a new instance of the WikipediaTaskReader class.

        Args:
            task_description (TaskDescription): The task description.
        """
        self.task = task_description

    def read(self):
        """
        Reads and returns the task.

        Returns:
            TaskDescription: The task description.
        """
        return self.task


page_name = "ويكيبيديا:طلبات نقل عبر البوت/ملخص التعديل"
site = pywikibot.Site("ar", "wikipedia")
default_description = "بوت:نقل ([[ويكيبيديا:طلبات نقل عبر البوت]])"
task_description = TaskDescription(site=site, page_title=page_name, default_description=default_description)
print(task_description.get_description())

option_page_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت"
default_template_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت/قالب"
task_option = TaskOption(site=site, page_title=option_page_name, template_name=default_template_name)
print(task_option.get_options())

bot_runner_page_name = "ويكيبيديا:طلبات نقل عبر البوت/تشغيل البوت"
bot_runner = BotRunner(site=site, page_title=bot_runner_page_name)
print(bot_runner.can_run())
