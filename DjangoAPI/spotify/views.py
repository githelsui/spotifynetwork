from django.shortcuts import render
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post

# Create your views here.

# API endpoints to authenticate our application / request access
class AuthURL(APIView):
    
    #returns url that redirects to spotify login
    def get(self, request, format=None):
        scopes = 'user-top-read user-read-recently-played' #what operations and info we want to access from spotify api
        # url redirecting to spotify login + request for authorization
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI
        }).prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)
    
    def spotify_callback(request, format=None):
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET
        }).json()
        
        # look at json response
        access_token = response.get('access_token')
        token_type = response.get('token_type')
        refresh_token = response.get('refresh_token')
        expires_in = response.get('expires_in')
        error = response.get('error')
        
        