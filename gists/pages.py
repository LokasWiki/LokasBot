import re

import pywikibot
import pymysql
from pywikibot import config as _config
import os
import datetime
import pywikibot.flow


class Database():
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
        self._query = value

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



db = Database()
db.query = """select page_title
from page
where page_namespace in (10) and page_title like "%أفريقي%" and page_is_redirect = 0 order by page_id;"""
db.get_content_from_database()

text = """<big>'''حالة الطلب:'''</big>  {{تم}}   <big>'''أو'''</big>    {{مرفوض}}
{| class="wikitable"
|+
! colspan="3" |<big>قالب (نطاق 10) (762 قالب)</big>
|-
!العنوان السابق
!نقل إلى
!حالة الطلب"""
text +="\n"
for row in db.result:
    o_title = str(row['page_title'], 'utf-8')
    result = re.search("أفريقي", o_title)
    n_title = o_title[:result.start()] + "إفريقي" + o_title[result.end():]
    oo_title = o_title[:result.start()] + "'''أفريقي'''" + o_title[result.end():]
    text +="|- \n|[[:قالب:"+o_title+"|قالب:"+oo_title+"]] \n|قالب:"+n_title+" \n|"
    # text +="|- \n|[["+o_title+"|"+oo_title+"]] \n|"+n_title+" \n|"

    text += "\n"
text +="\n"
text +="""|}"""


site = pywikibot.Site()
page = pywikibot.Page(site,"مستخدم:لوقا/ملعب 4")
page.text = text
page.save("انشاء")