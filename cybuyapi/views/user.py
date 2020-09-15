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
from django.contrib.auth.models import User



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'username', 'first_name', 'last_name')
        depth = 1


class Users(ViewSet):

    def create(self, request):
        """Handle POST requests"""

        try:
            user = User.objects.create_user(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                username=request.data["username"],
                password=request.data["password"],
                email=request.data["email"]
            )

            token = Token.objects.create(user=user)

            data = json.dumps({"token": token.key})
            return HttpResponse(data, content_type='application/json')
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """Handle GET requests"""

        user = User.objects.get(pk=pk)
        
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests"""

        user = User.objects.get(pk=pk)
        user.email = request.data["email"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests"""
        user = User.objects.get(pk=pk)
        user.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def list(self, request):
        """Handle GET requests"""
        user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request' : request})
        return Response(serializer.data)