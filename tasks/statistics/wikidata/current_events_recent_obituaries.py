from datetime import datetime

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
#  main query
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
#  connect to wikidata
repo = wiki_site.data_repository()

generator = pagegenerators.PreloadingEntityGenerator(pagegenerators.WikidataSPARQLPageGenerator(query, site=repo))

#  start add item to list
list_of_items = []

for item in generator:
    #  we add unix timestamp to make sort desc cos order by of query not work
    # todo: find better a way to make sort
    try:
        date_of_death = item.claims.get('P570')  # Assuming 'P570' is the property for date of death
        if date_of_death:
            date_string = date_of_death[0].getTarget()
            unix_timestamp_string = f"{date_string.year}-{date_string.month}-{date_string.day} 00:00:00"
            unix_timestamp = datetime.strptime(unix_timestamp_string, "%Y-%m-%d %H:%M:%S").timestamp()
            list_of_items.append((item.id, unix_timestamp))
        else:
            print("No date of death found for", item.id)
    except Exception as e:
        print(e)
#  sort item desc
sorted_items_desc = sorted(list_of_items, key=lambda x: x[1], reverse=False)
#  show only fisrt 20 items
index = 0
for row in sorted_items_desc:
    #  to add only 20
    if index == 20:
        break
    index += 1
    id = row[0]

    wiki_page_text += "\n"
    wiki_page_text += """ {{بوابة:أحداث جارية/شريط جانبي/وفيات حديثة/قالب | qid =  WIKI_ITEM }} """.replace("WIKI_ITEM",
                                                                                                            id)
# start save page
wiki_page_text += """
{{Wikidata list end}}
<noinclude>
[[تصنيف:بوابة أحداث جارية|أحداث جارية/شريط جانبي/وفيات حديثة]]
[[تصنيف:إحصاءات يحدثها LokasBot]]
</noinclude>
"""

page_obj = pywikibot.Page(wiki_site, wiki_page_title)
page_obj.text = wiki_page_text

page_obj.save(summary="Wikidata list updated (v0.0.2)")
