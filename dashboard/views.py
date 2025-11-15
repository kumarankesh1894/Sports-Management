from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from bookings.models import Booking
from tournaments.models import Tournament
from equipment.models import Rental
from users.models import User

# Create your views here.

def is_admin(user):
    return user.is_staff or user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view"""
    # Statistics
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    total_tournaments = Tournament.objects.count()
    total_revenue = Booking.objects.filter(payment_status=True).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_tournaments': total_tournaments,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard/admin.html', context)
