from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'category_type', 'order', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'category_type')
    search_fields = ('name', 'slug', 'meta_title')
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}

    # Organizing the detail view into clean, separated sections
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'parent', 'category_type'),
            'description': 'Basic details and hierarchy of the category.'
        }),
        ('Display & Styling', {
            'fields': ('icon_class', 'color', 'order'),
            'classes': ('collapse',),  # Hides this section by default with a "Show" button
            'description': 'Control how this category appears on the frontend.'
        }),
        ('Status & Visibility', {
            'fields': ('is_active', 'is_featured')
        }),
        ('SEO Configuration', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),  # Keeps the admin clean by collapsing SEO fields
            'description': 'Search Engine Optimization tags for this specific category.'
        }),
    )