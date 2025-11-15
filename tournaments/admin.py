from django.contrib import admin
from .models import Tournament, Team, Match

# Register your models here.

class TeamInline(admin.TabularInline):
    model = Team
    extra = 0
    readonly_fields = ['points', 'wins', 'losses', 'draws']

class MatchInline(admin.TabularInline):
    model = Match
    extra = 0

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'tournament_type', 'sport', 'status', 'start_date', 'end_date', 'created_by']
    list_filter = ['tournament_type', 'status', 'sport', 'created_at']
    search_fields = ['name', 'description', 'sport']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TeamInline, MatchInline]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'tournament', 'captain', 'points', 'wins', 'losses', 'draws']
    list_filter = ['tournament', 'points']
    search_fields = ['name', 'captain__username']
    filter_horizontal = ['players']
    readonly_fields = ['created_at']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'team1', 'team2', 'scheduled_date', 'status', 'winner']
    list_filter = ['tournament', 'status', 'scheduled_date']
    search_fields = ['tournament__name', 'team1__name', 'team2__name']
    readonly_fields = ['created_at', 'updated_at']
