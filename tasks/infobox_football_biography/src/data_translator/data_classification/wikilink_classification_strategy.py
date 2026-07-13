from tasks.infobox_football_biography.src.data_translator.value_classification_strategy import \
    ValueClassificationStrategy


class WikiLinkClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        # todo: use wpikitextparser
        if value.startswith("[[") and value.endswith("]]"):
            return "wiki_link"
        return None
