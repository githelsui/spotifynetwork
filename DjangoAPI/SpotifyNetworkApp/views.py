from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from.user_manager import UserManager
from.network_manager import NetworkManager
from SpotifyNetworkApp.models import Users, Artists, ArtistAssocs
from SpotifyNetworkApp.serializers import UsersSerializer, ArtistsSerializer, ArtistAssocsSerializer
import json
#Todo: dev only, remove
from spotify.util import get_user_top_artists, get_related_artists

# Create your views here.
class UserSignIn(APIView):
    
      # init method or constructor
    def __init__(self):
        self.UserManager = UserManager()
         # TODO: Initialize Logger object for View Layer
        self.Logger = ''
        
    def post(self, request, formate=None):
        data = json.loads(request.body)
        session_id = data['session_id']
        response = self.UserManager.sign_in(session_id)
        if not response['status']:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            user = response['item']
            return Response({'item': user}, status=status.HTTP_200_OK)
        
class ArtistNetwork(APIView):
    
    # init method or constructor
    def __init__(self):
        self.NetworkManager = NetworkManager()
         # TODO: Initialize Logger object for View Layer
        self.Logger = ''
        
    def post(self, request, formate=None):
        item = None
        data = json.loads(request.body)
        session_id = data['session_id']
        timeframe = data['timeframe']
        response = self.NetworkManager.get_network(session_id, timeframe)
        if not response['status']:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            item = response['item']
            return Response({'item': item}, status=status.HTTP_200_OK)