from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post, get
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import Users

class UserDAO:
    
    # init method or constructor
    def __init__(self):
        # TODO: Initialize Logger object for DAO Layer
        self.Logger = ''
    
    def user_exists(self, user):
        email = user['UserEmail']
        print("Email: " + email)
        
        try:
            user = Users.objects.get(UserEmail=email)
            if user:
                return True
            return False
        except Users.DoesNotExist:
            print("Does not exist")
            return False
    
    def save_user(self, user):
        username = user['UserName']
        email = user['UserEmail']
        user = Users(UserEmail=email, UserName=username)
        user.save()
        return ''