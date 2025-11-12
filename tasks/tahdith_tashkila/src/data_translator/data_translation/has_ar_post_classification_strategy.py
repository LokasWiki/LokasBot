import pywikibot

from tasks.tahdith_tashkila.src.data_translator.data_translation_handler import DataTranslationHandler
from tasks.tahdith_tashkila.src.models.player import Player


class HasArPostTranslationHandler(DataTranslationHandler):
    def translate(self, model: Player):
        if model.classification != "has_ar_post":
            return

        template_format = "{{template_name|الرقم=number|الاسم=page_title}}"
        template_format = template_format.replace("template_name", self.template_name(model))
        if model.is_manager:
            template_format = template_format.replace("|الرقم=number", "")
        else:
            template_format = template_format.replace("number", self.number(model))
        template_format = template_format.replace("page_title", self.name(model))

        # Translate the wiki link to Arabic (implement this logic)
        return template_format

    def template_name(self, model: Player):
        template = "لاعب تشكيلة فريق كرة قدم"
        if model.is_manager:
            template = "مدرب تشكيلة فريق كرة قدم"
        return template

    def number(self, model: Player):
        return str(model.number)

    def name(self, model: Player):
        en_site = pywikibot.Site("en", "wikipedia")
        en_page = pywikibot.Page(en_site, model.page_title)
        ar_title = None
        if en_page.exists():
            for item in en_page.langlinks():
                if str(item).startswith("[[ar:"):
                    ar_title = item.title
                    break

        if ar_title is None:
            return model.page_title
        else:
            return "[[" + ar_title + "]]"
