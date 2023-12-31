from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Artists, ArtistAssocs, ArtistNetworks

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
        exists = self.assoc_exists(assoc['source'], assoc['target'])
        if(not exists):
            source = assoc['source']
            target = assoc['target']
            source_name = assoc['source_name']
            target_name = assoc['target_name']
            weight = assoc['weight']
            genres = assoc['genres']
            assoc_obj = ArtistAssocs(SourceId=source,TargetId=target,SourceName=source_name,TargetName=target_name,Weight=weight,SharedGenres=genres)
            assoc_obj.save()
            return True
        else:
            return False
        
    def network_exists(self, session_id, timeframe):
        try:
            network = ArtistNetworks.objects.get(SessionId=session_id, Timeframe=timeframe)
            if network:
                return True
            return False
        except ArtistNetworks.DoesNotExist:
            return False
        
    def save_network(self, session_id, timeframe, network):
        exists = self.network_exists(session_id, timeframe)
        if(not exists):
            nodes = network['Nodes']
            links = network['Links']
            network_obj = ArtistNetworks(SessionId=session_id,Timeframe=timeframe,Nodes=nodes,Links=links)
            network_obj.save()
            return True
        else:
            return False
    
    def get_network(self, session_id, timeframe):
        try:
            return ArtistNetworks.objects.get(SessionId=session_id, Timeframe=timeframe)
        except ArtistNetworks.DoesNotExist:
            return None