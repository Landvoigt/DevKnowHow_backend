from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Option


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated options.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated options.")

activate.short_description = "Activate selected options"
deactivate.short_description = "Deactivate selected options"

class OptionAdmin(TranslationAdmin):
    list_display = ('id', 'active', 'title', 'created_at')
    list_filter = ('id', 'active', 'title', 'created_at',)
    list_display_links = ('title',)
    search_fields = ('title',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    ordering = ('id',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('id', 'active',)
        }),
        ('Content', {
            'fields': ('title', 'description',)
        }),
        ('Creation', {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    
    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Option, OptionAdmin)