from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from spotify.util import get_user_top_artists, get_related_artists 
from .network_service import NetworkService
from .network_dao import NetworkDAO
import json
from Logging.logger import Logger

class NetworkManager:
    def __init__(self):
        self.NetworkService = NetworkService()
        self.NetworkDAO = NetworkDAO()
        self.Logger = Logger()
    
    def get_network(self, session_id, timeframe):
        status = None
        item = None
        
        network = self.NetworkDAO.get_network(session_id, timeframe)
        if network:
            # Get saved network data for that session and timeframe selection
            status = True
            item = {'Nodes': network.Nodes, 'Links': network.Links}
            self.Logger.log(f'Successfully fetched saved network from database', 'info', 'manager', f'get-{timeframe}-network-dao', 1, session_id)    
        else:
            # Create new network data
            self.Logger.log(f'Attempt to create a new {timeframe} network', 'info', 'manager', f'create-{timeframe}-network')    
            response = self.extract_data(session_id, timeframe)
            status = response['status']
            if status:
                data = response['item']
                graph = self.NetworkService.get_graph(data)
                self.NetworkDAO.save_network(session_id, timeframe, graph)
                item = graph
                status = True
                self.Logger.log(f'Successful attempt to create a new {timeframe} network', 'info', 'manager', f'create-{timeframe}-network', 1, session_id)    
            else:
                status = False 
                self.Logger.log(f'Failed attempt to create a new {timeframe} network', 'error', 'manager', f'create-{timeframe}-network', 0, session_id)    
        result = {'status': status, 'item': item}
        return result 
    
    def extract_data(self, session_id, timeframe):
        status = None
        item = None
        response1 = get_user_top_artists(session_id, timeframe)
        status = response1['status']
        if status:
            item = response1['item']
            # Get related artists
            for artist in item:
                artist_id = artist['id']
                # Get artist objects from database if they exist
                exists_db = self.NetworkDAO.artist_exists(artist_id)
                if not exists_db:
                    self.Logger.log('Attempt to create a new artist', 'info', 'manager', 'create-new-artist')    
                    response2 = get_related_artists(session_id, artist_id)
                    status = response2['status']
                    if not status: #Error from Spotifyapi call -> return false status for entire function
                        self.Logger.log('Failed attempt to fetch related artists', 'error', 'manager', 'get-spotify-related-artists', 0)    
                        break
                    artist['similar_artists'] = response2['item']
                else:
                    artist_db = self.NetworkDAO.get_artist(artist_id)
                    artist['similar_artists'] = artist_db.SimilarArtists
                    self.Logger.log('Successful attempt to get saved artist from database', 'info', 'manager', 'get-artist-dao', 1)    
            self.Logger.log('Successful attempt to get top artists', 'info', 'manager', 'get-spotify-top-artists', 1)    
        else:
            status = False 
            self.Logger.log('Failed attempt to fetch top artists', 'error', 'manager', 'get-spotify-top-artists', 0)    
        result = {'status': status, 'item': item}
        return result 