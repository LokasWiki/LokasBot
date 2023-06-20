import datetime
import os

import pymysql
import pywikibot
import pywikibot.flow
from pywikibot import config as _config


class Translator:
    """A class for translating English words to Arabic.

    Attributes:
        english_months (list): A list of English month names.
        arabic_months (list): A list of Arabic month names.
        english_days (list): A list of English day names.
        arabic_days (list): A list of Arabic day names.
        english_rank (list): A list of English rank names (1st, 2nd, etc.).
        arabic_rank (list): A list of Arabic rank names (الأول, الثاني, etc.).
    """

    def __init__(self):
        """Initializes the Translator with the lists of English and Arabic words."""
        self.english_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                               'October', 'November', 'December']
        self.arabic_months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر',
                              'نوفمبر', 'ديسمبر']
        self.english_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.arabic_days = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']

        self.english_rank = ['1', '2', '3', '4', '5', '6', '7']
        self.arabic_rank = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع']

    def translate_month(self, month):
        """Translates an English month name to Arabic.

        Args:
            month (str): An English month name.

        Returns:
            str: The corresponding Arabic month name, or the original string if not found in the list of English month names.
        """

        if month in self.english_months:
            return self.arabic_months[self.english_months.index(month)]
        else:
            return month

    def translate_rank(self, rank):
        """Translates an English rank name to Arabic.

        Args:
            rank (str): An English rank name.

        Returns:
            str: The corresponding Arabic rank name, or the original string if not found in the list of English rank names.
        """
        if rank in self.english_rank:
            return self.arabic_rank[self.english_rank.index(rank)]
        else:
            return rank

    def translate_day(self, day):
        """Translates an English day name to Arabic.

        Args:
            day (str): An English day name.

        Returns:
            str: The corresponding Arabic day name, or the original string if not found in the list of English day names.
        """
        if day in self.english_days:
            return self.arabic_days[self.english_days.index(day)]
        else:
            return day


class Base:
    def __init__(self):
        self.translator = Translator()
        # for test only
        #
        # first_day = datetime.datetime(2023, 1, 2)
        # last_day = datetime.datetime(2023, 1, 8)
        #
        # # for real
        first_day = None
        last_day = None

        # Set the first and last day of the week to the current week if not specified
        if first_day is None or last_day is None:
            # Get the current date and time
            self.now = datetime.datetime.now() - datetime.timedelta(days=1)
            # Get the ISO year, week number, and day of the week
            self.year, self.week, self.day = self.now.isocalendar()
            # Get the first day of the week as Monday
            self.first_day_of_week = self.now - datetime.timedelta(days=self.now.weekday())
            # if self.now.weekday() == 6:
            #     self.first_day_of_week -= datetime.timedelta(days=6)
            # Get the last day of the week
            self.last_day_of_week = self.first_day_of_week + datetime.timedelta(days=6)
        else:
            self.first_day_of_week = first_day
            # self.last_day_of_week = last_day
            self.last_day_of_week = self.first_day_of_week + datetime.timedelta(days=6)
            self.year, self.week, self.day = first_day.isocalendar()

        # Get the directory of the script
        self.script_dir = os.path.dirname(__file__)
        self.domain_name = "ويكيبيديا:"
        # self.domain_name = "مستخدم:لوقا/"

        # Format the first and last day of the week in the desired format
        self.date_before_30_days = self.first_day_of_week - datetime.timedelta(days=30)

        self.date_before_30_days_formatted = self.date_before_30_days.replace(hour=0, minute=0, second=0).strftime(
            "%Y%m%d%H%M%S")
        start_of_day = datetime.time(hour=0, minute=0, second=0)
        self.first_day_of_week_formatted = datetime.datetime.combine(self.first_day_of_week, start_of_day).strftime(
            "%Y%m%d%H%M%S")
        end_of_day = datetime.time(hour=23, minute=59, second=59)
        self.last_day_of_week_formatted = self.last_day_of_week.combine(self.last_day_of_week, end_of_day).strftime(
            "%Y%m%d%H%M%S")

        # Generate the desired text
        self.archive_into_text_text = "بدأ الأسبوع يوم " + self.translator.translate_day(
            self.first_day_of_week.strftime(
                "%A")) + " " + self.first_day_of_week.strftime(
            "%d ") + self.translator.translate_month(self.first_day_of_week.strftime(
            "%B")) + self.first_day_of_week.strftime(
            " %Y") + " الساعة 00:00 بالتوقيت العالمي وانتهاء " + self.translator.translate_day(
            self.last_day_of_week.strftime(
                "%A")) + " " + self.last_day_of_week.strftime("%d") + " " + self.translator.translate_month(
            self.last_day_of_week.strftime("%B")) + " " + self.last_day_of_week.strftime("%Y")


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
        self._query = str(value).replace("START_WEEK_DATE", self.first_day_of_week_formatted).replace("END_WEEK_DATE",
                                                                                                      self.last_day_of_week_formatted).replace(
            "DATE_BEFORE_30_DAYS", self.date_before_30_days_formatted)

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


class TableGenerator(Base):

    def __init__(self, competition_page, team, activity, members):
        """Initializes a `TableGenerator` object.

           Args:
               competition_page (str): The name of the competition page.
               team (str): The name of the team.
               activity (str): The name of the activity.
               members (List[Dict[str, Union[str, int]]]): A list of dictionaries containing the name and score of each member.
           """
        super().__init__()
        self.competition_page = str(competition_page).replace("WEEK_NUMBER", str(self.week)).replace("YEAR_NUMBER",
                                                                                                     str(self.year)).replace(
            "DOMAIN_NAME", str(self.domain_name))
        self.team = team
        self.activity = activity
        self.members = members

    def generate_table(self):
        """Generates a Wikipedia-formatted table for the team's activity.

        Returns:
            str: The generated table as a string.
        """
        table = "{{النشاط في مستخدمو الأسبوع\n|صفحة المسابقة = " + self.competition_page + "\n|الفريق= " + self.team + "\n\n|النشاط=" + self.activity + "\n\n|الأعضاء=\n"
        rank = 1
        current_score = None
        for member in self.members:
            name = str(member['name'], 'utf-8')
            score = member['score']
            if score != current_score:
                rank = rank + 1
                current_score = score
            if rank > 6:
                break
            table += "{{مركز في مسابقة/عضو|" + name + "|" + str(score) + "}}\n"
        table += "}}"
        return table


class SubPage(Base):
    """
    SubPage class is used to create a subpage and save it on Wikipedia.
    """

    def __init__(self, input_dict):
        """
        Initializes a SubPage object with the provided input dictionary.
        Parameters:
            - input_dict: a dictionary containing the following keys:
                - 'query': the SQL query to be executed on the database to get the data for the table.
                - 'competition_page': the title of the competition page.
                - 'activity': the activity for which the data is being collected.
                - 'team': the name of the team for which the data is being collected.
                - 'title_of_page': the title of the page to be created.
                - 'summary': the summary to be used when saving the page.
        """
        super().__init__()

        self.database = Database()
        self.database.query = input_dict['query']
        self.database.get_content_from_database()

        self.input_dict = input_dict

        self.table_generator = TableGenerator(
            competition_page=input_dict['competition_page'],
            activity=input_dict['activity'],
            team=input_dict['team'],
            members=self.database.result
        )

    def save_page(self):
        """
        Creates a subpage using the provided input dictionary and saves it on Wikipedia.
        """
        # Generate the table
        table = self.table_generator.generate_table()
        # Set the site you want to use
        site = pywikibot.Site()
        title = str(self.input_dict['title_of_page']).replace("WEEK_NUMBER", str(self.week)).replace("YEAR_NUMBER",
                                                                                                     str(self.year)).replace(
            "DOMAIN_NAME", str(self.domain_name))
        # Set the page you want to edit
        page = pywikibot.Page(site, title)
        # Load the page
        page.text = table
        # Save the page with a summary
        page.save(summary=self.input_dict['summary'])


class SendTemplate(Base):
    def __init__(self, input_dict):
        """
        Initialize a SendTemplate object with a dictionary of input parameters.
        :param input_dict: A dictionary of input parameters with keys:
            - 'query': The query to be executed on the database.
            - 'template_stub': The stub of the template to be sent to users, with placeholders for year, week, and rank.
        """
        super().__init__()

        self.database = Database()
        self.database.query = input_dict['query']
        self.database.get_content_from_database()
        self.input_dict = input_dict

    def send(self):
        """
        Send the template to the top 5 users in the database query results.
        """
        # Set the site and user to be used
        site = pywikibot.Site()

        rank = 1
        current_score = None
        for member in self.database.result:
            name = str(member['name'], 'utf-8')
            score = member['score']
            if score != current_score:
                rank = rank + 1
                current_score = score
            if rank > 6:
                break

            # Retrieve the user talk page
            user = pywikibot.User(site, name)

            # Get the user page for the user
            talk_page = user.getUserTalkPage()

            if talk_page.is_flow_page():
                board = pywikibot.flow.Board(talk_page)

                # Add a new section to the page
                title = 'تهانينا'
                content = self.input_dict['template_stub'].replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                                          str(self.week)).replace(
                    "RANK", self.translator.translate_rank(str(rank - 1))).replace("USER_NAME", name)

                try:
                    topic = board.new_topic(title, content)
                except Exception as error:
                    print(f'Error saving page: {error}')

            else:
                pass
                # Add a new section to the page
                text = talk_page.text
                text += '\n\n== تهانينا ==\n\n'
                text += self.input_dict['template_stub'].replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                                        str(self.week)).replace(
                    "RANK", self.translator.translate_rank(str(rank - 1))).replace("USER_NAME", name)

                text += "\n~~~~"
                try:
                    # Save the edited page

                    talk_page.text = text

                    # Save the page
                    talk_page.save(
                        "بوت: توزيع أوسمة [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
                        minor=False
                    )
                except Exception as error:
                    print(f'Error saving page: {error}')


class MainPage(Base):
    """
    MainPage is a class used to represent the main page of the Active Users of the Week competition.
    It provides methods to read the page text from a file and save the page to Wikipedia.
    """

    def __init__(self, title_of_page, summary, stub):
        """
        Initializes a MainPage instance with the given title, summary, and stub file.

            Args:
        title_of_page (str): The title of the page to be saved on Wikipedia.
        summary (str): The summary to be used when saving the page on Wikipedia.
        stub (str): The file name of the stub file to be read.
    """

        super().__init__()
        self.summary = summary
        self.title_of_page = str(title_of_page).replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                               str(self.week)).replace(
            "DOMAIN_NAME", self.domain_name)
        self.stub = stub
        self.text = ""

    def read_file(self):
        """
        Reads the text of the page from the stub file.
        """
        # Construct the file path
        file_path = os.path.join(self.script_dir, self.stub)
        # Open the file in read mode
        with open(file_path) as file:
            # Read the contents of the file
            self.text = file.read()

    def save_page(self):
        """
              Creates a MainPage and saves it on Wikipedia.
         """
        # Connect to the site
        site = pywikibot.Site()
        # Get a SubPage page for the page

        page = pywikibot.Page(site, self.title_of_page)

        # Set the text of the page
        page.text = str(self.text).replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                  str(self.week)).replace(
            "DOMAIN_NAME", self.domain_name).replace("ARCHIVE_INTO_TEXT_TEXT", self.archive_into_text_text)

        # Save the page
        page.save(summary=self.summary)
