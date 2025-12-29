from modeltranslation.translator import translator, TranslationOptions
from .models import Command


class CommandTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'tooltip',)


translator.register(Command, CommandTranslationOptions)