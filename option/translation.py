from modeltranslation.translator import translator, TranslationOptions
from .models import Option


class OptionTranslationOptions(TranslationOptions):
    fields = ('description', 'value',)

translator.register(Option, OptionTranslationOptions)