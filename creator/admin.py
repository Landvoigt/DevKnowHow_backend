from django.contrib import admin
from .models import Creator


class CreatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'firstName', 'lastName', 'created_at')
    list_filter = ('id', 'active', 'email', 'firstName', 'lastName', 'created_at',)
    list_display_links = ('email',)
    search_fields = ('email', 'firstName', 'lastName',)
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('id', 'active',)
        }),
        ('Content', {
            'fields': ('firstName', 'lastName', 'email',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )

admin.site.register(Creator, CreatorAdmin)