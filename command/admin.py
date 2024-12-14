from django.contrib import admin

from .models import Command


class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'command', 'category', 'example', 'creation_date')

admin.site.register(Command, CommandAdmin)