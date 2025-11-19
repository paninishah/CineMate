from django.contrib import admin
from .models import UserProfile, Movie, Rating

# Register your models here
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Rating)
