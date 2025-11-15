from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment'),
    path('<int:pk>/rent/', views.rent_equipment, name='rent_equipment'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
]

