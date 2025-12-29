from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Routine


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated routines.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated routines.")

activate.short_description = "Activate selected routines"
deactivate.short_description = "Deactivate selected routines"

class RoutineAdmin(TranslationAdmin):
    list_display = ('id', 'active', 'title', 'category_list', 'copy_count', 'created_at',)
    list_filter = ('id', 'active', 'title', 'copy_count', 'created_at',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'copy_count',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('category', 'alternative',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'category',)
        }),
        ('Content', {
            'fields': ('title', 'routine', 'tooltip', 'example',)
        }),
        ('Extra', {
            'fields': ('alternative',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

    def category_list(self, obj):
        return ", ".join([c.title for c in obj.category.all()])
    category_list.short_description = 'Category'

    def category_field(self, db_field, request, **kwargs):
        if db_field.name == "category":
            from category.models import Category
            categories = Category.objects.all()
            if categories.count() == 1:
                kwargs["initial"] = categories
        return super().category_field(db_field, request, **kwargs)

    def alternative_field(self, db_field, request, **kwargs):
        if db_field.name == "alternative":
            from .models import Command
            alternatives = Command.objects.all()
            if alternatives.count() == 1:
                kwargs["initial"] = alternatives
        return super().alternative_field(db_field, request, **kwargs)

admin.site.register(Routine, RoutineAdmin)