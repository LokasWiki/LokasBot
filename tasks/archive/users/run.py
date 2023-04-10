import pywikibot

site = pywikibot.Site()

template_name = "قالب:أرشفة آلية"

template = pywikibot.Page(site, template_name)

gen = template.embeddedin(filter_redirects=False, namespaces=3)

for user_take in gen:
    if user_take.depth == 0:
        print(user_take)
