from django.contrib import admin
from .models import Payment, PaymentHistory

# Register your models here.

class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    readonly_fields = ['action', 'notes', 'metadata', 'timestamp']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'transaction_id', 'payment_date', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['user__username', 'transaction_id', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['payment', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['payment__transaction_id']
    readonly_fields = ['timestamp']
