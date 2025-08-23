
import wikitextparser as wtp


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


site = pywikibot.Site()
list_page_name = "ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا/الأسبوع ال21 2023/مقالات"
template_stub = "{{وسام كاتب الأسبوع|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد إنشاء المقالات|USER_NAME}}"
list_page = pywikibot.Page(site, list_page_name)
parsed = wtp.parse(list_page.text)
users_template = parsed.templates[1:]
translator = Translator()
rank = 1
current_score = None
for score, user in enumerate(users_template):
    name = user.arguments[0].value
    # Retrieve the user talk page
    user = pywikibot.User(site, name)

    if score != current_score:
        rank = rank + 1
        current_score = score
    if rank > 6:
        break

    # Get the user page for the user
    talk_page = user.getUserTalkPage()

    # Add a new section to the page
    text = talk_page.text
    text += '\n\n== تهانينا ==\n\n'
    text += template_stub.replace('YEAR_NUMBER', str(2023)).replace("WEEK_NUMBER",
                                                                    str(21)).replace(
        "RANK", translator.translate_rank(str(rank - 1))).replace("USER_NAME", name)

    text += "\n~~~~"
    try:
        # Save the edited page

        talk_page.text = text

        # Save the page
        talk_page.save(
            "بوت:[[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مستخدمو الأسبوع الأكثر نشاطا]]",
            minor=False
        )
    except Exception as error:
        print(f'Error saving page: {error}')
