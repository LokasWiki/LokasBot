import os

import pywikibot

from core.utils.file import File
from modules import ReadUsers, Category
from tasks.check_usernames.load.load import Load


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
            if self.text.strip().lower() == "نعم".strip().lower():
                return True
        return False

    def reload(self):
        self.page.text = ""
        self.page.save("بوت:تم")


def main(*args: str) -> int:
    try:
        site = pywikibot.Site()

        category = Category(site=site)
        category.create()

        check_page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت"
        check_page = Check(site=site, page_title=check_page_title)
        check_page.load()
        if check_page.check():
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

    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
