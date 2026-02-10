from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-page/', views.my_page_view, name='my_page'),
    path('settings/', views.settings_view, name='settings'),
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('puzzle/<int:puzzle_id>/', views.puzzle_view, name='puzzle'),
    path('dashboard/', views.home_view, name='home'),
    path('set-language/', views.set_language, name='set_language'),
]


