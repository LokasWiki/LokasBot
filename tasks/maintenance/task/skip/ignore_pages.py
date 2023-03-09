import os

import pywikibot
import wikitextparser as wtp
from core.utils.helpers import prepare_str
from core.utils.file import File
site = pywikibot.Site()

page_name = "مستخدم:LokasBot/تجاهل مهمة صيانة المقالات"

page = pywikibot.Page(site, page_name)

if page.exists():
    parsed = wtp.parse(page.text)
    wikilinks = []
    for link in parsed.wikilinks:
        wikilinks.append(link.title)

    home_path = os.path.expanduser("~")
    file = File(script_dir=home_path)
    file_path = prepare_str('maintenance_skip.txt')
    file.set_stub_path(file_path)
    file.set_json_content(wikilinks)