import pywikibot

from tasks.archive.users.module import template_name, read_archive_template

site = pywikibot.Site()

template = pywikibot.Page(site, f"قالب:{template_name}")

gen = template.embeddedin(filter_redirects=False, namespaces=3, content=True)

for user_talk in gen:
    if user_talk.depth == 0:
        print(user_talk)
        template_type, template_value = read_archive_template(page_text=user_talk.text,
                                                              archive_template_name=template_name)
        print(template_type, template_value)
