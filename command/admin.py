from django.contrib import admin

from .models import Command


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated commands.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated commands.")

activate.short_description = "Activate selected commands"
deactivate.short_description = "Deactivate selected commands"

class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'command', 'category', 'creation_date',)
    list_filter = ('id', 'active', 'command', 'category', 'creation_date',)
    list_display_links = ('command',)
    search_fields = ('command', 'category',)
    ordering = ('-creation_date',)
    readonly_fields = ('id', 'creation_date',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'command', 'category', 'sub_category', 'description',)
        }),
        ('Extra Information', {
            'fields': ('example', 'tooltip', 'param',)
        }),
        ('Creation Information', {
            'fields': ('creation_date', 'creator_name', 'creator_email', 'creator_message',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Command, CommandAdmin)