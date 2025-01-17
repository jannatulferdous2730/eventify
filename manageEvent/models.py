from django.db import models
from django.conf import settings
#from tinymce.models import HTMLField


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

# Catering Model
class Catering(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# Location Model
class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Club Model
class Club(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
     
     
    WIFI_STATUS = [
        ('free', 'free'),
        ('paid', 'paid'),
    ]

    CAR_PARKING_STATUS = [
        ('Available', 'Available'),
        ('unavailable', 'unavailable'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    map_url = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    type = models.CharField(max_length=100, blank=True)
    car_parking = models.CharField(
        max_length=100,
        choices=CAR_PARKING_STATUS,
        default='Available',
    )
    wifi = models.CharField(
        max_length=100,
        choices=WIFI_STATUS,
        default='free',
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    features = models.TextField()
    capacity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='venue_images/')
    price_per_day = models.IntegerField(default=0)
    old_price_per_day = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class ClubImage(models.Model):
    club = models.ForeignKey(Club, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='club_images/')

    def __str__(self):
        return f"Image for {self.club.name}"

# Booking Model
class Booking(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField()
    hours = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.club.name}"


# Review Model
class Review(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    positions = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.club.name}"


# Question Model
class BurningQuestions(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
