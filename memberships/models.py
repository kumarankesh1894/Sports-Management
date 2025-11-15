from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class MembershipPlan(models.Model):
    """Model for membership plan details"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField(help_text="Duration in months")
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text="Discount percentage on bookings"
    )
    priority_booking = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ${self.price} ({self.duration_months} months)"


class MembershipSubscription(models.Model):
    """Model for user membership subscriptions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    auto_renew = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date
    
    def save(self, *args, **kwargs):
        """Auto-calculate end date if not provided"""
        if not self.pk and self.plan:  # Only on creation
            from dateutil.relativedelta import relativedelta
            self.end_date = self.start_date + relativedelta(months=self.plan.duration_months)
        super().save(*args, **kwargs)
