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
from cybuyapi.models import Conversation, Message
from django.contrib.auth.models import User







class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        url = serializers.HyperlinkedIdentityField(
            view_name='message',
            lookup_field='id'
        )
        fields = ('id', 'user', 'conversation', 'message', 'timestamp', 'read')
        depth = 2

class Messages(ViewSet):

    def update(self, request, pk=None):
        """Handle PUT requests"""
        message = Message.objects.get(pk=pk)
        message.read = True
        message.save()

        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data)


