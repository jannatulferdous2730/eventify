from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def venue_page(request):
    return render(request, 'venue_page.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')