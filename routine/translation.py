from modeltranslation.translator import translator, TranslationOptions
from .models import Routine


class RoutineTranslationOptions(TranslationOptions):
    fields = ('title', 'routine', 'tooltip')


translator.register(Routine, RoutineTranslationOptions)