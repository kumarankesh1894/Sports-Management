from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:facility_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
]

