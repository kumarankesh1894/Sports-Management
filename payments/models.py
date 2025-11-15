from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class Payment(models.Model):
    """Model for payment transactions"""
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='razorpay')
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    
    # Reference to related object (Booking, Rental, Subscription, etc.)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.status})"


class PaymentHistory(models.Model):
    """Model to track payment history"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50)  # 'initiated', 'completed', 'failed', 'refunded'
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional payment data
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Payment Histories'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.payment} - {self.action}"
