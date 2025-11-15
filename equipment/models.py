from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class Equipment(models.Model):
    """Model for sports equipment inventory"""
    CATEGORY_CHOICES = [
        ('racquet', 'Racquet Sports'),
        ('ball', 'Balls'),
        ('protective', 'Protective Gear'),
        ('fitness', 'Fitness Equipment'),
        ('other', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    quantity_available = models.IntegerField(default=0)
    rental_price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.quantity_available} available)"


class Rental(models.Model):
    """Model for equipment rentals"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rentals')
    quantity = models.IntegerField(default=1)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rental_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.equipment.name}"
    
    @property
    def is_overdue(self):
        """Check if rental is overdue"""
        return self.status == 'active' and self.return_date < timezone.now()
