from django.shortcuts import render, get_object_or_404
from .models import Facility, FacilityAvailability

# Create your views here.

def facility_list(request):
    """List all facilities"""
    facilities = Facility.objects.filter(is_active=True)
    context = {
        'facilities': facilities,
    }
    return render(request, 'facilities/list.html', context)

def facility_detail(request, pk):
    """Show facility details"""
    facility = get_object_or_404(Facility, pk=pk)
    availabilities = facility.availabilities.filter(is_available=True)
    context = {
        'facility': facility,
        'availabilities': availabilities,
    }
    return render(request, 'facilities/detail.html', context)
