from django.contrib import admin

from .models import Command


def mark_active(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated commands.")

mark_active.short_description = "Activate selected commands"

class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'command', 'category', 'example', 'creation_date')
    actions = [mark_active]

admin.site.register(Command, CommandAdmin)