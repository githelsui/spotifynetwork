from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Artists, ArtistAssocs, ArtistNetworks
from Logging.logger import Logger

class NetworkDAO:
    def __init__(self):
        self.Logger = Logger()
    
    def artist_exists(self, artist_id):
        try:
            artist = Artists.objects.get(ArtistId=artist_id)
            if artist:
                return True
            return False
        except Artists.DoesNotExist:
            return False
        except Exception as e:
            self.Logger.log(f'Failed to fetch artist exist from database. Error: {e}', 'error', 'data access layer', 'get-artist-exists-dao', 0)
            return False
    
    def get_artist(self, artist_id):
        try:
            return Artists.objects.get(ArtistId=artist_id)
        except Exception as e:
            self.Logger.log(f'Failed to fetch artist from database. Error: {e}', 'error', 'data access layer', 'get-artist-dao', 0)
            return None
    
    def save_artist(self, artist):
        exists = self.artist_exists(artist['ArtistId'])
        if(not exists):
            try:
                id = artist['ArtistId']
                name = artist['ArtistName']
                popularity = artist['ArtistPopularity']
                genre = artist['ArtistGenre']
                image = artist['ArtistImage']
                url = artist['ArtistUrl']
                similar = artist['SimilarArtists']
                artist_obj = Artists(ArtistId=id, ArtistName=name, ArtistPopularity=popularity, ArtistGenre=genre, ArtistImage=image, SimilarArtists=similar, ArtistUrl=url)
                artist_obj.save()
                self.Logger.log(f'Successfully saved new artist to database.', 'info', 'data access layer', 'save-artist-dao', 1)
                return True
            except Exception as e:
                self.Logger.log(f'Failed to save artist to database. Error: {e}', 'error', 'data access layer', 'save-artist-dao', 0)
                return False
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
        except Exception as e:
            self.Logger.log(f'Failed to fetch assoc or link existence from database. Error: {e}', 'error', 'data access layer', 'get-assoc-exists-dao', 0)
            return False
    
    def get_assoc(self, source, target):
        try:
            return ArtistAssocs.objects.get(SourceId=source, TargetId=target)
        except ArtistAssocs.DoesNotExist:
            return None
        except Exception as e:
            self.Logger.log(f'Failed to fetch assoc or link obj from database. Error: {e}', 'error', 'data access layer', 'get-assoc-dao', 0)
            return False
        
    def save_assoc(self, assoc):
        exists = self.assoc_exists(assoc['source'], assoc['target'])
        if(not exists):
            try:
                source = assoc['source']
                target = assoc['target']
                source_name = assoc['source_name']
                target_name = assoc['target_name']
                weight = assoc['weight']
                genres = assoc['genres']
                assoc_obj = ArtistAssocs(SourceId=source,TargetId=target,SourceName=source_name,TargetName=target_name,Weight=weight,SharedGenres=genres)
                assoc_obj.save()
                self.Logger.log(f'Successfully saved new association to database', 'info', 'data access layer', 'save-assoc-dao', 1)
                return True 
            except Exception as e:
                self.Logger.log(f'Failed to save association to database. Error: {e}', 'error', 'data access layer', 'save-assoc-dao', 0)
                return False
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
        except Exception as e:
            self.Logger.log(f'Failed to fetch network existence from database. Error: {e}', 'error', 'data access layer', 'get-network-exist-dao', 0)
            return False
    
    def get_network(self, session_id, timeframe):
        try:
            return ArtistNetworks.objects.get(SessionId=session_id, Timeframe=timeframe)
        except ArtistNetworks.DoesNotExist:
            return None
        except Exception as e:
            self.Logger.log(f'Failed to fetch network obj from database. Error: {e}', 'error', 'data access layer', f'get-{timeframe}-network-dao', 0)
            return False
        
    def save_network(self, session_id, timeframe, network):
        exists = self.network_exists(session_id, timeframe)
        if(not exists):
            try:
                nodes = network['Nodes']
                links = network['Links']
                network_obj = ArtistNetworks(SessionId=session_id,Timeframe=timeframe,Nodes=nodes,Links=links)
                network_obj.save()
                self.Logger.log(f'Successfully saved new network to database', 'info', 'data access layer', 'save-network-dao', 1)
                return True
            except Exception as e:
                self.Logger.log(f'Failed to save network to database. Error: {e}', 'error', 'data access layer', 'save-network-dao', 0)
                return False
        else:
            return False