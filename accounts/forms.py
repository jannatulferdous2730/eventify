from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from manageEvent . models import *

from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        
        
        
class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name', 'category', 'catering', 'location', 'map_url', 'description',
            'type', 'car_parking', 'wifi', 'features', 'capacity', 'image',
            'price_per_day', 'old_price_per_day',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter club name'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Select category'}),
            'catering': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Select catering option'}),
            'location': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Select location'}),
            'map_url': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter map URL'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full h-12', 'placeholder': 'Enter club description'}),
            'type': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter club type'}),
            'car_parking': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Select car parking option'}),
            'wifi': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Select Wi-Fi availability'}),
            'features': forms.Textarea(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full h-12', 'placeholder': 'Enter club features'}),
            'capacity': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter club capacity'}),
            'image': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Upload club image'}),
            'price_per_day': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter price per day'}),
            'old_price_per_day': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg p-2 w-full', 'placeholder': 'Enter old price per day'}),
        }
        
class ClubImageForm(forms.ModelForm):
    class Meta:
        model = ClubImage
        fields = ['image']