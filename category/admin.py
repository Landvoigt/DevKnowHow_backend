from django.contrib import admin

from .models import Category


def mark_active(modeladmin, request, queryset):
    updated_count = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated_count} successfully activated categories.")

mark_active.short_description = "Activate selected categories"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'title', 'description', 'creation_date')
    actions = [mark_active]

admin.site.register(Category, CategoryAdmin)