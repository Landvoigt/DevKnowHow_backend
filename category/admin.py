from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


def activate(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated categories.")

def deactivate(modeladmin, request, queryset):
    updated_count = queryset.update(active=False)
    modeladmin.message_user(request, f"{updated_count} successfully deactivated categories.")

activate.short_description = "Activate selected categories"
deactivate.short_description = "Deactivate selected categories"

class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'active', 'title', 'description', 'type', 'creation_date',)
    list_filter = ('id', 'active', 'title', 'description', 'type', 'creation_date',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('-creation_date',)
    readonly_fields = ('id', 'creation_date',)
    fieldsets = (
        (None, {
            'fields': ('id', 'active', 'title', 'description', 'type',)
        }),
        ('Creation Information', {
            'fields': ('creation_date',)
        }),
    )
    inlines = [SubCategoryInline]
    actions = [activate, deactivate, 'delete_selected']

admin.site.register(Category, CategoryAdmin)
