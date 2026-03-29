from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Option
from category.models import Category
from command.models import Command


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated options.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated options.")

activate.short_description = "Activate selected options"
deactivate.short_description = "Deactivate selected options"


class OptionAdminForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.command:
            self.fields["category"].queryset = self.instance.command.category.all()

        elif "command" in self.data:
            try:
                command_id = int(self.data.get("command"))
                command = Command.objects.get(pk=command_id)
                self.fields["category"].queryset = command.category.all()
            except (ValueError, Command.DoesNotExist):
                self.fields["category"].queryset = Category.objects.none()
        else:
            self.fields["category"].queryset = Category.objects.none()


class OptionAdmin(TranslationAdmin):
    form = OptionAdminForm

    list_display = ('id', 'active', 'command', 'title', 'description', 'level', 'created_at')
    list_filter = ('id', 'active', 'command', 'title', 'created_at',)
    filter_horizontal = ('category',)
    list_display_links = ('title',)
    search_fields = ('command', 'title', 'description',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    ordering = ('id',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'command', 'category',)
        }),
        ('Content', {
            'fields': ('title', 'description', 'level', 'combinable', 'standalone', 'overwrite',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    
    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Option, OptionAdmin)