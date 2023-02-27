import pywikibot
import wikitextparser as wtp
import pywikibot.flow
from datetime import datetime
from pywikibot.data.api import Request

# todo: move this class to core and move tests files
class DateFormatter:
    """
    Utility class for formatting timestamps into human-readable dates.

    Args:
        language (str): Optional. The language of the formatted date string. Defaults to 'en'.

    Attributes:
        language (str): The language of the formatted date string.

    Methods:
        format_timestamp(timestamp: str) -> str:
            Formats a timestamp string into a human-readable date string according to the specified
            language. The timestamp string should be in the format 'YYYYMMDDHHMMSS'.

    Example usage:
        >>> formatter = DateFormatter()
        >>> formatter.format_timestamp('20220101000000')
        '01 January 2022'
    """

    def __init__(self, language: str = 'en'):
        self.language = language

    def format_timestamp(self, timestamp: str) -> str:
        """
        Formats a timestamp string into a human-readable date string according to the specified
        language.

        Args:
            timestamp (str): A timestamp string in the format 'YYYYMMDDHHMMSS'.

        Returns:
            str: A human-readable date string.

        Raises:
            ValueError: If the timestamp string is not in the correct format.
        """
        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        if self.language == 'ar':
            month_names = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                           'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
            month_name = month_names[dt.month - 1]
            formatted_date = f"{dt.day} {month_name} {dt.year}"
        else:
            formatted_date = dt.strftime('%d %B %Y')
        return formatted_date


class Category:
    def __init__(self, site):
        self.site = site
        self.cat_name = None
    def create(self):
        try:
            formatter = DateFormatter("ar")
            start_date = datetime.now()
            start_time_str = start_date.strftime("%Y%m%d%H%M%S")
            cat_date = formatter.format_timestamp(start_time_str)
            self.cat_name = f"تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع منذ {cat_date}"
            cat = pywikibot.Category(self.site, self.cat_name)
            cat.text = "{{تصنيف تهذيب شهري}}"
            cat.save("إنشاء تصنيف صيانة")
        except:
            print("failed to create category")


class SendAlert:
    def __init__(self, user_name, has_reason, reason, site,cat_name):
        self.user_name = user_name
        self.has_reason = has_reason
        self.cat_name = cat_name
        self.reason = reason
        self.site = site
        self.header = ""
        self.revisionId = None
        self.token= None
        self.page_title =None
    def start_send(self):
        # Retrieve the user talk page
        user = pywikibot.User(self.site, self.user_name)

        # Get the user page for the user
        talk_page = user.getUserTalkPage()
        self.page_title = talk_page.title(with_ns=True)
        if talk_page.is_flow_page():
            board = pywikibot.flow.Board(talk_page)

            # Add a new section to the page
            title = 'اسم المستخدم مخالف'
            if self.has_reason:
                content = "{{نسخ:تنبيه اسم مستخدم|REASON}}".replace("REASON", str(self.reason).strip())
            else:
                content = "{{نسخ:تنبيه اسم مستخدم}}"

            try:
                topic = board.new_topic(title, content)
                # add category to header
                self.get_header_text()

                self.header += """\n[[تصنيف:أسماء مستخدمين مخالفة مرشحة للمنع]]\n[[CAT_NAME|{{اسم_الصفحة_الأساسي}}]]\n""".replace("CAT_NAME",self.cat_name)
                self.token = self.site.tokens["edit"]
                self.save_flow_header()

            except Exception as error:
                print(f'Error saving page: {error}')

        else:
            pass
            # Add a new section to the page
            text = talk_page.text
            text += '\n'
            if self.has_reason:
                text += "{{نسخ:تنبيه اسم مستخدم|REASON}}----[[مستخدم:Dr-Taher|Dr-Taher]] ([[نقاش المستخدم:Dr-Taher|نقاش]]) {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)".replace(
                    "REASON", str(self.reason).strip())
            else:
                text += "{{نسخ:تنبيه اسم مستخدم}}----[[مستخدم:Dr-Taher|Dr-Taher]] ([[نقاش المستخدم:Dr-Taher|نقاش]]) {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)"

            try:
                # Save the edited page
                talk_page.text = text
                # Save the page
                talk_page.save(summary="بوت:تنبيه اسم مخالف", minor=False)
            except Exception as error:
                print(f'Error saving page: {error}')

    def get_header_text(self):

        params = {
            "action": "flow",
            "format": "json",
            "submodule": "view-header",
            "page": self.page_title,
            "utf8": 1,
            "formatversion": "2",
            "vhformat": "wikitext"
        }
        # Create a custom API request
        request = Request(site=self.site, parameters=params)
        # Send the request to the API and get the response
        data = request.submit()
        # Extract the header information from the API response
        try:
            self.header = data['flow']['view-header']['result']['header']['revision']['content']['content']
            self.revisionId = data['flow']['view-header']['result']['header']['revision']['revisionId']
        except:
            self.header = ""
            self.revisionId = data['flow']['view-header']['result']['header']['revision']['revisionId']

    def save_flow_header(self):
        """
        Get the header information of a Flow page using the Pywikibot API.

        :param page_title: the title of the Flow page
        :return: a dictionary containing the header information
        """
        # Set up the site and API parameters
        site = pywikibot.Site()
        params = {
            "action": "flow",
            "format": "json",
            "submodule": "edit-header",
            "page": self.page_title,
            "utf8": 1,
            "formatversion": "2",
            "ehprev_revision": self.revisionId,
            "ehcontent": self.header,
            "vhformat": "wikitext",
            "token": self.token,  # get the edit token
        }

        # Create a custom API request
        request = Request(site=self.site, parameters=params, use_get=False)

        # Send the request to the API and get the response
        data = request.submit()

        # todo:add check error here



class ReadUsers:
    def __init__(self, site, page_title,cat_name):
        self.page = None
        self.cat_name = cat_name
        self.parsed = None
        self.site = site
        self.page_title = page_title
        self.text = None
        self.users = []

    def load_page(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        self.text = self.page.text
        self.parsed = wtp.parse(str(self.text))

    def parse_table(self):
        table = self.parsed.tables[0].data()
        for row in table:
            reason = row[4]
            status = row[3]
            user = row[2]
            if status.strip().lower() == str("نعم").strip().lower():
                t = wtp.Template(user)
                user_dic = {
                    "reason": reason,
                    "has_reason": not (str(reason).strip().lower() == str("")),
                    "user_template": user,
                    "username": t.arguments[0].value.strip()
                }
                self.users.append(user_dic)

    def start_send_alert(self):
        for user in self.users:
            try:
                send_obj = SendAlert(user['username'], user['has_reason'], user['reason'], site=self.site,cat_name=self.cat_name)
                send_obj.start_send()
            except:
                print("can`t send  alert")
