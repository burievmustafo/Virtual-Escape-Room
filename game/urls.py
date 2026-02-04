from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('puzzle/<int:puzzle_id>/', views.puzzle_view, name='puzzle'),
    path('statistics/', views.statistics_view, name='statistics'),
]


