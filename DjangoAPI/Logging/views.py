from django.shortcuts import render
from rest_framework.views import APIView
import json
from Logging.publisher import Publisher
from rest_framework.response import Response
from rest_framework import status

class CloudPublisher(APIView):
    
    def __init__(self):
        self.Publisher = Publisher()
    
    def post(self, request, formate=None):
        data = json.loads(request.body)
        message = data['message']
        topic = data['topic']
        attributes = data['attributes']
        self.Publisher.publish(message, topic, attributes)
        return Response(status=status.HTTP_200_OK)