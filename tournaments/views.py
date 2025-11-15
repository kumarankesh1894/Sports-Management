from django.shortcuts import render, get_object_or_404
from .models import Tournament, Team, Match

# Create your views here.

def tournament_list(request):
    """List all tournaments"""
    tournaments = Tournament.objects.all().order_by('-start_date')
    context = {
        'tournaments': tournaments,
    }
    return render(request, 'tournaments/list.html', context)

def tournament_detail(request, pk):
    """Show tournament details"""
    tournament = get_object_or_404(Tournament, pk=pk)
    teams = tournament.teams.all().order_by('-points')
    matches = tournament.matches.all().order_by('scheduled_date')
    context = {
        'tournament': tournament,
        'teams': teams,
        'matches': matches,
    }
    return render(request, 'tournaments/detail.html', context)
