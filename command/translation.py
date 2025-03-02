from modeltranslation.translator import translator, TranslationOptions
from .models import Command


class CommandTranslationOptions(TranslationOptions):
    fields = ('command', 'description', 'tooltip',)


translator.register(Command, CommandTranslationOptions)