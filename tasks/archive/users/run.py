import pywikibot

site = pywikibot.Site()

template_name = "قالب:أرشفة آلية"

template = pywikibot.Page(site, template_name)

gen = template.embeddedin(filter_redirects=False, namespaces=3)

for user_talk in gen:
    if user_talk.depth == 0 and user_talk.has_permission(action='edit'):
        print(user_talk)
