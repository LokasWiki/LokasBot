import traceback

from waybackpy.exceptions import NoCDXRecordFound, TooManyRequestsError
from datetime import datetime, timedelta

from tasks.webcite.data import list_of_template
from tasks.webcite.modules.cites.webcite import WebCite

from waybackpy import WaybackMachineCDXServerAPI
from waybackpy import WaybackMachineSaveAPI


class Archive:
    def __init__(self, url, timestamp):
        self.url = url
        self.timestamp = timestamp


class Cite:
    def __init__(self, template):

        self.list_of_templates = []
        self.template = self._set_right_class(template)
        self.url = self.template.url()

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        self.archive_object = None

    def _fill_all_template(self):
        for dic in list_of_template:
            for template in dic['list_of_template']:
                self.list_of_templates.append(template)

    def _set_right_class(self, template):
        self._fill_all_template()
        for t in self.list_of_templates:
            if str(t).strip().lower() == str(template.name).strip().lower():
                return WebCite(template)

    def is_archived(self):
        return self.template.is_archived()

    def check_available(self):
        pass
        # try:
        #     if self.template.url() is not None:
        #         status, archive_obj = self.check_available_on_api()
        #         self.archive_object = archive_obj
        #         return status
        # except AttributeError:
        #     print(" 'Template' object has no attribute 'url'")
        # return False

    def check_available_on_api(self):
        # encoded_url = quote(str(self.url.value).strip().lower(), safe=':/?=&')
        encoded_url = str(self.url.value).strip().lower()
        cdx_api = WaybackMachineCDXServerAPI(encoded_url, self.user_agent)
        try:
            newest = cdx_api.newest()
            # check if the date is before 5 minutes from now
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if not (newest.datetime_timestamp < five_minutes_ago) and (newest.statuscode == 200):
                self.archive_object = Archive(newest.archive_url, newest.timestamp)

        except Exception as e:

            print(f"An error occurred while processing: {e} and url is {encoded_url}")

            # just_the_string = traceback.format_exc()
            #
            # print(just_the_string)

    def archive_it(self):
        self.check_available_on_api()

        if self.archive_object is None:
            try:
                encoded_url = str(self.url.value).strip().lower()

                save_api = WaybackMachineSaveAPI(encoded_url, self.user_agent)
                self.archive_object = Archive(save_api.save(), str(save_api.timestamp().strftime('%Y%m%d%H%M%S')))
            except TooManyRequestsError as e:
                # todo:add option to database
                just_the_string = traceback.format_exc()
                print(just_the_string)
                print("ip well blocked now stop run bot for 6 minutes")
                # time.sleep(60*6)
            except Exception as e:
                print(f"An error occurred while processing: {e}")
                just_the_string = traceback.format_exc()
                print(just_the_string)

    def update_template(self):

        if self.archive_object is not None:
            self.template.update_template(self.archive_object.url, self.archive_object.timestamp)
