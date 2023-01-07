import pywikibot
import pymysql
from pywikibot import config as _config
import os
import datetime


class Translator:
    def __init__(self):
        self.english_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                               'October', 'November', 'December']
        self.arabic_months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر',
                              'نوفمبر', 'ديسمبر']
        self.english_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.arabic_days = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']

        self.english_rank = ['1', '2', '3', '4', '5', '6', '7']
        self.arabic_rank = ['الاول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع']


    def translate_month(self, month):
        if month in self.english_months:
            return self.arabic_months[self.english_months.index(month)]
        else:
            return month

    def translate_rank(self, rank):
        if rank in self.english_rank:
            return self.arabic_rank[self.english_rank.index(rank)]
        else:
            return rank

    def translate_day(self, day):
        if day in self.english_days:
            return self.arabic_days[self.english_days.index(day)]
        else:
            return day


class Base:
    def __init__(self):
        self.translator = Translator()
        # for test only
        #
        # first_day = datetime.datetime(2021, 1, 11)
        # last_day = datetime.datetime(2021, 1, 18)
        # current_day = datetime.datetime(2021, 1, 17)

        # for real
        first_day = None
        last_day = None
        current_day = None

        # Set the first and last day of the week to the current week if not specified
        if first_day is None or last_day is None:
            # Get the current date and time
            self.now = datetime.datetime.now()
            # Get the ISO year, week number, and day of the week
            self.year, self.week, self.day = self.now.isocalendar()
            # Get the first day of the week as Monday
            self.first_day_of_week = self.now - datetime.timedelta(days=self.now.weekday())
            if self.now.weekday() == 6:
                self.first_day_of_week -= datetime.timedelta(days=6)
            # Get the last day of the week
            self.last_day_of_week = self.first_day_of_week + datetime.timedelta(days=6)
        else:
            self.first_day_of_week = first_day
            self.last_day_of_week = last_day
            self.year, self.week, self.day = current_day.isocalendar()

        # Get the directory of the script
        self.script_dir = os.path.dirname(__file__)
        # domain_name = "ويكيبيديا:"
        self.domain_name = "مستخدم:لوقا/"

        # Format the first and last day of the week in the desired format
        self.date_before_30_days = self.first_day_of_week - datetime.timedelta(days=30)

        self.date_before_30_days_formatted = self.date_before_30_days.replace(hour=0, minute=0, second=0).strftime(
            "%Y%m%d%H%M%S")

        self.first_day_of_week_formatted = self.first_day_of_week.replace(hour=0, minute=0, second=0).strftime(
            "%Y%m%d%H%M%S")
        self.last_day_of_week_formatted = self.last_day_of_week.replace(hour=0, minute=0, second=0).strftime(
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
    def __init__(self):
        super().__init__()
        self._connection = None
        self._query = ""
        self.result = []

    @property
    def connection(self):
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
        return self._query

    @query.setter
    def query(self, value):

        self._query = str(value).replace("START_WEEK_DATE", self.first_day_of_week_formatted).replace("END_WEEK_DATE",
                                                                                                      self.last_day_of_week_formatted).replace(
            "DATE_BEFORE_30_DAYS", self.date_before_30_days_formatted)

    def get_content_from_database(self):
        try:
            # Create a cursor object
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
        self._connection = value


class TableGenerator(Base):
    def __init__(self, competition_page, team, activity, members):
        super().__init__()
        self.competition_page = str(competition_page).replace("WEEK_NUMBER", str(self.week)).replace("YEAR_NUMBER",
                                                                                                     str(self.year)).replace(
            "DOMAIN_NAME", str(self.domain_name))
        self.team = team
        self.activity = activity
        self.members = members

    def generate_table(self):
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
    def __init__(self, input_dict):
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
        # Generate the table
        table = self.table_generator.generate_table()
        # Set the site you want to use
        site = pywikibot.Site("ar", "wikipedia")
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
        super().__init__()

        self.database = Database()
        self.database.query = input_dict['query']
        self.database.get_content_from_database()
        self.input_dict = input_dict

    def send(self):
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

            # Add a new section to the page
            text = talk_page.text
            text += '\n\n== تهانينا ==\n\n'
            text += self.input_dict['template_stub'].replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER", str(self.week)).replace("RANK", self.translator.translate_rank(str(rank)))

            talk_page.text = text
            # Save the page
            talk_page.save("بوت:توزيع أوسمة مستخدمو الأسبوع الأكثر نشاطا")


class MainPage(Base):
    def __init__(self, title_of_page, summary, stub):
        super().__init__()
        self.summary = summary
        self.title_of_page = str(title_of_page).replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                               str(self.week)).replace(
            "DOMAIN_NAME", self.domain_name)
        self.stub = stub
        self.text = ""

    def read_file(self):
        # Construct the file path
        file_path = os.path.join(self.script_dir, self.stub)
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file
            self.text = file.read()

    def save_page(self):
        # Connect to the site
        site = pywikibot.Site("ar", "wikipedia")
        # Get a SubPage object for the page

        page = pywikibot.Page(site, self.title_of_page)

        # Set the text of the page
        page.text = str(self.text).replace('YEAR_NUMBER', str(self.year)).replace("WEEK_NUMBER",
                                                                                  str(self.week)).replace(
            "DOMAIN_NAME", self.domain_name).replace("ARCHIVE_INTO_TEXT_TEXT", self.archive_into_text_text)

        # Save the page
        page.save(summary=self.summary)
