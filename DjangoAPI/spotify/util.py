from .models import SpotifyToken
from datetime import timedelta
from django.utils import timezone
from requests import Request, post, get
from .credentials import CLIENT_ID, CLIENT_SECRET
from Logging.logger import Logger

logger = Logger()
# -- Authentication / Authorization Core Component Feature --
# Handling tokens from Spotify API
def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        logger.log('Successfully received Spotify session tokens', 'info', 'service', 'get-session-spotify-token', 1, session_id)
        return user_tokens[0]
    else:
        logger.log('Successfully found zero spotify tokens for session', 'info', 'service', 'get-session-spotify-token', 1, session_id)
        return None
    
def get_access_token(session_id):
    current_session = get_user_tokens(session_id)
    if current_session:
        logger.log('Successfully received Spotify access tokens', 'info', 'service', 'get-access-spotify-token', 1, session_id)
        return current_session.access_token
    else:
        logger.log('Successfully found zero spotify access tokens for session', 'info', 'service', 'get-access-spotify-token', 1, session_id)
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
        logger.log('Successfully updated spotify session token', 'info', 'service', 'update-session-spotify-token', 1, session_id)
    else: #create new token if user has never had a session before
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()
        logger.log('Successfully created spotify session token', 'info', 'service', 'create-session-spotify-token', 1, session_id)

        
def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now(): #session is authenticated if token is not expired
            # if current expiration date has passed, refresh the token
            refresh_spotify_token(session_id)
        logger.log('Successfully authenticated spotify user', 'info', 'service', 'auth-spotify-user', 1, session_id)
        return True
    # user is not authenticated
    logger.log('Successfully flagged invalid authentication attemp for spotify user', 'info', 'service', 'auth-spotify-user', 1, session_id)
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
    
    if 'error' in response:
        logger.log('Failed to refresh spotify token', 'error', 'service', 'refresh-spotify-token',0,session_id)
    else:
        logger.log('Successfully refreshed spotify token', 'info', 'service', 'refresh-spotify-token',1,session_id)
        
    # gets new access token info from the spotify api
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)
        
        
def get_spotify_account(session_id):
    status = None 
    item = None
    access_token = get_access_token(session_id)
    headers = {'Authorization': 'Bearer ' + access_token}
        
    response = get('https://api.spotify.com/v1/me', headers=headers).json()

    if 'error' in response: #API returned an error
        logger.log('Failed to get spotify user', 'error', 'service', 'get-spotify-user',0,session_id)
        status = False 
    else:
        username = response.get('display_name')
        email = response.get('email')
        user = {
            'UserName': username,
            'UserEmail': email
        }
        item = user
        status = True
        logger.log('Successfully fetched spotify user', 'info', 'service', 'get-spotify-user',1,session_id)
    result = {'status': status, 'item': item}
    return result

# -- Artist Network Feature -- 
def get_user_top_artists(session_id, timeframe):
    
    status = None 
    item = None
    
    is_authenticated = is_spotify_authenticated(session_id)
    if is_authenticated:
        access_token = get_access_token(session_id)
        headers = {'Authorization': 'Bearer ' + access_token}
        
        url = 'https://api.spotify.com/v1/me/top/artists?limit=30&time_range=' + timeframe
        response = get(url, headers=headers).json()
    
        if 'error' in response: #API returned an error
            logger.log('Failed to get spotify user top artists', 'error', 'service', 'get-spotify-top-artists',0,session_id)
            status = False 
        else:
            items = response.get('items')
            artists = []
            rank = 1
            for artist in items:
                artObj = {
                    'id': artist['id'],
                    'name': artist['name'],
                    'popularity': artist['popularity'],
                    'genres': artist['genres'],
                    'rank': rank,
                    'image': 'https://www.samys.com/images/product/main/S-008607x1000.jpg' if len(artist['images'])==0 else artist['images'][0]['url'],
                    'url': 'https://spotify.com' if len(artist['external_urls']) == 0 else artist['external_urls']['spotify']
                }
                artists.append(artObj)
                rank += 1
            item = artists
            status = True
            logger.log('Successfully fetched spotify user top artists', 'info', 'service', 'get-spotify-top-artists',1,session_id)
    else:
        status = False 
        item = {'Message':'User is not authenticated via Spotify'}
    result = {'status': status, 'item': item}
    return result

def get_related_artists(session_id, artist_id):
    status = None 
    item = None
    
    access_token = get_access_token(session_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/related-artists'
    response = get(url, headers=headers).json()
    if 'error' in response: #API returned an error
        logger.log('Failed to get spotify related artists', 'error', 'service', 'get-spotify-related-artists',0,session_id)
        status = False 
    else:
        neighbors = []
        related_artists = response['artists']
        relatability_score = len(related_artists)
        for artist in related_artists:
            artObj = {
                'id': artist['id'],
                'name': artist['name'],
                'popularity': artist['popularity'],
                'genres': artist['genres'],
                'relatability_score': relatability_score
            }
            neighbors.append(artObj)
            relatability_score -= 1
        item = neighbors
        status = True 
        logger.log('Successfully fetched spotify related artists', 'info', 'service', 'get-spotify-related-artists',1,session_id)
    result = {'status': status, 'item': item}
    return result