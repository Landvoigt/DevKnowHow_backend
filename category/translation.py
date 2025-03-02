from modeltranslation.translator import translator, TranslationOptions
from .models import Category, SubCategory


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


translator.register(Category, CategoryTranslationOptions)
translator.register(SubCategory, SubCategoryTranslationOptions)