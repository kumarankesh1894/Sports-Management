from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class Facility(models.Model):
    """Model for sports facilities/courts"""
    FACILITY_TYPE_CHOICES = [
        ('badminton', 'Badminton Court'),
        ('tennis', 'Tennis Court'),
        ('football', 'Football Field'),
        ('basketball', 'Basketball Court'),
        ('gym', 'Gym'),
        ('swimming', 'Swimming Pool'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    capacity = models.IntegerField(default=1, help_text="Number of players/capacity")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Facilities'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()})"


class FacilityAvailability(models.Model):
    """Model for managing facility availability schedule"""
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Facility Availabilities'
        unique_together = ['facility', 'day_of_week', 'start_time', 'end_time']
        ordering = ['facility', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.facility.name} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"
