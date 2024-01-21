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
from Logging.logger import Logger
from Logging.publisher import Publisher
from rest_framework.throttling import UserRateThrottle
from django_ratelimit.decorators import ratelimit

# Create your views here.
class UserSignIn(APIView):
    
    # init method or constructor
    def __init__(self):
        self.UserManager = UserManager()
        self.Logger = Logger()
    
    # @ratelimit(key='post:sign-in', rate='150/m', block=True)
    def post(self, request, formate=None):
        # throttle_classes = [UserRateThrottle]
         
        self.Logger.log('Attempt/request to sign user in', 'info', 'view', 'sign-in-user')    
        data = json.loads(request.body)
        session_id = data['session_id']
        response = self.UserManager.sign_in(session_id)
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not response['status']:
                self.Logger.log('Failed attempt/request to sign user in', 'error', 'view', 'sign-in-user', 0)    
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                self.Logger.log('Successful user sign in', 'info', 'view', 'sign-in-user', 1)    
                user = response['item']
                return Response({'item': user}, status=status.HTTP_200_OK)
        
class ArtistNetwork(APIView):
    
    # init method or constructor
    def __init__(self):
        self.NetworkManager = NetworkManager()
        self.Logger = Logger()
        self.Publisher = Publisher()
    
    # @ratelimit(key='post:get-network', rate='150/m', block=True)
    def post(self, request, formate=None):
        # throttle_classes = [UserRateThrottle]
        
        item = None
        data = json.loads(request.body)
        session_id = data['session_id']
        timeframe = data['timeframe']
        self.Logger.log(f'Request to render {timeframe} artist network', 'info', 'view', f'request-{timeframe}-network')    
        self.Publisher.publish(f'Request to render {timeframe} artist network', 'network-selection', {'timeframe': timeframe})
        response = self.NetworkManager.get_network(session_id, timeframe)
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not response['status']:
                self.Logger.log(f'Failed request to render {timeframe} artist network', 'error', 'view', f'request-{timeframe}-network', 0)    
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                item = response['item']
                self.Logger.log(f'Successful request to render {timeframe} artist network', 'info', 'view', f'request-{timeframe}-network', 1)    
                return Response({'item': item}, status=status.HTTP_200_OK)