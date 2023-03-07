import os

import pywikibot
import wikitextparser as wtp
from core.utils.helpers import prepare_str
from core.utils.file import File
site = pywikibot.Site()

page_name = "ويكيبيديا:AutoWikiBrowser/Template redirects"

page = pywikibot.Page(site, page_name)

if page.exists():
    parsed = wtp.parse(page.text)
    wikilist = parsed.get_lists()
    wikilist_items = []
    templates = []
    for l in wikilist:
        for item in l.items:
            wikilist_items.append(item)
    for wikilist_item in wikilist_items:
        from_str, to_str = wikilist_item.strip().split("→", 1)
        parsed_from_templates = wtp.parse(from_str)
        to_template = wtp.Template(str(to_str).replace("'''", ""))
        for from_template in parsed_from_templates.templates:
            try:
                if prepare_str(from_template.name) == prepare_str("tl"):
                    templates.append([from_template.arguments[0].value, to_template.arguments[0].value])
            except:

                print("skip one " + from_str)
    home_path = os.path.expanduser("~")
    file = File(script_dir=home_path)
    file_path = prepare_str('Template_redirects.txt')
    file.set_stub_path(file_path)
    file.set_json_content(templates)