from tasks.infobox_football_biography.src.data_translator.value_classification_strategy import \
    ValueClassificationStrategy


class NumberClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        try:
            float(value)
            return "number"
        except ValueError:
            return None
