from tasks.webcite.modules.cite import Cite
from tasks.webcite.modules.cites.webcite import WebCite
import wikitextparser as wtp

url = "https://lokasbot.toolforge.org/pages"
template = """{{استشهاد ويب
        | عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
        | موقع = www.alarabiya.net
        | url = https://ar.wikipedia.org/wiki/%D9%85%D8%B3%D8%AA%D8%AE%D8%AF%D9%85:LokasBot
        }}"""

parser = wtp.Template(template)
webcite = WebCite(parser)
cite = Cite(webcite)
print(cite.url.value)
if cite.is_archived() is False:
    cite.archive_it()
print(cite.archive_object)
cite.update_template()
# print(cite.archive_object.archive_url)
