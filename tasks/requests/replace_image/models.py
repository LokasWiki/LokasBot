import copy

import pywikibot
import wikitextparser as wtp

from core.utils.helpers import prepare_str


class ImageReplacer:
    def __init__(self, site, page_name):
        self.site = site
        self.page_name = page_name
        self.page = pywikibot.Page(site, page_name)
        self.parsed = wtp.parse(self.page.text)
        self.temp_text = copy.deepcopy(self.page.text)
        self.template_list = [
            prepare_str("صورة صفحة رئيسية")
        ]

    def set_old_file_name(self, old_file_name):
        self.old_file_name = prepare_str(old_file_name)
        self.pure_old_file_name = old_file_name

    def set_new_file_name(self, new_file_name):
        self.new_file_name = prepare_str(new_file_name)
        self.pure_new_file_name = new_file_name

    def replace_image(self):
        for wikilink in self.parsed.wikilinks:
            # for ملف: namespace
            if wikilink.title.startswith("ملف:"):
                if prepare_str(wikilink.title) == prepare_str("ملف:" + self.old_file_name):
                    temp_wikilink = copy.deepcopy(wikilink)
                    temp_wikilink.title = "ملف:" + self.new_file_name
                    self.temp_text = self.temp_text.replace(str(wikilink), str(temp_wikilink))
            # for File: namespace
            elif wikilink.title.startswith("File:"):
                if prepare_str(wikilink.title) == prepare_str("File:" + self.old_file_name):
                    temp_wikilink = copy.deepcopy(wikilink)
                    temp_wikilink.title = "File:" + self.new_file_name
                    self.temp_text = self.temp_text.replace(str(wikilink), str(temp_wikilink))

    def replace_image_in_gallery_tag(self):
        for tag in self.parsed.get_tags("gallery"):
            tag_str = copy.deepcopy(tag.string).lower()
            # for ملف: namespace in
            if prepare_str("ملف:" + self.old_file_name) in prepare_str(tag_str):
                tag_str = tag_str.replace("ملف:" + self.pure_old_file_name.lower(), "ملف:" + self.pure_new_file_name)
                tag_str = tag_str.replace("ملف:" + self.old_file_name.lower(), "ملف:" + self.pure_new_file_name)
                self.temp_text = self.temp_text.replace(str(tag.string), str(tag_str))
        for tag in self.parsed.get_tags("gallery"):
            # for File: namespace in
            if prepare_str("File:" + self.old_file_name) in prepare_str(tag_str):
                tag_str = tag_str.replace("File:".lower() + self.pure_old_file_name.lower(),
                                          "File:" + self.pure_new_file_name)
                tag_str = tag_str.replace("File:".lower() + self.old_file_name.lower(),
                                          "File:" + self.pure_new_file_name)
                self.temp_text = self.temp_text.replace(str(tag.string), str(tag_str))

    def replace_image_in_imagemap_tag(self):
        for tag in self.parsed.get_tags("imagemap"):
            tag_str = copy.deepcopy(tag.string).lower()
            # for ملف: namespace in
            if prepare_str("ملف:" + self.old_file_name) in prepare_str(tag_str):
                tag_str = tag_str.replace("ملف:" + self.pure_old_file_name.lower(), "ملف:" + self.pure_new_file_name)
                tag_str = tag_str.replace("ملف:" + self.old_file_name.lower(), "ملف:" + self.pure_new_file_name)
                self.temp_text = self.temp_text.replace(str(tag.string), str(tag_str))
        for tag in self.parsed.get_tags("imagemap"):
            # for File: namespace in
            if prepare_str("File:" + self.old_file_name) in prepare_str(tag_str):
                tag_str = tag_str.replace("File:".lower() + self.pure_old_file_name.lower(),
                                          "File:" + self.pure_new_file_name)
                tag_str = tag_str.replace("File:".lower() + self.old_file_name.lower(),
                                          "File:" + self.pure_new_file_name)
                self.temp_text = self.temp_text.replace(str(tag.string), str(tag_str))

    def replace_image_in_custom_template(self):
        for template in self.parsed.templates:
            temp_template = copy.deepcopy(template)
            if prepare_str(temp_template.name) in self.template_list:
                for param in temp_template.arguments:
                    if prepare_str(param.value) == prepare_str(self.old_file_name):
                        param.value = self.pure_new_file_name
                        self.temp_text = self.temp_text.replace(str(template), str(temp_template))

    def get_new_text(self):
        return self.temp_text
