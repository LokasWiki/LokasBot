from waybackpy.exceptions import NoCDXRecordFound
from datetime import datetime, timedelta

from tasks.webcite.modules.cites.webcite import WebCite
from waybackpy import WaybackMachineCDXServerAPI


class Cite:
    def __init__(self, template):

        if template is None:
            self.template = WebCite(template)
        else:
            self.template = template

        self.url = self.template.url()

        self.user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
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
        cdx_api = WaybackMachineCDXServerAPI(self.url.value, self.user_agent)
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
