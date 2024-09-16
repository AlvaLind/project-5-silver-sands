from django.contrib import admin
from .models import Category, Wine
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):
    """
    Lists fields for display, Allow searching by name & description.
    Allow text input through summernote. 
    """
    list_display = ('name',)
    search_fields = ['name', 'description']
    summernote_fields = ('description',)


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    """
    List fields for display. Allow searching by name, category & vintage.
    Provide filtering by category & availability.
    Support ordering by price, vintage, rating & stock.
    """
    list_display = ('name', 'category', 'price', 'vintage', 'rating', 'stock', 'available')
    search_fields = ('name', 'category', 'vintage')
    list_filter = ('category', 'available')
    ordering = ('category',)
    ordering_fields = ('price', 'vintage', 'rating', 'stock')
    