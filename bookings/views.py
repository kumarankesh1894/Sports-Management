from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Booking
from facilities.models import Facility

# Create your views here.

@login_required
def create_booking(request, facility_id):
    """Create a new booking"""
    facility = get_object_or_404(Facility, id=facility_id)
    
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        # Check for conflicts
        conflicts = Booking.objects.filter(
            facility=facility,
            booking_date=booking_date,
            status__in=['confirmed', 'pending']
        ).filter(
            Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
        )
        
        if conflicts.exists():
            messages.error(request, 'This time slot is already booked. Please choose another time.')
            return render(request, 'bookings/create.html', {'facility': facility})
        
        # Calculate cost
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        hours = (end - start).total_seconds() / 3600
        total_cost = float(facility.hourly_rate) * hours
        
        booking = Booking.objects.create(
            user=request.user,
            facility=facility,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            total_cost=total_cost,
            status='pending'
        )
        
        messages.success(request, f'Booking created successfully! Total cost: ${total_cost:.2f}')
        return redirect('my_bookings')
    
    return render(request, 'bookings/create.html', {'facility': facility})

@login_required
def my_bookings(request):
    """List user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date', '-start_time')
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/list.html', context)

@login_required
def cancel_booking(request, pk):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')
    
    return render(request, 'bookings/cancel.html', {'booking': booking})
