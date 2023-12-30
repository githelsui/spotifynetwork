from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .network_dao import NetworkDAO
import json

class NetworkService:
    def __init__(self):
        self.NetworkDAO = NetworkDAO()
        self.nodes = [] #data to be sent to client via our web api
        self.nodesDAO = [] #data to be saved to DAO
        self.links = []
    
    def get_graph(self, data):
        # get nodes
        self.nodes = self.get_nodes(data)
        # get links
        self.links = self.get_links(data)
        return {'Nodes': self.nodes, 'Links': self.links}
        
    def get_nodes(self, data):
        artistsDAO = []
        artistsAPI = []
        for artist in data:
            artistDao = {
                'ArtistId': artist['id'],
                'ArtistName': artist['name'],
                'ArtistPopularity': artist['popularity'],
                'ArtistGenre': [] if (len(artist['genres']) == 0 or artist['genres'][0] == 'None') else artist['genres'],
                'ArtistRank': artist['rank'],
                'ArtistImage': artist['image'],
                'SimilarArtists': artist['similar_artists']
            }
            artistsDAO.append(artistDao)
            artistAPI = {
                'id': artist['id'],
                'name': artist['name'],
                'popularity': artist['popularity'],
                'genre': "N/A" if (len(artist['genres']) == 0 or artist['genres'][0] == 'None') else artist['genres'][0],
                'genres': artistDao['ArtistGenre'],
                'image': artist['image'],
                'rank': artist['rank'],
            }
            artistsAPI.append(artistAPI)
        self.nodesDAO = artistsDAO
        return artistsAPI
        
    def get_links(self, data):
        links = []
        for source_node in self.nodesDAO:
            for target_node in self.nodesDAO:
                if source_node['ArtistId'] != target_node['ArtistId']: 
                    #get node connections and their weights
                    weight = self.get_weight(target_node, source_node)
                    if weight > 0:
                        # TODO: Shared genres between two artists
                        # genres1 = source_node['ArtistGenre']
                        # genres2 = target_node['ArtistGenre']
                        # # print("\ngenres 1:")
                        # print(genres1)
                        # print("\ngenres 2:")
                        # print(genres2)
                        # genres1.extend(genres2)
                        # print("\nshared genres:")
                        # print(genres1)
                        # shared_genres = set(genres1)
                        # print("\set genres:")
                        # print(shared_genres)
                        link = {
                            'source': source_node['ArtistId'],
                            'target': target_node['ArtistId'],
                            'source_name': source_node['ArtistName'],
                            'target_name': target_node['ArtistName'],
                            'weight': weight,
                            # 'genres': shared_genres
                        }
                        links.append(link)
                        # update artist node with new neighbor
                        
        return links
    
    def get_neighbors(self):
        for artist in self.nodes:
            artist_id = artist['id']
            
    
    def get_weight(self, artist1, artist2):
        weight = 0
        # p0: relatability score
        relatability_score = self.is_similar_artist(artist1, artist2)
        weight += relatability_score
        # p1: genres
        weight += self.similar_genres(artist1, artist2)
        return weight
    
    def is_similar_artist(self, artist1, artist2):
        id_1 = artist1['ArtistId']
        id_2 = artist2['ArtistId']
        neighbors1 = artist1['SimilarArtists']
        neighbors2 = artist2['SimilarArtists']
        # artist1 exists in artist2's similar artists
        for neighbor in neighbors2:
            neighbor_id = neighbor['id']
            if id_1 == neighbor_id:
                return neighbor['relatability_score']
        # artist2 exists in artist1's similar artists
        for neighbor in neighbors1:
            neighbor_id = neighbor['id']
            if id_2 == neighbor_id:
                return neighbor['relatability_score']
        return 0
    
    def similar_genres(self, artist1, artist2):
        score = 0
        artist1_genres = artist1['ArtistGenre']
        artist2_genres = artist2['ArtistGenre']
        for genre in artist1_genres:
            if genre in artist2_genres:
                score += 1
        return score
    