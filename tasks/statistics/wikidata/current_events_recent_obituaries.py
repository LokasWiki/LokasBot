import pywikibot
from pywikibot import pagegenerators

wiki_site = pywikibot.Site("ar", "wikipedia")
wikidata_site = pywikibot.Site("wikidata", "wikidata")
wiki_page_title = "بوابة:أحداث جارية/شريط جانبي/وفيات حديثة"
wiki_page_text = """{{Wikidata list
|hidetext=yes
|sparql=SELECT ?item
WHERE { values ?offset {"1920-02-00T00:00:00"^^xsd:dateTime }. values ?offset0 { "1920-01-00T00:00:00"^^xsd:dateTime }.
       Bind((NOW() - ?offset) as ?mintime). 
       ?item wdt:P570 ?dod . 
       FILTER EXISTS { ?war schema:about ?item . ?war schema:inLanguage "ar" }
       FILTER (?dod > "2020-10-01T00:00:00Z"^^xsd:dateTime) 
       FILTER (?dod < now())  Bind(((?dod - ?offset0)) as ?dodtime ).  
       FILTER (  ?dodtime > ?mintime ) ?item wdt:P31 wd:Q5 } 
ORDER BY DESC(?dod)
LIMIT 20
|columns=qid
|links=text
|skip_table=1
|row_template=بوابة:أحداث جارية/شريط جانبي/وفيات حديثة/قالب
|page=بوابة:أحداث جارية/شريط جانبي/وفيات حديثة
}}"""
query = '''
SELECT ?item
WHERE { values ?offset {"1920-02-00T00:00:00"^^xsd:dateTime }. values ?offset0 { "1920-01-00T00:00:00"^^xsd:dateTime }.
       Bind((NOW() - ?offset) as ?mintime). 
       ?item wdt:P570 ?dod . 
       FILTER EXISTS { ?war schema:about ?item . ?war schema:inLanguage "ar" }
       FILTER (?dod > "2020-10-01T00:00:00Z"^^xsd:dateTime) 
       FILTER (?dod < now())  Bind(((?dod - ?offset0)) as ?dodtime ).  
       FILTER (  ?dodtime > ?mintime ) ?item wdt:P31 wd:Q5 } 
ORDER BY DESC(?dod)
LIMIT 20
'''
repo = wiki_site.data_repository()

generator = pagegenerators.PreloadingEntityGenerator(pagegenerators.WikidataSPARQLPageGenerator(query, site=repo))

list_of_items = []

for item in generator:
    list_of_items.append(item.id)

for id in list_of_items:
    wiki_page_text += "\n"
    wiki_page_text += """ {{بوابة:أحداث جارية/شريط جانبي/وفيات حديثة/قالب | qid =  WIKI_ITEM }} """.replace("WIKI_ITEM",
                                                                                                            id)

wiki_page_text += """
{{Wikidata list end}}
<noinclude>
[[تصنيف:بوابة أحداث جارية|أحداث جارية/شريط جانبي/وفيات حديثة]]
[[تصنيف:إحصاءات يحدثها LokasBot]]
</noinclude>
"""

page_obj = pywikibot.Page(wiki_site, wiki_page_title)
page_obj.text = wiki_page_text

page_obj.save(summary="Wikidata list updated")
