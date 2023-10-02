from tasks.tahdith_tashkila.src.data_translator.value_classification_strategy import ValueClassificationStrategy


class NotHasArPostClassificationStrategy(ValueClassificationStrategy):
    def classify(self, value):
        try:
            float(value)
            return "not_has_ar_post"
        except ValueError:
            return None
