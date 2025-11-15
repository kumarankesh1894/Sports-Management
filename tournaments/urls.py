from django.urls import path
from . import views

urlpatterns = [
    path('', views.tournament_list, name='tournaments'),
    path('<int:pk>/', views.tournament_detail, name='tournament_detail'),
]

