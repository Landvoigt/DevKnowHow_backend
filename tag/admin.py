from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_filter = ('id', 'active', 'created_at',)
    list_display_links = ('id',)
    search_fields = ('title',)
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('id', 'active',)
        }),
        ('Content', {
            'fields': ('title',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

admin.site.register(Tag, TagAdmin)