from django.contrib.auth import login as auth_login, authenticate
from .decorators import role_required
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import CustomLoginForm, ClubForm
from django.contrib.auth.forms import PasswordChangeForm
from manageEvent . models import *
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ClubForm, ClubImageForm,ClubImage


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please fill up properly...')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect based on role
                if hasattr(user, 'role') and user.role == 'owner':
                    return redirect('owner_dashboard')  # Redirect to owner's dashboard
                else:
                    return redirect('user_dashboard')  # Redirect to user's dashboard
            
                
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})



@login_required
def create_club(request):
    # Restrict access: only superuser or users with the 'owner' role can create a club
    if not request.user.is_superuser and request.user.role != 'owner':
        return redirect('/')  # Or redirect to a "permission denied" page
    
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # Retrieve multiple images from the form
        
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user  # Set the logged-in user as the owner
            club.status = 'pending'  # Default status is pending
            club.save()
            
            # Save the uploaded images
            for image in images:
                ClubImage.objects.create(club=club, image=image)
            messages.success(request, "Club created successfully!") 
            return redirect('owner_dashboard')  # Redirect to the owner's dashboard
    else:
        form = ClubForm()
    
    return render(request, 'create_club.html', {'form': form})



@login_required
def edit_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    if not request.user.is_superuser and request.user != club.owner:
        return redirect('/')  # Or a "permission denied" page
    
    if request.method == 'POST':
        club_form = ClubForm(request.POST, instance=club)
        image_forms = [ClubImageForm(request.POST, request.FILES, instance=image) for image in club.images.all()]
        
        if club_form.is_valid():
            club = club_form.save()  # Save the club first

            # Save or update images
            for form in image_forms:
                if form.is_valid():
                    form.save()
            
            # Handle new images if uploaded
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    ClubImage.objects.create(club=club, image=image)
            messages.success(request, "Club updated successfully!")        
            return redirect('owner_dashboard')  # Redirect to the owner dashboard
    
    else:
        club_form = ClubForm(instance=club)
        image_forms = [ClubImageForm(instance=image) for image in club.images.all()]
    
    return render(request, 'edit_club.html', {'club_form': club_form, 'image_forms': image_forms, 'club': club})



@login_required
def delete_club(request, club_id):
    club = get_object_or_404(Club, id=club_id, owner=request.user)
    if request.method == 'POST':
        club.delete()
        messages.error(request, "Club deleted successfully!") 
        return redirect('owner_dashboard')  # Redirect after deletion
    return render(request, 'delete_club.html', {'club': club})





@login_required
def owner_dashboard(request):
     # Get the clubs owned by the logged-in user
    clubs = Club.objects.filter(owner=request.user)
    
    # Get the bookings for the clubs owned by the logged-in user
    bookings = Booking.objects.filter(club__owner=request.user)
    
    return render(request, 'accounts/owner_dashboard.html', {
        'clubs': clubs,
        'bookings': bookings,
    })
    
@login_required
def user_dashboard(request):

    # Retrieve all bookings for the current user
    bookings = Booking.objects.filter(user=request.user)
    booked_count = bookings.count()  
    
    paginator = Paginator(bookings, 6)  # Show 6 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass bookings and booked_count to the template
    return render(request, 'accounts/user_dashboard.html', {
        'bookings': bookings,
        'booked_count': booked_count,
        'page_obj': page_obj,
    })




@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, club__owner=request.user)
    booking.status = 'approved'
    booking.save()
    messages.success(request, f'Booking for {booking.club.name} on {booking.booking_date} approved.')
    return redirect('owner_dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, club__owner=request.user)
    booking.status = 'rejected'
    booking.save()
    messages.warning(request, f'Booking for {booking.club.name} on {booking.booking_date} rejected.')
    return redirect('owner_dashboard')


# Logout 
def logout_view(request):
    logout(request)
    return redirect('/')


# Update Password 
@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Save the new password
            form.save()
            # Update the session to prevent logout
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been updated successfully!")

            # Redirect based on user role
            if request.user.role == 'owner':  # Check if the user is an owner
                return redirect('owner_dashboard')  # Redirect owner to their dashboard
            elif request.user.role == 'user':  # Check if the user is a regular user
                return redirect('user_dashboard')  # Redirect user to their dashboard
            else:
                return redirect('/')  # Fallback redirect if roles are not clearly defined
        else:
            messages.error(request, "Please fill up properly...")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'update_password.html', {'form': form})