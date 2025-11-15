from django.contrib import admin
from .models import MembershipPlan, MembershipSubscription

# Register your models here.

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_months', 'discount_percentage', 'priority_booking', 'is_active']
    list_filter = ['is_active', 'duration_months']
    search_fields = ['name', 'description']

@admin.register(MembershipSubscription)
class MembershipSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'status', 'auto_renew', 'created_at']
    list_filter = ['status', 'auto_renew', 'plan', 'created_at']
    search_fields = ['user__username', 'plan__name']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
