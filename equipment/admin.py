from django.contrib import admin
from .models import Equipment, Rental

# Register your models here.

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity_available', 'rental_price_per_hour', 'condition', 'is_active']
    list_filter = ['category', 'condition', 'is_active']
    search_fields = ['name', 'description']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['user', 'equipment', 'quantity', 'rental_date', 'return_date', 'status', 'payment_status']
    list_filter = ['status', 'payment_status', 'rental_date']
    search_fields = ['user__username', 'equipment__name']
    date_hierarchy = 'rental_date'
    readonly_fields = ['created_at', 'updated_at']
