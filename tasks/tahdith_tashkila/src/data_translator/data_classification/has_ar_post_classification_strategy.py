from pywikibot.scripts.generate_user_files import pywikibot

from tasks.tahdith_tashkila.src.data_translator.value_classification_strategy import ValueClassificationStrategy
from tasks.tahdith_tashkila.src.models.player import Player


class HasArPostClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        try:
            self.check_if_has(value)
            return "has_ar_post"
        except ValueError:
            return None

    def check_if_has(self, model: Player):
        en_site = pywikibot.Site("en", "wikipedia")
        en_page = pywikibot.Page(en_site, model.page_title)
        ar_title = None
        if en_page.exists():
            for item in en_page.langlinks():
                if str(item).startswith("[[ar:"):
                    ar_title = item.title
                    break

        if ar_title is None:
            raise ValueError("ar page not found")
