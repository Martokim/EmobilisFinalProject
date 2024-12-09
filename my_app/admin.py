from django.contrib import admin
from .models import Plant, Service, QuoteRequest, PlantRequest


# Register your models here.

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'price', 'stock')
    search_fields = ('name', 'scientific_name')
    list_filter = ('stock',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_in_months', 'location', 'created_at', 'updated_at')
    list_filter = ('category', 'location')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'created_at', 'status')
    list_filter = ('status', 'service')
    search_fields = ('user__username', 'service__name')

@admin.register(PlantRequest)
class PlantRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'quantity', 'request_date', 'status')
    list_filter = ('status', 'plant')
    search_fields = ('user__username', 'plant__name')
