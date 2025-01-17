from django import forms
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Review Form
class ReviewForm(forms.ModelForm):
      class Meta:
        model = Review
        fields = ['content', 'positions', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none',
                'placeholder': 'Write your review...',
                'rows': 4,
            }),
            'positions': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none',
                'placeholder': 'Enter your position (e.g., Developer, Manager)',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none',
                'min': 1,
                'max': 5,
                'placeholder': 'Rate (1-5)',
            }),
        }


# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'hours'] 

