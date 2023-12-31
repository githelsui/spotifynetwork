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
        self.link_pairs = set() #unique pairs only
    
    def get_graph(self, data):
        # get nodes
        self.nodes = self.get_nodes(data)
        # get links
        self.get_links(data)
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
                'ArtistImage': artist['image'],
                'SimilarArtists': artist['similar_artists']
            }
            artistsDAO.append(artistDao)
            self.NetworkDAO.save_artist(artistDao)
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
        for source_node in self.nodesDAO:
            for target_node in self.nodesDAO:
                source_id = source_node['ArtistId']
                target_id = target_node['ArtistId']
                if source_id != target_id and self.is_unique_link(source_node, target_node): 
                    assoc = self.NetworkDAO.get_assoc(source_id, target_id)
                    if assoc:
                        assoc_api = assoc.convert_api()
                        self.links.append(assoc_api)
                        primary_key = source_id + ':' + target_id
                        self.link_pairs.add(primary_key)
                    else:
                        self.create_link(source_node, target_node)
    
    def is_unique_link(self, source, target):
        source_id = source['ArtistId']
        target_id = target['ArtistId']
        if (source_id + ':' + target_id) in self.link_pairs:
            return False 
        if (target_id + ':' + source_id) in self.link_pairs:
            return False 
        return True
    
    def create_link(self, source_node, target_node):
        #get node connections and their weights
        weight = self.get_weight(source_node, target_node)
        if weight > 0:
            genres = self.get_genres(source_node, target_node)
            link = {
                'source': source_node['ArtistId'],
                'target': target_node['ArtistId'],
                'source_name': source_node['ArtistName'],
                'target_name': target_node['ArtistName'],
                'weight': weight,
                'genres': genres
            }
            self.links.append(link)
            primary_key = source_node['ArtistId'] + ':' + target_node['ArtistId']
            self.link_pairs.add(primary_key)
            self.NetworkDAO.save_assoc(link)
    
    def get_genres(self, source_node, target_node):
        combined = []
        genres1 = source_node['ArtistGenre']
        genres2 = target_node['ArtistGenre']
        combined.extend(genres1)
        combined.extend(genres2)
        shared_genres = set(combined) #remove duplicates
        return list(shared_genres)

    
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
    