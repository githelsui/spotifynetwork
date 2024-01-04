from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Users
from Logging.logger import Logger

class UserDAO:
    
    # init method or constructor
    def __init__(self):
        self.Logger = Logger()
    
    def user_exists(self, user):    
        try:
            email = user['UserEmail']
            user = Users.objects.get(UserEmail=email)
            if user:
                return True
            return False
        except Users.DoesNotExist:
            return False
        except Exception as e:
            self.Logger.log(f'Failed to fetch user from database. Error: {e}', 'error', 'data access layer', 'get-user-exists-dao', 0)
            return False
    
    def save_user(self, user):
        try:
            username = user['UserName']
            email = user['UserEmail']
            user = Users(UserEmail=email, UserName=username)
            user.save()
            self.Logger.log('Successfully saved newly created user to app.', 'info', 'data access layer', 'create-user-dao', 1)
        except Exception as e:
            self.Logger.log(f'Failed to save user to database. Error: {e}', 'error', 'data access layer', 'create-user-dao', 0)