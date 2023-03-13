import os

import pywikibot
import wikitextparser as wtp
from core.utils.helpers import prepare_str
from core.utils.file import File
site = pywikibot.Site()

page_name = "ويكيبيديا:AutoWikiBrowser/Rename template parameters"

page = pywikibot.Page(site, page_name)

if page.exists():
    parsed = wtp.parse(page.text)
    templates_items = []
    templates = []

    # keep AWB rename template parameter template
    for template in parsed.templates:
        if prepare_str(template.name) == prepare_str("AWB rename template parameter"):
            templates_items.append(template)

    for template_item in templates_items:

        search_key = template_item.arguments[0].value.strip()
        search_range = [template_item.arguments[1].value.strip(), template_item.arguments[2].value.strip()]

        # Loop through the outer list and check if the search_key is present in the first element of any of the inner lists
        for inner_list in templates:
            if inner_list[0] == search_key:
                # If the key is found, check if the search_range is present in the second element of the inner list
                if search_range in inner_list[1]:
                    pass
                    # print("Range found in the list")
                else:
                    # If the range is not found, append it to the second element of the inner list
                    inner_list[1].append(search_range)
                    # print("Range not found. Added to the list.")
                break
        else:
            # If the key is not found, append a new inner list to the outer list with the key and the search_range
            templates.append([search_key, [search_range]])
            # print("Key not found. Added to the list.")

    home_path = os.path.expanduser("~")
    file = File(script_dir=home_path)
    file_path = prepare_str('rename_template_parameters.txt')
    file.set_stub_path(file_path)
    file.set_json_content(templates)