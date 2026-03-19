from tasks.infobox_football_biography.src.data_translator.classification_context import ClassificationContext
from tasks.infobox_football_biography.src.data_translator.data_classification.normal_text_classification_strategy import \
    NormalTextClassificationStrategy
from tasks.infobox_football_biography.src.data_translator.data_classification.number_classification_strategy import \
    NumberClassificationStrategy
from tasks.infobox_football_biography.src.data_translator.data_classification.wikilink_classification_strategy import \
    WikiLinkClassificationStrategy
from tasks.infobox_football_biography.src.data_translator.data_translation.number_translation_handler import \
    NumberTranslationHandler
from tasks.infobox_football_biography.src.data_translator.translation_chain import TranslationChain

classification_context = ClassificationContext()
classification_context.add_strategy(NumberClassificationStrategy())
classification_context.add_strategy(WikiLinkClassificationStrategy())
classification_context.add_strategy(NormalTextClassificationStrategy())

# Create translation chain and add translation handlers
translation_chain = TranslationChain()
translation_chain.add_handler(NumberTranslationHandler())
# Add handlers for WikiLink and NormalText as needed

# Sample data
data = [
    {"name": "param1", "value": "42"},
    {"name": "param2", "value": "[[link to article]]"},
    {"name": "param3", "value": "This is normal text."}
]

for item in data:
    value = item["value"]
    classification = classification_context.classify(value)
    translation = translation_chain.translate(value)

    print(f"Name: {item['name']}")
    print(f"Value: {value}")
    print(f"Classification: {classification}")
    print(f"Translation: {translation}")
    print("---")
