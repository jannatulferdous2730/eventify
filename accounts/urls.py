from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login',views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-password/', views.update_password, name='update_password'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('accounts/owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('accounts/owner/club/create/', views.create_club, name='create_club'),
    path('accounts/owner/club/edit/<int:club_id>/', views.edit_club, name='edit_club'),
    path('accounts/owner/club/delete/<int:club_id>/', views.delete_club, name='delete_club'),
    path('accounts/owner/approve_booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('accounts/owner/reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
   
]
