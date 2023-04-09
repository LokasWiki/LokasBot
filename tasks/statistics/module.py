import os

import pymysql
import pywikibot
from pywikibot import config as _config


class Database:
    def __init__(self):
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
        self._query = value

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


class Page:
    def __init__(self):
        self.site = pywikibot.Site()
        self._page_name = ""
        self.contents = ""
        self._summary = "بوت:إحصاءات V2.2.1"

    @property
    def page_name(self):
        return self._page_name

    @page_name.setter
    def page_name(self, value):
        self._page_name = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    def make_new_text(self):
        # Get the username of the bot account
        username_bot = self.site.username()
        self.contents = self.contents.replace(
            'BOT_USER_NAME', f"[[مستخدم:{username_bot}|{username_bot}]]"
        ).replace(
            "BOT_TIME_NOW", "{{نسخ:#time:H:i، j F Y}}"
        )

    def set_contents(self, content):
        self.contents = content

    def save_page(self):
        # Get a Page object for the page
        page = pywikibot.Page(self.site, self.page_name)
        self.make_new_text()
        # Set the text of the page
        # Set the text of the page
        page.text = self.contents
        # Save the page
        page.save(summary=self.summary)


class File:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.file_path = ""
        self.contents = ""

    def set_stub_path(self, name):
        # Construct the file path
        self.file_path = os.path.join(self.script_dir, name)

    def get_file_content(self):
        # Open the file in read mode
        with open(self.file_path) as file:
            # Read the contents of the file
            self.contents = file.read()


class ArticleTable:
    def __init__(self):
        self.columns = []
        self.add_header_text = None
        self.add_footer_text = None
        self.add_table_name = None
        self.add_end_row_to_table = None
        self.sort_column = None

    def add_column(self, name, value_index, clause=None):
        self.columns.append((name, value_index, clause))

    def set_sort_column(self, column_name):
        self.sort_column = column_name

    def build_table(self, result, end_row_in_table=None, header_text=None, footer_text=None):
        if self.sort_column:
            result = sorted(result, key=lambda x: x[self.sort_column], reverse=True)

        table_header = ""
        if header_text is not None:
            table_header += header_text(result)

        # create the table header
        header = '{| class="wikitable sortable"\n'
        for column_name, _, _ in self.columns:
            header += f'!style="background-color:#808080" align="center"|{column_name}\n'

        # create the table body
        body = header

        for index, row in enumerate(result):
            body += '|-\n'
            for _, value_index, clause in self.columns:
                if clause:
                    cell_value = clause(row, result, index)
                else:
                    if isinstance(row[value_index], (str, bytes)):
                        cell_value = str(row[value_index], 'utf-8')
                    else:
                        cell_value = str(row[value_index])
                body += f'|{cell_value}\n'
            body += '\n'
        if end_row_in_table is not None:
            body += end_row_in_table(result)

        # create the table footer
        footer = '|}\n'

        if footer_text is not None:
            footer += footer_text(result)

        # return the full table
        return str(table_header + body + footer).replace("TABLE_NAME", str(self.add_table_name))


class UpdatePage:
    def __init__(self, query, file_path, page_name, tables, connection=None):
        self.database = Database()
        self.file = File()
        self.tables = tables
        self.page = Page()
        if connection is not None:
            self.database.connection = connection
        self.database.query = query
        self.database.get_content_from_database()

        self.file.set_stub_path(file_path)
        self.file.get_file_content()

        self.page.page_name = page_name

    def update(self):
        content = self.file.contents
        table_body = ""
        for table in self.tables.tables:
            table_body += table.build_table(result=self.database.result, end_row_in_table=table.add_end_row_to_table,
                                            header_text=table.add_header_text, footer_text=table.add_footer_text)

        content = content.replace("BOT_TABLE_BODY", table_body)
        self.page.set_contents(content)
        self.page.save_page()


class ArticleTables:
    def __init__(self):
        self.tables = []

    def add_table(self, name, columns, header_text=None, footer_text=None, end_row_text=None, sort_column=None):
        table = ArticleTable()
        if header_text is not None:
            table.add_header_text = header_text

        if footer_text is not None:
            table.add_footer_text = footer_text

        if end_row_text is not None:
            table.add_end_row_to_table = end_row_text

        if name is not None:
            table.add_table_name = name

        if sort_column is not None:
            table.set_sort_column(sort_column)

        for column in columns:
            column_name = column[0]
            value_index = column[1]
            clause = None
            if len(column) > 2:
                clause = column[2]
            table.add_column(column_name, value_index, clause=clause)
        self.tables.append(table)


def index(row, result, index):
    return index + 1
