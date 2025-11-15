from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from datetime import datetime, timedelta
from .models import Equipment, Rental

# Create your views here.

def equipment_list(request):
    """List all equipment"""
    equipment = Equipment.objects.filter(is_active=True)
    context = {
        'equipment': equipment,
    }
    return render(request, 'equipment/list.html', context)

@login_required
def rent_equipment(request, pk):
    """Rent equipment"""
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        rental_start = request.POST.get('rental_start')
        rental_end = request.POST.get('rental_end')
        
        # Validate quantity availability
        if quantity > equipment.quantity_available:
            messages.error(request, f'Only {equipment.quantity_available} {equipment.name}(s) available.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        # Parse dates
        try:
            start_date = datetime.strptime(rental_start, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(rental_end, '%Y-%m-%dT%H:%M')
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        # Validate dates
        if start_date >= end_date:
            messages.error(request, 'Return date must be after rental start date.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        if start_date < datetime.now():
            messages.error(request, 'Rental start date cannot be in the past.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        # Calculate hours and cost
        duration = (end_date - start_date).total_seconds() / 3600
        total_cost = float(equipment.rental_price_per_hour) * duration * quantity
        
        # Check for conflicts (equipment already rented in this time)
        conflicts = Rental.objects.filter(
            equipment=equipment,
            status__in=['pending', 'active']
        ).filter(
            Q(rental_date__lt=end_date) & Q(return_date__gt=start_date)
        ).aggregate(rented_qty=Sum('quantity'))
        
        rented_quantity = conflicts.get('rented_qty') or 0
        if rented_quantity + quantity > equipment.quantity_available:
            messages.error(request, f'Not enough equipment available for this time period.')
            return render(request, 'equipment/rent.html', {'equipment': equipment})
        
        # Create rental
        rental = Rental.objects.create(
            user=request.user,
            equipment=equipment,
            quantity=quantity,
            rental_date=start_date,
            return_date=end_date,
            total_cost=total_cost,
            status='pending'
        )
        
        messages.success(request, f'Rental request created successfully! Total cost: ${total_cost:.2f}')
        return redirect('my_rentals')
    
    return render(request, 'equipment/rent.html', {'equipment': equipment})

@login_required
def my_rentals(request):
    """List user's equipment rentals"""
    rentals = Rental.objects.filter(user=request.user).order_by('-rental_date')
    context = {
        'rentals': rentals,
    }
    return render(request, 'equipment/my_rentals.html', context)
