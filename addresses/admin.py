from django.contrib import admin
from .models import State, City

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'pincode_prefix', 'slug')
    list_filter = ('state',)
    search_fields = ('name', 'pincode_prefix', 'state__name')
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ('state',)
    autocomplete_fields = ['state']
    
    ordering = ('name',)