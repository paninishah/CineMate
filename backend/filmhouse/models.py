from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_phone = models.CharField(max_length=15)   
    user_gender = models.CharField(max_length=10, 
    choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    user_dob = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | {self.user_gender} | Phone: {self.user_phone}"


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    genres = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()
    synopsis = models.TextField(max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")

    def __str__(self):
        return f"{self.title} ({self.year}) | Added by: {self.user.username}"


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)

    rating_value = models.PositiveIntegerField()   
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return (
            f"Rating {self.rating_id} | Movie: {self.movie.title} | "
            f"User: {self.user.username} | Rating: {self.rating_value}"
        )
