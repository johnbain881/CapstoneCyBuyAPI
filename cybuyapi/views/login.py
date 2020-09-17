import json
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']

        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the registration of a user'''

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        try:
            user = User.objects.create_user(
                first_name=req_body["first_name"],
                last_name=req_body["last_name"],
                username=req_body["username"],
                password=req_body["password"],
                email=req_body["email"]
            )

            token = Token.objects.create(user=user)

            data = json.dumps({"token": token.key})
            return HttpResponse(data, content_type='application/json')
        except Exception as ex:
            return HttpResponseServerError(ex)