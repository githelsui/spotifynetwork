from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SpotifyNetworkApp.models import Users, Artists, ArtistAssocs
from SpotifyNetworkApp.serializers import UsersSerializer, ArtistsSerializer, ArtistAssocsSerializer

# Create your views here.
@csrf_exempt
def usersApi(request,id=0):
    if request.method=='GET':
        users = Users.objects.all()
        users_serializer = UsersSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
    elif request.method=='POST':
        users_data = JSONParser().parse(request)
        users_serializer = UsersSerializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse('User added successfully.', safe=False)
        return JsonResponse('Failed to add user', safe=False)
    elif request.method=='PUT':
        users_data = JSONParser().parse(request)
        users = Users.objects.get(UserID=users_data['UserId'])
        users_serializer=UsersSerializer(users, data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse('Updated user successfully.', safe=False)
        return JsonResponse('Failed to update user', safe=False)
    elif request.method=='DELETE':
        user = Users.objects.get(UserID=id)
        user.delete()
        return JsonResponse('Deleted user successfully.', safe=False)
    
@csrf_exempt
def artistsApi(request,id=0):
    if request.method=='GET':
        artists = Artists.objects.all()
        artists_serializer = ArtistsSerializer(artists, many=True)
        return JsonResponse(artists_serializer.data, safe=False)
    elif request.method=='POST':
        artists_data = JSONParser().parse(request)
        artists_serializer = ArtistsSerializer(data=artists_data)
        if artists_serializer.is_valid():
            artists_serializer.save()
            return JsonResponse('Artist added successfully.', safe=False)
        return JsonResponse('Failed to add artist', safe=False)
    elif request.method=='PUT':
        artists_data = JSONParser().parse(request)
        artists = Artists.objects.get(ArtistId=artists_data['ArtistId'])
        artists_serializer=ArtistsSerializer(artists, data=artists_data)
        if artists_serializer.is_valid():
            artists_serializer.save()
            return JsonResponse('Updated artist successfully.', safe=False)
        return JsonResponse('Failed to update artist', safe=False)
    elif request.method=='DELETE':
        artist = Artists.objects.get(ArtistId=id)
        artist.delete()
        return JsonResponse('Deleted artist successfully.', safe=False)