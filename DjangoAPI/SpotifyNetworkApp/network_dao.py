from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Artists

class NetworkDAO:
    def __init__(self):
        # TODO: Initialize Logger object for DAO Layer
        self.Logger = ''
    
    def artist_exists(self, artist_id):
        try:
            artist = Artists.objects.get(ArtistId=artist_id)
            if artist:
                return True
            return False
        except Artists.DoesNotExist:
            print("Does not exist")
            return False
    
    def save_artist(self, artist):
        exists = self.artist_exists(artist['ArtistId'])
        if(not exists):
            id = artist['ArtistId']
            name = artist['ArtistName']
            popularity = artist['ArtistPopularity']
            genre = artist['ArtistGenre']
            image = artist['ArtistImage']
            similar = artist['SimilarArtists']
            artist_obj = Artists(ArtistId=id, ArtistName=name, ArtistPopularity=popularity, ArtistGenre=genre, ArtistImage=image, SimilarArtists=similar)
            artist_obj.save()
            return True
        else:
            return False
    
    def get_artist(self, artist_id):
        return Artists.objects.get(ArtistId=artist_id)
          
    def save_network(self, session_id, timeframe):
        return ''
    
    def get_network(self, session_id, timeframe):
        return ''