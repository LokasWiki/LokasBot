import copy
import logging
import re
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


class WikiListFormatInterface(ABC):
    """
    Represents an interface for checking the format of a wiki list and performing operations on it.
    """

    @abstractmethod
    def set_wiki_text(self, wiki_text):
        """
        Set the wiki text.

        Args:
            wiki_text (str): The wiki text to set.
        """
        pass

    @abstractmethod
    def check_format(self):
        """
        Check the format of the wiki list.

        Returns:
            bool: True if the wiki list has the correct format, False otherwise.
        """
        pass

    @abstractmethod
    def get_list(self):
        """
        Get the wiki list.

        Returns:
            list: The wiki list.
        """
        pass


class WikiListFormatChecker(WikiListFormatInterface):
    """
    Represents a class for checking the format of a wiki list and performing operations on it.

    Methods:
        set_wiki_text: Set the wiki text.
        check_format: Check the format of the wiki list.
        get_list: Get the wiki list.

    Example:
        # Create a WikiListFormatChecker object
        format_checker = WikiListFormatChecker()

        # Set the wiki text
        format_checker.set_wiki_text("1. Item 1\n2. Item 2\n3. Item 3")

        # Check the format of the wiki list
        is_format_correct = format_checker.check_format()

        if is_format_correct:
            print("The wiki list format is correct!")
        else:
            print("The wiki list format is incorrect.")

        # Get the wiki list
        wiki_list = format_checker.get_list()
        print("The wiki list is:", wiki_list)
    """

    def __init__(self):
        self.list = []
        self.wiki_text = ""

    def set_wiki_text(self, wiki_text):
        """
        Set the wiki text.

        Args:
            wiki_text (str): The wiki text to set.
        """
        self.wiki_text = wiki_text

    def check_format(self):
        """
        Check the format of the wiki list.

        Returns:
            bool: True if the wiki list has the correct format, False otherwise.
        """
        tem_wiki_text = self.wiki_text.replace("{{/مقدمة}}", "").strip()
        status = True
        regex = re.compile(
            r"\*\s*\[\[(?P<from_ns>.*):(?P<source>.*)\]\](?P<extra>.*\>.*)\[\[(?P<to_ns>.*):(?P<destination>.*)\]\]")
        # loop line by line
        for line in tem_wiki_text.split("\n"):
            # to skip empty lines
            if line.strip() == "":
                continue
            line_regex = regex.match(line.strip())
            if line_regex:
                # print from_ns, source, to_ns, destination
                from_ns = line_regex.group("from_ns")
                source = line_regex.group("source")
                to_ns = line_regex.group("to_ns")
                destination = line_regex.group("destination")
                # todo: add list of namespaces that only allowed to move
                self.list.append({
                    "from_ns": from_ns,
                    "source": source,
                    "to_ns": to_ns,
                    "destination": destination
                })
            else:
                status = False
                break
        return status

    def get_list(self):
        """
        Get the wiki list.

        Returns:
            list: The wiki list.
        """
        return self.list


class Order:
    """
    Represents an order.

    Attributes:
        from_ns (str): The source namespace of the order.
        source (str): The source of the order.
        to_ns (str): The destination namespace of the order.
        destination (str): The destination of the order.
        description (str): The description of the order.
        options (str): The options of the order.

    Methods:
        __init__: Initialize a new instance of the Order class.
        set_description: Set the description of the order.
        set_options: Set the options of the order.

    Example:
        # Create a new order
        order = Order("NS1", "Source1", "NS2", "Destination1")

        # Set the description of the order
        order.set_description("This is a sample order.")

        # Set the options of the order
        order.set_options("Option 1, Option 2, Option 3")

        # Access the attributes of the order
        print("From Namespace:", order.from_ns)
        print("Source:", order.source)
        print("To Namespace:", order.to_ns)
        print("Destination:", order.destination)
        print("Description:", order.description)
        print("Options:", order.options)
    """

    def __init__(self, from_ns, source, to_ns, destination):
        """
        Initialize a new instance of the Order class.

        Args:
            from_ns (str): The source namespace of the order.
            source (str): The source of the order.
            to_ns (str): The destination namespace of the order.
            destination (str): The destination of the order.
        """
        self.from_ns = from_ns.replace(":", "")
        self.source = source
        self.to_ns = to_ns.replace(":", "")
        self.destination = destination
        self.description = ""
        self.options = ""

    def set_description(self, description):
        """
        Set the description of the order.

        Args:
            description (str): The description to set.
        """
        self.description = description

    def set_options(self, options):
        """
        Set the options of the order.

        Args:
            options (str): The options to set.
        """
        self.options = options


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
                 task_stats: BotRunnerInterface, last_user_edit_role: LastUserEditRoleInterface,
                 wiki_text_list: WikiListFormatInterface):
        self.description = description
        self.option = option
        self.task_stats = task_stats
        self.site = site
        self.last_user_edit_role = last_user_edit_role
        self.wiki_text_list = wiki_text_list
        self.orders_list = []

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

    def check_format(self):
        if self.wiki_text_list.check_format():
            print("can run page status has true value")
            return True
        else:
            print("can run page status has false value")
            return False

    def get_list(self):
        temp_list = self.wiki_text_list.get_list()
        self.orders_list = []
        for item in temp_list:
            order = Order(item["from_ns"], item["source"], item["to_ns"], item["destination"])
            order.set_description(self.description.get_description())
            order.set_options(self.option.get_options())
            self.orders_list.append(order)
        return self.orders_list

    def can_read(self):
        return self.can_bot_run() and self.check_user_role() and self.check_format()

    def move_to_talk_page(self):
        # titles
        page_name = "ويكيبيديا:طلبات نقل عبر البوت"
        talk_name = "ويكيبيديا:طلبات نقل عبر البوت/أرشيف 10"
        turn_on_name = "ويكيبيديا:طلبات نقل عبر البوت/تشغيل البوت"
        # objects
        page = pywikibot.Page(self.site, page_name)
        archive_page = pywikibot.Page(self.site, talk_name)
        turn_on_name = pywikibot.Page(self.site, turn_on_name)
        # set texts
        template = "{{/مقدمة}}"
        archive_page.text = archive_page.text + "\n" + page.text.replace(template, "")
        page.text = template
        turn_on_name.text = "لا"
        # start save
        page.save("جاري النقل")
        archive_page.save("اضافة الي الارشيف")
        turn_on_name.save("تم تشغيل البوت")
