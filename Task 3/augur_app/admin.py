from django.contrib import admin
from .models import Distributor, Shipment, Forecast

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'location', 'active', 'created_at')
    list_filter = ('active', 'location')
    search_fields = ('name', 'code')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('distributor', 'quantity', 'shipment_date', 'created_at')
    list_filter = ('shipment_date', 'distributor')
    date_hierarchy = 'shipment_date'

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('distributor', 'forecast_month', 'forecast_year', 'quantity', 'created_at')
    list_filter = ('forecast_month', 'forecast_year', 'distributor')
