from rest_framework import serializers
from SpotifyNetworkApp.models import Users, Artists, ArtistAssocs

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('UserId',
                  'UserEmail',
                  'UserName')
        
class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists 
        fields = ('ArtistId',
                  'ArtistName',
                  'ArtistFollowers',
                  'ArtistGenre',
                  'ArtistRank',
                  'SimilarArtists')
        
class ArtistAssocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistAssocs
        fields = ('AssocId',
                  'UserId',
                  'SourceId',
                  'TargetId',
                  'Weight',
                  'Type')