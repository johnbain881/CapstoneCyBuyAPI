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
from cybuyapi.models import Service, ServicePhoto
from django.contrib.auth.models import User


class ServicePhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicePhoto
        fields = ('id', 'service', 'photo_url')

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    photos = ServicePhotoSerializer(many=True)
    class Meta:
        model = Service
        url = serializers.HyperlinkedIdentityField(
            view_name='service',
            lookup_field='id'
        )
        fields = ('id', 'user', 'title', 'body', 'photos')
        depth = 2


class Services(ViewSet):

    def create(self, request):
        """Handle POST requests"""

        
        service = Service.objects.create(
            user = request.user,
            title = request.data["title"],
            body = request.data["body"],
        )
        for photo in request.data["photos"]:
            if photo != "":
                ServicePhoto.objects.create(
                    service = service,
                    photo_url = photo,
                )
        
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests"""

        service = Service.objects.get(pk=pk)

        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests"""
        service = Service.objects.get(pk=pk)
        service.body = request.data["body"]
        service.title = request.data["title"]
        service.save()

        photos = ServicePhoto.objects.filter(service=service).delete()
        for photo in request.data["photos"]:
            if photo != "":
                ServicePhoto.objects.create(
                    service = service,
                    photo_url = photo,
                )
        
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests"""
        service = Service.objects.get(pk=pk)
        service.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def list(self, request):
        """Handle GET requests"""
        search = self.request.query_params.get('search', None)
        service = Service.objects.filter(title__contains=search).order_by('-id')
        serializer = ServiceSerializer(service, many=True, context={'request' : request})
        return Response(serializer.data)