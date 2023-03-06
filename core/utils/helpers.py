import pywikibot


def check_status(name):
    site = pywikibot.Site()
    title = name
    page = pywikibot.Page(site, title)
    text = page.text
    if text == "لا":
        return True
    return False


def prepare_str(string):
    return str(string).strip().lower().replace(" ", "_")
