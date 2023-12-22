from .models import SpotifyToken
from datetime import timedelta
from django.utils import timezone
from requests import Request, post
from .credentials import CLIENT_ID, CLIENT_SECRET

# Handling tokens from Spotify API

def get_user_tokens(session_id):
    print("session id in get_user_tokens = " + str(session_id))
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    # check if user already has sessions running
    tokens = get_user_tokens(session_id)
    # converts expires_in to an actual datetime
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    # update existing token if user already had a session before
    if tokens:
        tokens.access_token = access_token 
        tokens.refresh_token = refresh_token 
        tokens.expires_in = expires_in 
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type']) 
        print("Token being updated")
    else: #create new token if user has never had a session before
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()
        print("New token being saved")
        
def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now(): #session is authenticated if token is not expired
            # if current expiration date has passed, refresh the token
            refresh_spotify_token(session_id)
        return True
    # user is not authenticated
    return False

def refresh_spotify_token(session_id):
    # send request to spotify api that refreshes the access token
    refresh_token = get_user_tokens(session_id).refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID, 
        'client_secret': CLIENT_SECRET
    }).json() 
    
    # gets new access token info from the spotify api
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)
        