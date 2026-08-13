import datetime
import logging

import pywikibot


def check_status(name):
    site = pywikibot.Site()
    title = name
    page = pywikibot.Page(site, title)
    if page.exists():
        text = page.text
        if text == "لا":
            return True
    else:
        return True
    return False


def prepare_str(string):
    # .replace("  ", "_")  with two space to fix many space in name like  {{فنانون      تشكيليون سعوديون}}
    return str(string).strip().lower().replace("  ", "_").replace(" ", "_")


def is_valid_title(title):
    """Return True if the given title is a valid MediaWiki title (no illegal characters)."""
    if title is None:
        return False
    title = str(title).strip()
    if not title:
        return False
    # MediaWiki illegal title characters: # < > [ ] | { }
    illegal_chars = set("#<>[]|{}")
    return not any(ch in title for ch in illegal_chars)


def check_edit_age(page, number_of_hours=3):
    status = False
    try:
        # Get first revision
        revisions = page.revisions(reverse=True, total=1)
        first_edit = None
        for revision in revisions:
            first_edit = revision['timestamp']
            break
        # Get the current time
        current_time = datetime.datetime.utcnow()

        # Calculate the difference between the timestamp and the current time
        time_difference = current_time - first_edit

        # Check if the time difference is less than 3 hours
        if time_difference > datetime.timedelta(hours=number_of_hours):
            status = True
    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)

    return status
