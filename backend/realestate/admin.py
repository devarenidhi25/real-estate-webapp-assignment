from django.contrib import admin
from .models import RealEstateData, QueryLog


@admin.register(RealEstateData)
class RealEstateDataAdmin(admin.ModelAdmin):
    list_display = ('area', 'year', 'price', 'demand')
    list_filter = ('area', 'year')
    search_fields = ('area',)
    ordering = ('area', 'year')


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query_text_short', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query_text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def query_text_short(self, obj):
        return obj.query_text[:100] + '...' if len(obj.query_text) > 100 else obj.query_text
    query_text_short.short_description = 'Query'
