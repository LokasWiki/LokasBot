import pywikibot

from tasks.infobox_football_biography.src.data_extraction.templates.infobox_football_biography import \
    InfoboxFootballBiography
from tasks.infobox_football_biography.src.football_player_bot import FootballPlayerBot

bot = FootballPlayerBot()

site = pywikibot.Site("en", "wikipedia")
page_title = "Paul_Abasolo"
page = pywikibot.Page(site, page_title)

template = InfoboxFootballBiography(
    logger=bot.getChainOfLoggers(),
    text_page=page.text
)

template.parse()
template.template_name()
template.parameters_list()
if template.check():
    template.list.sort(key=lambda x: x["name"])
