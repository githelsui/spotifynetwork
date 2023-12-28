from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Artists

class NetworkDAO:
    def __init__(self):
        # TODO: Initialize Logger object for DAO Layer
        self.Logger = ''
    
    def artist_exists(self, artist_id):
        return ''
    
    def save_artist(self, artist):
        return ''