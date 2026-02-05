from django.urls import path
from . import views

urlpatterns = [
    path('submit-answer/<int:puzzle_id>/', views.submit_answer, name='submit_answer'),
    path('use-hint/<int:puzzle_id>/', views.use_hint, name='use_hint'),
]


