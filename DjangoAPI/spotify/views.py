from django.shortcuts import render, redirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from .util import update_or_create_user_tokens, is_spotify_authenticated, get_access_token
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json

# Create your views here.

# API endpoints to authenticate our application / request access
class AuthURL(APIView):
    #returns url that redirects to spotify login
    def get(self, request, format=None):
        scopes = 'user-read-private user-read-email user-top-read user-read-recently-played' #what operations and info we want to access from spotify api
        # url redirecting to spotify login + request for authorization
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)
    # https://accounts.spotify.com/authorize?scope=user-top-read+user-read-recently-played&response_type=code&redirect_uri=
    
# Handles redirect after successful request for AuthURL
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
        print("token: " + access_token)
        token_type = response.get('token_type')
        refresh_token = response.get('refresh_token')
        expires_in = response.get('expires_in')
        error = response.get('error')
        
        if not request.session.exists(request.session.session_key):
            request.session.create()

        update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
        
        frontend_url = 'http://localhost:4200/artists-network'
        return redirect(f'{frontend_url}?token={request.session.session_key}')
    
class IsAuthenticated(APIView):
    def post(self, request, formate=None):
        data = json.loads(request.body)
        session = data['session_id']
        is_authenticated = is_spotify_authenticated(session)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
  
class SpotifyUser(APIView):
    #TODO: Remove this endpoint/view
    def get(self, request, formate=None):
        data = json.loads(request.body)
        session = data['session_id']
        access_token = get_access_token(session)
        # GET request to spotify api https://api.spotify.com/v1/me with access_token as header -> output to response
        
        auth_token = "Bearer " + access_token
        headers = {
            'Authorization': auth_token,
        }
        
        response = get('https://api.spotify.com/v1/me', headers=headers).json()
        print(response)
        # username = response.get('display_name')
        # email = response.get('email')
        return Response(response, status=status.HTTP_200_OK)
        
class TopArtists(APIView):
    def get(self, request, formate=None):
        return ""