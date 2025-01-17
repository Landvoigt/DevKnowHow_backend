from django.contrib import admin
from .models import Routine


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated routines.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated routines.")

activate.short_description = "Activate selected routines"
deactivate.short_description = "Deactivate selected routines"

class RoutineAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'routine', 'category', 'sub_category', 'copy_count', 'creation_date',)
    list_filter = ('id', 'active', 'routine', 'category', 'sub_category', 'copy_count', 'creation_date',)
    list_display_links = ('routine',)
    search_fields = ('routine', 'category','sub_category',)
    ordering = ('-creation_date',)
    readonly_fields = ('id', 'creation_date', 'copy_count',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'routine', 'category', 'sub_category',)
        }),
        ('Extra Information', {
            'fields': ('example', 'tooltip', 'copy_count',)
        }),
        ('Creation Information', {
            'fields': ('creation_date', 'creator_name', 'creator_email', 'creator_message',)
        }),
    )

    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Routine, RoutineAdmin)