from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Artists, ArtistAssocs

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
            return False
    
    def get_artist(self, artist_id):
        return Artists.objects.get(ArtistId=artist_id)
    
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
    
    def assoc_exists(self, source, target):
        try:
            assoc = ArtistAssocs.objects.get(SourceId=source, TargetId=target)
            if assoc:
                return True
            return False
        except ArtistAssocs.DoesNotExist:
            return False
    
    def get_assoc(self, source, target):
        try:
            return ArtistAssocs.objects.get(SourceId=source, TargetId=target)
        except ArtistAssocs.DoesNotExist:
            return None
        
    def save_assoc(self, assoc):
        exists = self.assoc_exists(assoc['SourceId'], assoc['TargetId'])
        if(not exists):
            source = assoc['SourceId']
            target = assoc['TargetId']
            weight = assoc['Weight']
            assoc_obj = ArtistAssocs(SourceId=source,TargetId=target,Weight=weight)
            assoc_obj.save()
            return True
        else:
            return False
        
    def save_network(self, session_id, timeframe):
        return ''
    
    def get_network(self, session_id, timeframe):
        return ''