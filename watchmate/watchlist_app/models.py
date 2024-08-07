from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatForm(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(max_length=200)
    about = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class WatchList(models.Model):  
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    platForm = models.ForeignKey(StreamPlatForm, related_name= 'watchlist', on_delete= models.CASCADE)
    avg_rating = models.FloatField(default=0)
    num_ratings = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    

class Reviews(models.Model):
    review_user = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        return self.title + " - " + str(self.rating)
    