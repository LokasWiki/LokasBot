import copy

import pywikibot
import wikitextparser as wtp

from core.utils.helpers import prepare_str

site = pywikibot.Site()

page_title = "ألان روبر"
page = pywikibot.Page(site, page_title)

parsed_text = wtp.parse(page.text)
cat_name = "أشخاص مصابون بمرض آلزهايمر"

temp_text = copy.deepcopy(page.text)

for link in parsed_text.wikilinks:
    if link.title.startswith("تصنيف:"):
        if prepare_str(link.title.replace("تصنيف:", "")) == prepare_str(cat_name):
            temp_text = str(temp_text).replace(str(link), "")

print(temp_text)
