from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
