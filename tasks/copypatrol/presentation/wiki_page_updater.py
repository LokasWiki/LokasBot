import pywikibot


class WikiPageUpdater:
    def __init__(self, site, page_name):
        """
        Initializes a new instance of the `WikiPageUpdater` class.

        Args:
            site (str): The name of the wiki site.
            page_name (str): The name of the page to be updated.

        Initializes the `site` attribute with the given `site` parameter, and the `page_name` attribute with the given `page_name` parameter.

        """
        self.site = pywikibot.Site(site)
        self.page_name = page_name

    def update_page(self, open_cases_count: int):
        """
        Updates a wiki page with the given number of open cases.

        Args:
            open_cases_count (int): The number of open cases.

        Returns:
            None

        This method retrieves the wiki page specified by `self.page_name` and updates its text with the number of open cases. The updated text includes a link to the copypatrol tool and the number of open cases. The text also includes a noinclude section that includes a category for wiki maintenance templates. The updated text is then saved with the message "تحديث v1.0.0" (Update v1.0.0 in Arabic).
        """
        page = pywikibot.Page(self.site, self.page_name)
        text = """[https://copypatrol.toolforge.org/ar/ أداة كشف خرق حقوق النشر] (OPENEDNUMBER)

<noinclude>
[[تصنيف:قوالب صيانة ويكيبيديا]]
</noinclude>"""
        text = text.replace("OPENEDNUMBER", str(open_cases_count))
        page.text = text
        page.save("تحديث v2.0.0")
