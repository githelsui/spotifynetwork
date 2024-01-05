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
from Logging.logger import Logger
from Logging.publisher import Publisher
import json

class UserManager:
    
    # init method or constructor
    def __init__(self):
        self.UserDao = UserDAO()
        self.Logger = Logger()
        self.Publisher = Publisher()
        
    def sign_in(self, session_id):
        status = None
        item = None
        
        response = get_spotify_account(session_id)
        status = response['status']
        if status:
            item = response['item']
            if self.UserDao.user_exists(item):
                self.Logger.log(f'Successful attempt to sign-in an existing user for app', 'info', 'manager', 'sign-in-user', 1)
                status = True
            else: # User has a spotify account but has never made an account with our web app/their first time entering app
                self.Logger.log(f'Successful attempt to create new user for app', 'info', 'manager', 'sign-in-user', 1)
                self.UserDao.save_user(item)
                status = True
                self.Publisher.publish('Successful account registration', 'create-user-dao')
            self.Publisher.publish('Successful user sign in', 'sign-in-user')
        else:
            self.Logger.log(f'Failed to sign user into app. Error thrown from spotify.utils.get_spotify_account', 'error', 'manager', 'sign-in-user', 0)
            status = False
        
        result = {'status': status, 'item': item}
        return result