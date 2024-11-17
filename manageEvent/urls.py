from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('venue_page/', views.venue_page, name='venue_page'),
] 