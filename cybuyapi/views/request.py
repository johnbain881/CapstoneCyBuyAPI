import json
from django.http import HttpResponse
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from cybuyapi.models import Request, RequestPhoto
from django.contrib.auth.models import User


class RequestPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequestPhoto
        fields = ('id', 'request', 'photo_url')

class RequestSerializer(serializers.HyperlinkedModelSerializer):
    photos = RequestPhotoSerializer(many=True)
    class Meta:
        model = Request
        url = serializers.HyperlinkedIdentityField(
            view_name='request',
            lookup_field='id'
        )
        fields = ('id', 'user', 'title', 'body', 'photos')
        depth = 2


class Requests(ViewSet):

    def create(self, request):
        """Handle POST requests"""

        
        user_request = Request.objects.create(
            user = request.user,
            title = request.data["title"],
            body = request.data["body"],
        )
        for photo in request.data["photos"]:
            if photo != "":
                RequestPhoto.objects.create(
                    request = user_request,
                    photo_url = photo,
                )
        
        serializer = RequestSerializer(user_request, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests"""

        user_request = Request.objects.get(pk=pk)

        serializer = RequestSerializer(user_request, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests"""
        user_request = Request.objects.get(pk=pk)
        user_request.body = request.data["body"]
        user_request.title = request.data["title"]
        user_request.save()

        photos = RequestPhoto.objects.filter(request=user_request).delete()
        for photo in request.data["photos"]:
            if photo != "":
                RequestPhoto.objects.create(
                    request = user_request,
                    photo_url = photo,
                )
        
        serializer = RequestSerializer(user_request, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests"""
        user_request = Request.objects.get(pk=pk)
        user_request.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def list(self, request):
        """Handle GET requests"""
        user_request = Request.objects.all().order_by('-id')
        serializer = RequestSerializer(user_request, many=True, context={'request' : request})
        return Response(serializer.data)