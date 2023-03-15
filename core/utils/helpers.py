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
    #.replace("  ", "_")  with two space to fix many space in name like  {{فنانون      تشكيليون سعوديون}}
    return str(string).strip().lower().replace("  ", "_").replace(" ", "_")
