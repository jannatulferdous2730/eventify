from django.contrib import admin
from . models import *

# Register your models here.


class ClubImageInline(admin.TabularInline):
    model = ClubImage
    extra = 1  # Number of empty forms to display by default

class ClubAdmin(admin.ModelAdmin):
    inlines = [ClubImageInline]
    list_display = ('name', 'status', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

admin.site.register(Club, ClubAdmin)


admin.site.register(Category)
admin.site.register(Catering)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(BurningQuestions)

