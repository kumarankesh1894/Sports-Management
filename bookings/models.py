from django.db import models
from django.utils import timezone
from users.models import User
from facilities.models import Facility

# Create your models here.

class Booking(models.Model):
    """Model for facility bookings/reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booking_date', '-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.facility.name} on {self.booking_date}"
    
    @property
    def duration_hours(self):
        """Calculate duration in hours"""
        from datetime import datetime
        start = datetime.combine(self.booking_date, self.start_time)
        end = datetime.combine(self.booking_date, self.end_time)
        return (end - start).total_seconds() / 3600


class BookingHistory(models.Model):
    """Model to track booking history and cancellations"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50)  # 'created', 'confirmed', 'cancelled', etc.
    action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Booking Histories'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.booking} - {self.action}"
