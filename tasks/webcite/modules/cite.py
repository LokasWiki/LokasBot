import traceback
import urllib.parse

from waybackpy.exceptions import NoCDXRecordFound, TooManyRequestsError
from datetime import datetime, timedelta

from tasks.webcite.data import list_of_template,web_type,press_release_type
from tasks.webcite.modules.cites.webcite import WebCite
from tasks.webcite.modules.cites.press_release import PressRelease

from waybackpy import WaybackMachineCDXServerAPI
from waybackpy import WaybackMachineSaveAPI


class Archive:
    def __init__(self, url, timestamp):
        self.url = url
        self.timestamp = timestamp


class Cite:
    def __init__(self, template):

        self.list_of_templates = list_of_template
        self.template = self._set_right_class(template)
        self.url = self.template.url()

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        self.archive_object = None

    def _set_right_class(self, template):
        for t in self.list_of_templates:
            if str(t[0]).strip().lower() == str(template.name).strip().lower():
                class_name = t[1].strip().lower()
                print(class_name)
                if class_name == web_type:
                    return WebCite(template)
                elif class_name == press_release_type:
                    return PressRelease(template)

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

        cdx_api = WaybackMachineCDXServerAPI(self.url.value.strip(), self.user_agent)
        try:
            newest = cdx_api.newest()
            # check if the date is before 5 minutes from now
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if not (newest.datetime_timestamp < five_minutes_ago) and (newest.statuscode == 200):
                self.archive_object = Archive(urllib.parse.unquote(newest.archive_url), newest.timestamp)

        except Exception as e:

            print(f"An error occurred while processing: {e} and url is {self.url.value.strip()}")

            # just_the_string = traceback.format_exc()
            #
            # print(just_the_string)

    def archive_it(self):
        self.check_available_on_api()

        if self.archive_object is None:
            try:

                save_api = WaybackMachineSaveAPI(self.url.value.strip(), self.user_agent)
                self.archive_object = Archive(urllib.parse.unquote(save_api.save()), str(save_api.timestamp().strftime('%Y%m%d%H%M%S')))
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
