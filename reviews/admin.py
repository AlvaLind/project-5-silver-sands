from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters,
    """
    search_fields = ['wine__name']
    list_filter = ('rating', 'wine',)
    readonly_fields = ["wine", "user", "rating",]
