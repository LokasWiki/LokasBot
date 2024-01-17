import wikitextparser as wtp
import pywikibot

from core.utils.helpers import prepare_str


class UnreviewedArticle:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.templates = [
            "مقالة غير مراجعة"
        ]

    def __call__(self):
        # todo:add try here for check def
        if not self.check():
            self.add_template()
        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{مقالة غير مراجعة}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        found = False
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    found = True
                    break

        if not found:
            new_text = "{{مقالة غير مراجعة|تاريخ ={{نسخ:شهر وسنة}}}}"
            new_text += "\n"
            new_text += self.text

            self.text = new_text
            self.summary += "، أضاف وسم مقالة غير مراجعة"

    def remove_template(self):
        """
           This method removes the {{مقالة غير مراجعة}} template from the page if it exists.
           """
        parsed = wtp.parse(self.text)
        new_text = self.text
        for needed_template in self.templates:
            for template in parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، حذف وسم مقالة غير مراجعة"

    def check(self):
        """
        The check() method is used to check if the current page has been reviewed or not. It does this by making an API
         request to the Wikipedia server using the pywikibot library. The method takes no arguments and returns a Boolean
          value of True if the page has been flagged as reviewed, and False otherwise.

The method starts by defining a dictionary params which contains the parameters for the API request. These include the
action to be performed, the format of the response, the properties to be returned, and the title of the page we want to
 check.

Next, the method creates a Request object using the pywikibot.data.api.Request class, passing in the site object and the
 params dictionary as arguments. This object is then used to submit the API request.

The response from the API is then parsed and the flagged property is checked in the pages section of the response.
If the flagged property is present and has a value of True, this means the page has been reviewed and the method returns True.
 If the flagged property is not present or has a value of False, the page has not been reviewed and the method returns False.
        :return:
            bool: to check if the current page has been reviewed or not
        """
        params = {
            "action": "query",
            "format": "json",
            "prop": "info|flagged",
            "titles": self.page.title(),
            "formatversion": 2
        }

        request = pywikibot.data.api.Request(site=self.page.site, **params)
        data = request.submit()
        pages = data["query"]["pages"]
        for page in pages:
            if "flagged" in page:
                if page["flagged"]:
                    return True
        return False
