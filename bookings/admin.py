from django.contrib import admin
from .models import Booking, BookingHistory

# Register your models here.

class BookingHistoryInline(admin.TabularInline):
    model = BookingHistory
    extra = 0
    readonly_fields = ['action', 'action_by', 'notes', 'timestamp']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'facility', 'booking_date', 'start_time', 'end_time', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'booking_date', 'created_at']
    search_fields = ['user__username', 'facility__name']
    date_hierarchy = 'booking_date'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BookingHistoryInline]

@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ['booking', 'action', 'action_by', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['booking__user__username', 'action']
    readonly_fields = ['timestamp']
