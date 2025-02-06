from modeltranslation.translator import translator, TranslationOptions
from .models import Command


class CommandTranslationOptions(TranslationOptions):
    fields = ('description', 'tooltip')

class RoutineTranslationOptions(TranslationOptions):
    fields = ('title', 'routine', 'tooltip')


translator.register(Command, CommandTranslationOptions)