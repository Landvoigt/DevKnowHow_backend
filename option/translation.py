from modeltranslation.translator import translator, TranslationOptions
from .models import Option


class OptionTranslationOptions(TranslationOptions):
    fields = ('description',)

translator.register(Option, OptionTranslationOptions)