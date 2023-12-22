from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from.user_dao import UserDAO
from spotify.util import get_spotify_account 
import json

class UserManager:
    
    # init method or constructor
    def __init__(self):
        self.UserDao = UserDAO()
         # TODO: Initialize Logger object for Manager Layer
        self.Logger = ''
        
    def sign_in(self, session):
        status = None
        item = None
        
        response = get_spotify_account(session)
        status = response['status']
        if status:
            item = response['item']
            if self.UserDao.user_exists(item):
                status = True
            else: # User has a spotify account but has never made an account with our web app/their first time entering app
                self.UserDao.save_user(item)
                status = True
        else:
            status = False
            
        result = {'status': status, 'item': item}
        return result