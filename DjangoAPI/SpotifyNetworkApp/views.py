from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from.user_manager import UserManager
from SpotifyNetworkApp.models import Users, Artists, ArtistAssocs
from SpotifyNetworkApp.serializers import UsersSerializer, ArtistsSerializer, ArtistAssocsSerializer
import json

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
        user = response['item']
        if not response['status']:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'item': user}, status=status.HTTP_200_OK)