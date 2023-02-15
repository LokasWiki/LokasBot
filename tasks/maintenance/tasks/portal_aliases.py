import pywikibot

from core.utils.lua_to_python import LuaToPython

site = pywikibot.Site()

page_name = "وحدة:Portal/images/aliases"

page = pywikibot.Page(site, page_name)


converter = LuaToPython(page.text)
result_dict = converter.data

converter.search("سريان")
