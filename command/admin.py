from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Command


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated commands.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated commands.")

activate.short_description = "Activate selected commands"
deactivate.short_description = "Deactivate selected commands"

class CommandAdmin(TranslationAdmin):
    list_display = ('id', 'active', 'command', 'category', 'sub_category', 'copy_count', 'creation_date',)
    list_filter = ('id', 'active', 'command', 'category', 'sub_category', 'copy_count', 'creation_date',)
    list_display_links = ('command',)
    search_fields = ('command', 'category','sub_category',)
    ordering = ('-creation_date',)
    readonly_fields = ('id', 'creation_date', 'copy_count',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'command', 'category', 'sub_category', 'description',)
        }),
        ('Extra Information', {
            'fields': ('example', 'tooltip', 'copy_count',)
        }),
        ('Creation Information', {
            'fields': ('creation_date', 'creator_name', 'creator_email', 'creator_message',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Command, CommandAdmin)