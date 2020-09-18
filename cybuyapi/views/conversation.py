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
from django.db.models import Q


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', 'message', 'timestamp', 'read')

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model = Conversation
        url = serializers.HyperlinkedIdentityField(
            view_name='conversation',
            lookup_field='id'
        )
        fields = ('id', 'user', 'other_user', 'messages')
        depth = 2


class Conversations(ViewSet):

    def create(self, request):
        """Handle POST requests"""
        print("userId", request.data["userId"])
        user = User.objects.get(pk=request.data["userId"])

        conversations = Conversation.objects.filter(user=request.user, other_user=user)
        if len(conversations) == 0:
            conversations = Conversation.objects.filter(user=user, other_user=request.user)
        if len(conversations) == 0:
            conversation = Conversation.objects.create(
                user = request.user,
                other_user = user,
            )
        else:
            conversation = conversations[0]
        Message.objects.create(
            conversation = conversation,
            message = request.data["message"],
            user = request.user,
        )
        
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests"""

        conversation = Conversation.objects.get(pk=pk)

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        """Handle DELETE requests"""
        conversation = Conversation.objects.get(pk=pk)
        conversation.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def list(self, request):
        """Handle GET requests"""
        conversations = Conversation.objects.filter(Q(user=request.user) | Q(other_user=request.user)).order_by('-id')
        serializer = ConversationSerializer(conversations, many=True, context={'request' : request})
        return Response(serializer.data)