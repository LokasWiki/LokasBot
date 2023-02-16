from tasks.webcite.modules.cite import Cite
from tasks.webcite.modules.cites.webcite import WebCite
import wikitextparser as wtp

url = "https://lokasbot.toolforge.org/pages"
template = """{{استشهاد ويب
        | عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
        | موقع = www.alarabiya.net
        | url = https://www.w3schools.com/python/python_try_except.asp
        }}"""

parser = wtp.Template(template)
webcite = WebCite(parser)
cite = Cite(webcite)
print(cite.url.value)
print(cite.is_archived())
print(cite.archive_object)
print(cite.archive_object.archive_url)