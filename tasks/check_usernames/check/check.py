import os

import pywikibot

from core.utils.file import File
from core.utils.helpers import prepare_str, check_status
from modules import ReadUsers, Category
from tasks.check_usernames.load.load import Load


# todo:move to core
class Check:
    def __init__(self, site, page_title):
        self.page_title = page_title
        self.site = site
        self.text = None
        self.page = None

    def load(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        if self.page.exists():
            self.text = self.page.text

    def check(self):
        if self.text is not None:
            if prepare_str(self.text) == prepare_str("نعم"):
                return True
        return False

    def reload(self):
        self.page.text = ""
        self.page.save("بوت:تم  V2.1.0")


def main(*args: str) -> int:
    try:
        if check_status("مستخدم:LokasBot/إخطار الإداريين/أسماء مستخدمين للفحص"):
            site = pywikibot.Site()

            check_page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت"
            check_page = Check(site=site, page_title=check_page_title)
            check_page.load()
            if check_page.check():
                # create only if check page is true
                # https://ar.wikipedia.org/w/index.php?title=%D9%86%D9%82%D8%A7%D8%B4_%D9%88%D9%8A%D9%83%D9%8A%D8%A8%D9%8A%D8%AF%D9%8A%D8%A7:%D8%A5%D8%AE%D8%B7%D8%A7%D8%B1_%D8%A7%D9%84%D8%A5%D8%AF%D8%A7%D8%B1%D9%8A%D9%8A%D9%86/%D8%A3%D8%B3%D9%85%D8%A7%D8%A1_%D9%85%D8%B3%D8%AA%D8%AE%D8%AF%D9%85%D9%8A%D9%86_%D9%84%D9%84%D9%81%D8%AD%D8%B5&oldid=62429509#17_%D9%85%D8%A7%D9%8A%D9%88!
                category = Category(site=site)
                category.create()

                check_page.reload()
                read_users_page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"
                # read_users_page_title= "مستخدم:لوقا/ملعب 20"
                read_users = ReadUsers(site=site, page_title=read_users_page_title, cat_name=category.cat_name)
                read_users.load_page()
                read_users.parse_table()
                read_users.start_send_alert()

                # new code to remove table after send alert
                # note this code under test
                page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"
                names = []

                script_dir = os.path.dirname(__file__)

                # text stub
                file = File(script_dir=script_dir)
                file_path = 'stub/load.txt'
                file.set_stub_path(file_path)
                file.get_file_content()
                content = file.contents

                load_obj = Load(content_text=content, names=names, page_title=page_title, site=site)
                load_obj.load_page().build_table().save_page()
        else:
            print("check wiki site")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
