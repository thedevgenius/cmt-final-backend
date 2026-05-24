from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    # What columns to show in the list view
    list_display = ('name', 'owner', 'primary_category', 'city', 'is_active', 'is_verified', 'created_at')
    
    # Filters on the right sidebar
    list_filter = ('is_active', 'is_verified', 'city', 'created_at')
    
    # Search bar at the top
    search_fields = ('name', 'email', 'phone', 'slug', 'handle')
    
    # Makes the ManyToMany categories selection a nice dual-list widget
    filter_horizontal = ('categories',)
    
    # These fields are auto-managed, so they must be read-only if we display them
    readonly_fields = ('created_at', 'updated_at')

    # Automatically populate the slug based on the name while typing in the admin
    prepopulated_fields = {'slug': ('name',)}

    # ==========================================
    # GROUPING FIELDS INTO SEPARATE SECTIONS
    # ==========================================
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'owner', 
                'name', 
                'slug', 
                'handle', 
                'description'
            )
        }),
        ('Categorization', {
            'fields': (
                'primary_category', 
                'categories'
            ),
            'description': 'Select the primary category and any other applicable categories.'
        }),
        ('Contact Information', {
            'fields': (
                'phone', 
                'phone_alt', 
                'whatsapp', 
                'email', 
                'website'
            )
        }),
        ('Location & Spatial Data', {
            'fields': (
                'address', 
                'landmark', 
                'locality', 
                'pincode', 
                'city', 
                ('latitude', 'longitude'), # Grouped on the same row
                'geohash'
            )
        }),
        ('SEO & Metadata', {
            'classes': ('collapse',), # This makes the section collapsible to save space
            'fields': (
                'meta_title', 
                'meta_description', 
                'meta_keywords'
            )
        }),
        ('Status & Tracking', {
            'fields': (
                'is_active', 
                'is_verified', 
                'created_at', 
                'updated_at'
            )
        }),
    )