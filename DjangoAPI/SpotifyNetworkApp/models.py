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
    ArtistImage = models.CharField(max_length=100)
    SimilarArtists = models.JSONField() # list of similar artist's unique ids
    
class ArtistAssocs(models.Model): 
    AssocId = models.AutoField(primary_key=True)
    SourceId = models.CharField(max_length=100)
    TargetId = models.CharField(max_length=100)
    SourceName = models.CharField(max_length=100)
    TargetName = models.CharField(max_length=100)
    Weight = models.IntegerField()
    SharedGenres = models.JSONField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['SourceId', 'TargetId'], name='composite_primary_key'),
        ]
        
    def convert_api(self):
        assoc_api = {
            'source': self.SourceId,
            'target': self.TargetId,
            'source_name': self.SourceName,
            'target_name': self.TargetName,
            'weight': self.Weight,
            'genres': self.SharedGenres
        }
        return assoc_api
    
class ArtistNetworks(models.Model):
    NetworkId = models.AutoField(primary_key=True)
    SessionId = models.CharField(max_length=50)
    Timeframe = models.CharField(max_length=50)
    Nodes = models.JSONField()
    Links = models.JSONField()