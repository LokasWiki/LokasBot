import random
import re

import pywikibot
import pymysql
from pywikibot import config as _config
import os
import datetime
import pywikibot.flow


class Base:
    def __init__(self):
        # for test only
        #
        # first_day = datetime.datetime(2022, 12, 1)
        # last_day = datetime.datetime(2023, 1, 31)
        #
        # # for real
        #  well run every day
        first_day = datetime.datetime.now() - datetime.timedelta(days=1)
        last_day = datetime.datetime.now()

        self.first_day_of_week = first_day
        # self.last_day_of_week = last_day
        # self.last_day_of_week = self.first_day_of_week + datetime.timedelta(days=6)
        self.last_day_of_week = last_day

        self.year, self.week, self.day = first_day.isocalendar()

        start_of_day = datetime.time(hour=0, minute=0, second=0)
        self.first_day_of_week_formatted = datetime.datetime.combine(self.first_day_of_week, start_of_day).strftime(
            "%Y%m%d%H%M%S")
        end_of_day = datetime.time(hour=23, minute=59, second=59)
        self.last_day_of_week_formatted = self.last_day_of_week.combine(self.last_day_of_week, end_of_day).strftime(
            "%Y%m%d%H%M%S")


class Database(Base):
    """A class for interacting with a database.

    Attributes:
        _connection (pymysql.connections.Connection): A connection to the database.
        _query (str): The current SQL query.
        result (list): The result of the last executed query.
    """

    def __init__(self):
        """Initializes the Database with the connection and query attributes set to None, and result set to an empty list."""
        super().__init__()
        self._connection = None
        self._query = ""
        self.result = []

    @property
    def connection(self):
        """Returns the current connection to the database. If none exists, a new connection is established and returned.

        Returns:
            pymysql.connections.Connection: A connection to the database.
        """

        if self._connection is not None:
            return self._connection
        else:
            return pymysql.connect(
                host=_config.db_hostname_format.format("arwiki"),
                read_default_file=_config.db_connect_file,
                db=_config.db_name_format.format("arwiki"),
                charset='utf8mb4',
                port=_config.db_port,
                cursorclass=pymysql.cursors.DictCursor,
            )

    @property
    def query(self):
        """Returns the current SQL query.

        Returns:
            str: The current SQL query.
        """
        return self._query

    @query.setter
    def query(self, value):
        """Sets the current SQL query and replaces placeholders with the appropriate values.

        Args:
            value (str): The new SQL query.
        """
        self._query = str(value).replace("START_DATE", self.first_day_of_week_formatted).replace("END_DATE",
                                                                                                 self.last_day_of_week_formatted)


    def get_content_from_database(self):
        """Executes the current SQL query and stores the result in the `result` attribute.

        Raises:
            pymysql.err.OperationalError: If a connection to the database cannot be established.
        """
        try:
            # Create a cursor page
            with self.connection.cursor() as cursor:
                # Execute the SELECT statement
                cursor.execute(self._query)
                # Fetch all the rows of the result
                self.result = cursor.fetchall()
        finally:
            # Close the connection
            self.connection.close()

    @connection.setter
    def connection(self, value):
        """Sets the current connection to the database.

        Args:
            value (pymysql.connections.Connection): The new connection to the database.
        """
        self._connection = value


class SignaturePage:
    def __init__(self, site):
        self._title = ""
        self._page = None
        self.site = site

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def page(self):
        return self._page

    def load_page(self):
        self._page = pywikibot.Page(self.site, self.title)

    def get_page_text(self):
        if self._page is None:
            self.load_page()
        text = self._page.text
        return text


class SignatureScanner:
    def __init__(self):
        self._pattern = None
        self._requests = []
        self._have_requests = False

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value

    @property
    def requests(self):
        return self._requests

    @property
    def have_requests(self):
        return self._have_requests

    def scan(self, text):
        matches = re.finditer(self.pattern, text, re.MULTILINE)
        self._requests = []
        for match in matches:
            request = match.groupdict()
            self._requests.append(request)
        if self._requests:
            self._have_requests = True
        else:
            self._have_requests = False


class SendTemplate(Base):
    def __init__(self, input_dict,signature_list):
        """
        Initialize a SendTemplate object with a dictionary of input parameters.
        :param input_dict: A dictionary of input parameters with keys:
            - 'query': The query to be executed on the database.
            - 'template_stub': The stub of the template to be sent to users, with placeholders for year, week, and rank.
        """
        super().__init__()
        self.database = Database()
        self.database.query = str(input_dict['query']).replace("NUMBER_COUNT", str(input_dict['number']))
        self.database.get_content_from_database()
        self.input_dict = input_dict
        self.signature_list = signature_list
    def send(self):
        """
        Send the template to the top 5 users in the database query results.
        """
        # Set the site and user to be used
        site = pywikibot.Site()

        for member in self.database.result:
            name = str(member['actor_name'], 'utf-8')

            # Retrieve the user talk page
            user = pywikibot.User(site, name)

            if user.is_blocked() or ("BOT" in [str(x).upper() for x in user.groups()]):
                continue

            # Get the user page for the user
            talk_page = user.getUserTalkPage()
            signature = str(random.choice(self.signature_list)['signature'])
            if talk_page.is_flow_page():
                board = pywikibot.flow.Board(talk_page)

                # Add a new section to the page
                title = 'تهانينا'
                content = self.input_dict['template_stub'].replace('NUMBER', str(self.input_dict['number'])).replace("SIGNATURE",signature).replace("USERNAME",name)

                try:
                    print("start send to " + name)
                    topic = board.new_topic(title, content)
                except Exception as error:
                    print(f'Error saving page: {error}')

            else:
                pass
                # Add a new section to the page
                text = talk_page.text
                text += '\n\n== تهانينا ==\n\n'
                text += self.input_dict['template_stub'].replace('NUMBER', str(self.input_dict['number'])).replace("SIGNATURE",signature).replace("USERNAME",name)

                try:
                    # Save the edited page
                    print("start send to " + name)
                    talk_page.text = text
                    summary = str("بوت:[[ويكيبيديا:توزيع أوسمة|توزيع أوسمة]] (NUMBER_COUNT تعديل) (v1.2)").replace('NUMBER_COUNT', str(self.input_dict['number']))
                    # Save the page
                    talk_page.save(summary=summary,minor=False)
                except Exception as error:
                    print(f'Error saving page: {error}')
