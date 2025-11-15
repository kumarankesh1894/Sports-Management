from django.contrib import admin
from .models import Facility, FacilityAvailability

# Register your models here.

class FacilityAvailabilityInline(admin.TabularInline):
    model = FacilityAvailability
    extra = 1

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_type', 'capacity', 'hourly_rate', 'is_active', 'created_at']
    list_filter = ['facility_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    inlines = [FacilityAvailabilityInline]

@admin.register(FacilityAvailability)
class FacilityAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['facility', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['facility', 'day_of_week', 'is_available']
    search_fields = ['facility__name']
