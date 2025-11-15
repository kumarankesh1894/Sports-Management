from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class Tournament(models.Model):
    """Model for tournaments and leagues"""
    TOURNAMENT_TYPE_CHOICES = [
        ('league', 'League'),
        ('knockout', 'Knockout'),
        ('round_robin', 'Round Robin'),
        ('mixed', 'Mixed Format'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tournament_type = models.CharField(max_length=20, choices=TOURNAMENT_TYPE_CHOICES)
    sport = models.CharField(max_length=100)
    max_teams = models.IntegerField(default=8)
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tournaments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.get_tournament_type_display()})"


class Team(models.Model):
    """Model for tournament teams"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=200)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
    players = models.ManyToManyField(User, related_name='teams', blank=True)
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-points', '-wins']
    
    def __str__(self):
        return f"{self.name} - {self.tournament.name}"


class Match(models.Model):
    """Model for tournament matches"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    scheduled_date = models.DateTimeField()
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.tournament.name}"
