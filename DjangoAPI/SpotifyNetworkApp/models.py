from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Users(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserEmail = models.CharField(max_length=100)
    UserName = models.CharField(max_length=100)
    
class Artists(models.Model):
    ArtistId = models.CharField(max_length=100, primary_key=True)
    ArtistName = models.CharField(max_length=100)
    ArtistPopularity = models.IntegerField()
    ArtistGenre = models.JSONField()
    ArtistRank = models.IntegerField() # -1 if not in User's Top Artist
    ArtistImage = models.CharField(max_length=100)
    SimilarArtists = models.JSONField() # list of similar artist's unique ids
    
class ArtistAssocs(models.Model): # maybe associate this with a specific UserId
    AssocId = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=100) 
    SourceId = models.CharField(max_length=100)
    TargetId = models.CharField(max_length=100)
    Weight = models.IntegerField()
    Type = models.CharField(max_length=100)
    
