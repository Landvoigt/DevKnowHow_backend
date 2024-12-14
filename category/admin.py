from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'title', 'description', 'creation_date')

admin.site.register(Category, CategoryAdmin)