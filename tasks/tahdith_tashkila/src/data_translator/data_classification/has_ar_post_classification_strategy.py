from tasks.tahdith_tashkila.src.data_translator.value_classification_strategy import ValueClassificationStrategy


class HasArPostClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        try:
            float(value)
            return "has_ar_post"
        except ValueError:
            return None
