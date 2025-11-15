from django.urls import path
from . import views

urlpatterns = [
    path('', views.facility_list, name='facilities'),
    path('<int:pk>/', views.facility_detail, name='facility_detail'),
]

