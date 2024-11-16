from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('venue_page/', views.venue_page),
] 