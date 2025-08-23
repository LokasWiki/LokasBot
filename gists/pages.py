import re

import pymysql
from pywikibot import config as _config


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


list_of_namespace = [
    {
        "namespace": 0,
        "namespace_text": "",
        "header_text": "مقالات (نطاق 0) (COUNT صفحة)"
    },
    {
        "namespace": 4,
        "namespace_text": "ويكيبيديا",
        "header_text": "ويكيبيديا (نطاق NAMESPACE) (COUNT صفحة)"
    },
    {
        "namespace": 6,
        "namespace_text": "ملف",
        "header_text": "ملف (نطاق NAMESPACE) (COUNT صفحة)"
    },
        {
        "namespace": 10,
        "namespace_text": "قالب",
        "header_text": "قالب (نطاق NAMESPACE) (COUNT صفحة)"
    },
    {
        "namespace": 14,
        "namespace_text": "تصنيف",
        "header_text": "تصنيف (نطاق NAMESPACE) (COUNT صفحة)"
    }
]
main_text = ""
for item in list_of_namespace:
    db = Database()
    db.query = """select page_title
    from page
    where page_namespace in ({}) and
    page_title like "%حقوق%"  and 
    (
        page_title like "%مجتمع_الميم%"
        or page_title like "%مجتمع_ميم%"
        or page_title like "%إل_جي_بي_تي%"
    )
      
    and page_is_redirect = 0
    order by page_id;""".format(item['namespace'])

    db.get_content_from_database()

    text = """<big>'''حالة الطلب:'''</big>  {{تم}}   <big>'''أو'''</big>    {{مرفوض}}
    {| class="wikitable"
    |+
    ! colspan="3" |<big>HEADER</big>
    |-
    !العنوان السابق
    !نقل إلى
    !حالة الطلب"""

    text = text.replace("HEADER", str(item['header_text']).replace('COUNT', str(len(db.result))).replace("NAMESPACE",
                                                                                                         str(item[
                                                                                                                 'namespace'])))
    text += "\n"
    for row in db.result:
        o_title = str(row['page_title'], 'utf-8')
        list_of_replacement = [
            ["مجتمع_الميم", "معاملة_المثليين"],
            ["مجتمع_ميم", "معاملة_المثليين"],
            ["إل_جي_بي_تي", "معاملة_المثليين"],
            # ["بيروفية", "بيروية"],
            # ["كونغولي", "كونغوي"],
            # ["كونغولية", "كونغوية"],
            # ["توغولي", "توغوي"],
            # ["توغولية", "توغوية"],
        ]

        n_title = o_title
        oo_title = o_title

        for pair in list_of_replacement:
            result = re.search(pair[0], o_title)
            if result:
                n_title = o_title[:result.start()] + pair[1] + o_title[result.end():]
                oo_title = o_title[:result.start()] + "'''" + pair[0] + "'''" + o_title[result.end():]
                break

        if item['namespace'] == 0:
            text +="|- \n|[["+o_title+"|"+oo_title+"]] \n|"+n_title+" \n|"
            # text += "|- \n|[[" + o_title + "|" + o_title + "]] \n| ~ \n|"
        else:
            text += "|- \n|[[:"+item['namespace_text']+":" + o_title + "|"+item['namespace_text']+":" + oo_title + "]] \n|"+item['namespace_text']+":" + n_title + " \n|"
            # text += "|- \n|[[:"+item['namespace_text']+":" + o_title + "|"+item['namespace_text']+":" + oo_title + "]] \n|"
            # text += "|- \n|[[:" + item['namespace_text'] + ":" + o_title + "|" + item[
            #     'namespace_text'] + ":" + o_title + "]] \n|~ \n|"

        text += "\n"
    text += "\n"
    text += """|}"""
    main_text += "\n" + text + "\n"

site = pywikibot.Site()
# print(main_text)
page = pywikibot.Page(site, "مستخدم:لوقا/ملعب 52")
page.text = main_text
page.save("انشاء")
