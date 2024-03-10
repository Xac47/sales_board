from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from .models import Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'name', 'slug')
    list_display_links = ('name', 'slug')

    fieldsets = (
        ('Основная информация', {'fields': ('name', 'slug', 'parent')}),
    )
