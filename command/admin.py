from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.contrib.postgres.aggregates import StringAgg

from category.models import Category
from option.models import Option
from .models import Command

from django import forms
from django.contrib.postgres.forms import SplitArrayField
from django.contrib.admin.widgets import FilteredSelectMultiple


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

class OptionInlineForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget = FilteredSelectMultiple(
            verbose_name='Categories',
            is_stacked=False
        )
        if self.instance and self.instance.pk:
            if self.instance.command_id:
                self.fields['category'].queryset = self.instance.command.category.all()
        elif 'command' in self.initial:
            self.fields['category'].queryset = self.initial['command'].category.all()
        else:
            self.fields['category'].queryset = Category.objects.all()

class OptionInline(TranslationTabularInline):
    model = Option
    extra = 1
    show_change_link = True
    form = OptionInlineForm

class CommandAdminForm(forms.ModelForm):
    example = SplitArrayField(
        base_field=forms.CharField(max_length=2000),
        size=3,
        remove_trailing_nulls=True,
        required=False,
    )

    class Meta:
        model = Command
        fields = "__all__"


class CommandAdmin(TranslationAdmin):
    form = CommandAdminForm
    inlines = [OptionInline]

    list_display = ('id', 'active', 'title', 'category_list', 'copy_count', 'created_at',)
    list_filter = ('id', 'active', 'title', 'copy_count', 'created_at',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'copy_count',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('category', 'alternative', 'equivalent', 'tag',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'category',)
        }),
        ('Content', {
            'fields': ('title', 'description', 'context', 'context_description', 'tooltip', 'example',)
        }),
        ('Extra', {
            'fields': ('alternative', 'equivalent', 'tag',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

    def get_actions(self, request):
        actions = super().get_actions(request)

        for category in Category.objects.all():
            add_action = make_add_to_category_action(category)
            remove_action = make_remove_from_category_action(category)

            actions[add_action.__name__] = (
                add_action,
                add_action.__name__,
                add_action.short_description,
            )
            actions[remove_action.__name__] = (
                remove_action,
                remove_action.__name__,
                remove_action.short_description,
            )

        return actions

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
    
    def alternative_field(self, db_field, request, **kwargs):
        if db_field.name == "alternative":
            from .models import Command
            alternatives = Command.objects.all()
            if alternatives.count() == 1:
                kwargs["initial"] = alternatives
        return super().alternative_field(db_field, request, **kwargs)
    
    def equivalent_field(self, db_field, request, **kwargs):
        if db_field.name == "equivalent":
            from .models import Command
            equivalents = Command.objects.all()
            if equivalents.count() == 1:
                kwargs["initial"] = equivalents
        return super().equivalent_field(db_field, request, **kwargs)    

admin.site.register(Command, CommandAdmin)