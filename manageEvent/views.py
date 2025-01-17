from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from . models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import random
import string

# Index Page
def index(request):
    # club = Club.objects.all()
    club = Club.objects.filter(status='approved')
    
    paginator = Paginator(club, 6)  # Show 6 clubs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    category = Category.objects.all()
    catering = Catering.objects.all()
    location = Location.objects.all()
    questions = BurningQuestions.objects.all() 

    return render(request, 'index.html', {
        'club': club,
        'category': category,
        'catering': catering,
        'location': location,
        'questions': questions,
        'page_obj': page_obj,
    })

# Search Venue
def search_venues(request):
    # Get data from the form
    categories = Category.objects.all()
    caterings = Catering.objects.all()
    locations = Location.objects.all()

    query = request.GET.get('query', '').strip()  
    category_id = request.GET.get('category', '').strip()  
    catering_id = request.GET.get('catering', '').strip() 
    location_id = request.GET.get('location', '').strip()  

    clubs = Club.objects.all()
    
    # Check if all fields are empty
    if not (query or category_id or catering_id or location_id):
        error_message = "Please fill in at least one field to search."
        return render(
            request, 
            'search.html', 
            {
                'error_message': error_message,
                'categories': categories,
                'caterings': caterings,
                'locations': locations
            }
        )

    # Filter clubs based on user input
    if query:
        clubs = clubs.filter(name__icontains=query)
    if category_id:
        clubs = clubs.filter(category_id=category_id)
    if catering_id:
        clubs = clubs.filter(catering_id=catering_id)
    if location_id:
        clubs = clubs.filter(location_id=location_id)

    # Handle case where no results match 
    if not clubs.exists():
        error_message = "No results found please try..."
        return render(
            request, 
            'search.html', 
            {
                'error_message': error_message,
                'categories': categories,
                'caterings': caterings,
                'locations': locations
            }
        )

    return render(
        request, 
        'search.html', 
        {
            'clubs': clubs,
            'categories': categories,
            'caterings': caterings,
            'locations': locations
        }
    )

   
# Venue Detail
def venue_detail(request,venue_id):
    club = get_object_or_404(Club, id=venue_id)
    reviews = club.reviews.all()  
 
     # Handle Review Submission
    if request.method == 'POST' and 'review_submit' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.club = club
            review.user = request.user
            review.save()
            return redirect('venue_detail', venue_id=club.pk)
    else:
        review_form = ReviewForm()

    # Handle Booking Submission
    if request.method == 'POST' and 'booking_submit' in request.POST:
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.club = club
            booking.user = request.user
            booking.total_price = booking.hours * club.hourly_rate  # Assuming `hourly_rate` in `Club`
            booking.save()
            return redirect('venue_detail', venue_id=club.pk)
    else:
        booking_form = BookingForm()
        
        
        context = {
        'club': club,
        'reviews': reviews,
        'review_form': review_form,
        'booking_form': booking_form,
        
        }

    return render(request, 'venue_page.html', context)


# Book
@login_required
def book(request):
    if request.method == 'POST':
        # Get data from the form
        context = {}
        
        club_id = request.POST.get('club_id')
        booking_date = request.POST.get('booking_date')
        
        user_email = request.user.email
        verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        base_url = "http://127.0.0.1:8000/"
        verification_url = f"{base_url}?code={verification_code}"

        
        subject = 'Book Payments Details - [eventify.com]'
        message = "\nWelcome, \n\nYour 30% payments completed successfully! \n\n"+verification_url+'' +" \nThank you!"+ "\n\n\n Your booked date is: "+booking_date
        
        
        if user_email and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
        
        # Validate the data
        if not club_id or not booking_date:
            return HttpResponse("Invalid data", status=400)
        
        # Fetch the Club object
        club = get_object_or_404(Club, id=club_id)
       
        # Debugging print statements
        print(f"Club: {club}, Booking Date: {booking_date}")

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            club=club,
            booking_date=booking_date,
            hours=1,  # Default value, update as needed
            total_price=100.00,  # Example price, update as needed
        )
        booking.save()

        # Redirect to a success page
        return redirect('success') 
    
    # If GET request, render form
    return HttpResponse("Invalid request method", status=405)


# Cancel Booking 
def cancel_booking(request, booking_id):
    # Get the booking object or return 404 if not found
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Delete the booking
    booking.delete()

    # Redirect to the dashboard after canceling
    return redirect('user_dashboard') 



# Success
def success(request):
    return render(request, 'success.html', {'message': 'Booking successful!'})





@user_passes_test(lambda u: u.is_staff)
def manage_clubs(request):
    clubs = Club.objects.filter(status='pending')  # Only show pending clubs
    if request.method == 'POST':
        club_id = request.POST.get('club_id')
        action = request.POST.get('action')
        try:
            club = Club.objects.get(id=club_id)
            if action == 'approve':
                club.status = 'approved'
            elif action == 'reject':
                club.status = 'rejected'
            club.save()
        except Club.DoesNotExist:
            pass
        return redirect('manage_clubs')
    
    return render(request, 'manage_clubs.html', {'clubs': clubs})

def club_list(request):
    clubs = Club.objects.filter(owner=request.user)
    return render(request, 'club_list.html', {'clubs': clubs})