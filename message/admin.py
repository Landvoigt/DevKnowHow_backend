from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    list_filter = ('id', 'active', 'created_at',)
    list_display_links = ('id',)
    search_fields = ('text',)
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('id', 'active',)
        }),
        ('Content', {
            'fields': ('text',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

admin.site.register(Message, MessageAdmin)