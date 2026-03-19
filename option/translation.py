from modeltranslation.translator import translator, TranslationOptions
from .models import Option


class OptionTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(Option, OptionTranslationOptions)