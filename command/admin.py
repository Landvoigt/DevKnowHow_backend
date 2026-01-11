from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.contrib.postgres.aggregates import StringAgg

from category.models import Category
from .models import Command


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated commands.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated commands.")

activate.short_description = "Activate selected commands"
deactivate.short_description = "Deactivate selected commands"

def make_add_to_category_action(category):
    def action(modeladmin, request, queryset):
        for command in queryset:
            command.category.add(category)
        modeladmin.message_user(
            request,
            f"{queryset.count()} commands added to category '{category.title}'."
        )
    action.short_description = f"Add commands to category '{category.title}'"
    action.__name__ = f"add_to_category_{category.id}"
    return action

def make_remove_from_category_action(category):
    def action(modeladmin, request, queryset):
        for command in queryset:
            command.category.remove(category)
        modeladmin.message_user(
            request,
            f"{queryset.count()} commands removed from category '{category.title}'."
        )
    action.short_description = f"Remove commands from category '{category.title}'"
    action.__name__ = f"remove_from_category_{category.id}"
    return action

class CommandAdmin(TranslationAdmin):
    list_display = ('id', 'active', 'title', 'category_list', 'copy_count', 'created_at',)
    list_filter = ('id', 'active', 'title', 'copy_count', 'created_at',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'copy_count',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('category', 'option', 'alternative',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'category',)
        }),
        ('Content', {
            'fields': ('title', 'description', 'tooltip', 'example',)
        }),
        ('Extra', {
            'fields': ('option', 'alternative',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            category_titles=StringAgg(
                'category__title',
                delimiter=', ',
                ordering='category__title'
            )
        )

    def category_list(self, obj):
        return obj.category_titles
    category_list.short_description = 'Category'
    category_list.admin_order_field = 'category_titles'

    def category_field(self, db_field, request, **kwargs):
        if db_field.name == "category":
            from category.models import Category
            categories = Category.objects.all()
            if categories.count() == 1:
                kwargs["initial"] = categories
        return super().category_field(db_field, request, **kwargs)
    
    def option_field(self, db_field, request, **kwargs):
        if db_field.name == "option":
            from option.models import Option
            options = Option.objects.all()
            if options.count() == 1:
                kwargs["initial"] = options
        return super().option_field(db_field, request, **kwargs)
    
    def alternative_field(self, db_field, request, **kwargs):
        if db_field.name == "alternative":
            from .models import Command
            alternatives = Command.objects.all()
            if alternatives.count() == 1:
                kwargs["initial"] = alternatives
        return super().alternative_field(db_field, request, **kwargs)

for cat in Category.objects.all():
    CommandAdmin.actions.append(make_add_to_category_action(cat))
    CommandAdmin.actions.append(make_remove_from_category_action(cat))

admin.site.register(Command, CommandAdmin)