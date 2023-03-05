"""
This module contains classes related to creating and updating citations.

Classes:
Archive: A class for storing information about an archived webpage.
Cite: A class for creating and updating citations using templates.
"""

import traceback

import requests
from waybackpy.exceptions import TooManyRequestsError
from datetime import datetime, timedelta

from tasks.webcite.data import list_of_template, web_type, press_release_type, newsgroup_type, news_type, map_type
from tasks.webcite.modules.cites.map import CiteMap
from tasks.webcite.modules.cites.news import News
from tasks.webcite.modules.cites.newsgroup import Newsgroup
from tasks.webcite.modules.cites.webcite import WebCite
from tasks.webcite.modules.cites.press_release import PressRelease

from waybackpy import WaybackMachineCDXServerAPI
from waybackpy import WaybackMachineSaveAPI


class Archive:
    """
    A class for storing information about an archived webpage.

    Attributes:
    - url (str): The URL of the archived webpage.
    - timestamp (str): The timestamp of the archived webpage.
    """
    def __init__(self, url, timestamp):
        self.url = url
        self.timestamp = timestamp


class Cite:
    """
    A class for creating and updating citations using templates.

    Attributes:
        - list_of_templates (list): A list of available templates.
        - template: The template used for creating the citation.
        - url (str): The URL of the citation.
        - user_agent (str): The user agent used when interacting with the Wayback Machine.
        - archive_object (Archive): The archived version of the citation.
    """
    def __init__(self, template):

        self.list_of_templates = list_of_template
        self.template = self._set_right_class(template)
        self.url = self.template.url()

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        self.archive_object = None

    def _set_right_class(self, template):
        """
        Sets the right Cite class based on the type of template.

        Args:
            template: WebpageTemplate object.

        Returns:
            Cite object.
        """
        for t in self.list_of_templates:
            if str(t[0]).lower().strip().replace(" ","_") == str(template.name).lower().strip().replace(" ","_"):
                class_name = t[1].strip().lower()
                if class_name == web_type:
                    return WebCite(template)
                elif class_name == press_release_type:
                    return PressRelease(template)
                elif class_name == newsgroup_type:
                    return Newsgroup(template)
                elif class_name == news_type:
                    return News(template)
                elif class_name == map_type:
                    return CiteMap(template)

    def is_archived(self):
        """
        Checks if the webpage is already archived.

        Returns:
            Boolean value, True if webpage is archived, else False.
        """
        return self.template.is_archived()

    def check_available(self):
        """
        Checks if the webpage URL is valid.

        Returns:
            Boolean value, True if URL is valid, else False.
        """
        if self.url is not None and self.url.value.strip() is not None:
            return self.is_url_excluded(self.url.value.strip())
        return None

    def is_url_excluded(self, url):
        sites = [
            'archive.org',
            'web.archive.org',
            'mail.yahoo.com',
            'duckduckgo.com/?q=',
            'google.com/search',
            '127.0.0.1',
            'localhost',
            '0.0.0.0',
            'chrome:',
            'chrome-extension:',
            'about:',
            'moz-extension:',
            'file:',
            'edge:',
            'extension:',
            'safari-web-extension:',
            'chrome-error:'
        ]
        status = True
        for site in sites:
            if site.lower().strip().replace(" ","_") in url.lower().strip().replace(" ","_"):
                status = None
        return status
    def check_available_on_api(self):
        """
        Checks if the webpage is available on Wayback Machine API
        and returns the archived URL and timestamp if
        available.

        If the citation is available, an Archive object is created
        and stored in self.archive_object.

        Returns:
        - None.
        """
        cdx_api = WaybackMachineCDXServerAPI(self.url.value.strip(), self.user_agent)
        try:
            newest = cdx_api.newest()
            # check if the date is before 5 minutes from now
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if not (newest.datetime_timestamp < five_minutes_ago) and (newest.statuscode == 200):
                self.archive_object = Archive(newest.archive_url, newest.timestamp)

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
                r = requests.get(save_api.save())
                if r.status_code == 200:
                    self.archive_object = Archive(save_api.save(),
                                                  str(save_api.timestamp().strftime('%Y%m%d%H%M%S')))
            except TooManyRequestsError as error:
                print(f"An error occurred while send link to archive site processing: {error}")
                just_the_string = traceback.format_exc()
                print(just_the_string)
            except Exception as error:
                print(f"An error occurred while processing: {error}")
                just_the_string = traceback.format_exc()
                print(just_the_string)

    def update_template(self):

        if self.archive_object is not None:
            self.template.update_template(self.archive_object.url, self.archive_object.timestamp)
