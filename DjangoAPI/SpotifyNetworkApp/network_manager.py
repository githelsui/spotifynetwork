from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from spotify.util import get_user_top_artists, get_related_artists 
from .network_service import NetworkService
import json

class NetworkManager:
    def __init__(self):
        self.NetworkService = NetworkService()
         # TODO: Initialize Logger object for Manager Layer
        self.Logger = ''
    
    def get_network(self, session_id, timeframe):
        status = None
        item = None
        
        response = self.extract_data(session_id, timeframe)
        status = response['status']
        if status:
            data = response['item']
            graph = self.NetworkService.get_graph(data)
            item = graph
            status = True
        else:
            status = False 
        result = {'status': status, 'item': item}
        return result 
    
    def extract_data(self, session_id, timeframe):
        status = None
        item = None
        response1 = get_user_top_artists(session_id, timeframe)
        status = response1['status']
        if status:
            item = response1['item']
            for artist in item:
                artist_id = artist['id']
                response2 = get_related_artists(session_id, artist_id)
                status = response2['status']
                if not status:
                    break
                artist['similar_artists'] = response2['item']
        else:
            status = False 
        result = {'status': status, 'item': item}
        return result 