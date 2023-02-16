from waybackpy.exceptions import NoCDXRecordFound
from datetime import datetime, timedelta
from urllib.parse import quote

from tasks.webcite.modules.cites.webcite import WebCite

from waybackpy import WaybackMachineCDXServerAPI
from waybackpy import WaybackMachineSaveAPI

class Cite:
    def __init__(self, template):

        if template is None:
            self.template = WebCite(template)
        else:
            self.template = template

        self.url = self.template.url()

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        self.archive_object = None

    def is_archived(self):
        return self.check_available()

    def check_available(self):
        if self.template.url() is not None:
            status, archive_obj = self.check_available_on_api()
            self.archive_object = archive_obj
            return status
        return False

    def check_available_on_api(self):
        encoded_url = quote(str(self.url.value).strip().lower(), safe=':/?=&')
        cdx_api = WaybackMachineCDXServerAPI(encoded_url, self.user_agent)
        found = False
        archive_obj = None
        try:
            newest = cdx_api.newest()
            date_str = str(newest.timestamp)
            date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S')

            # check if the date is before 6 months from now
            six_months_ago = datetime.now() - timedelta(days=30 * 6)
            if date_obj < six_months_ago:
                found = False
            else:
                # newest.archive_url
                found = True
                archive_obj = newest

        except NoCDXRecordFound:
            found = False
        return found, archive_obj

    def archive_it(self):
        encoded_url = quote(str(self.url.value).strip().lower(), safe=':/?=&')
        save_api = WaybackMachineSaveAPI(encoded_url, self.user_agent)
        self.archive_object = save_api.save()

    def update_template(self):
        self.template.update_template(self.archive_object.archive_url,self.archive_object.timestamp)