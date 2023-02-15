import pywikibot

from core.utils.lua_to_python import save_lue_table, portal_aliases_file_name

site = pywikibot.Site()

page_name = "وحدة:Portal/images/aliases"

page = pywikibot.Page(site, page_name)

if page.exists():
    save_lue_table(portal_aliases_file_name,page.text)
