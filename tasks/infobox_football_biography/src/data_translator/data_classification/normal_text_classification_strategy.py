from tasks.infobox_football_biography.src.data_translator.value_classification_strategy import \
    ValueClassificationStrategy


class NormalTextClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        return "normal_text"
