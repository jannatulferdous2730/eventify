from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('venue/<int:venue_id>/', views.venue_detail, name='venue_detail'),
    # path('logout/', views.logout_view, name='logout'),
    path('search-venues', views.search_venues, name='search-venues'),
    path('book/', views.book, name='book'),
    path('clubs/', views.club_list, name='club_list'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('success/', views.success, name='success'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    
    
] 