import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

@api_view(['GET'])
def google_login(request):
    """
    Redirect the user to the Google OAuth 2.0 authorization endpoint.
    """
    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'response_type=code&'
        f'client_id={settings.GOOGLE_CLIENT_ID}&'
        f'redirect_uri={settings.GOOGLE_REDIRECT_URI}&'
        'scope=email%20profile'
    )
    return Response({'auth_url': google_auth_url})

@swagger_auto_schema(
    method='post',
    request_body=GoogleCallbackSerializer,
    responses={
        200: GoogleCallbackResponseSerializer,
        400: 'Bad Request - Invalid or missing authorization code',
    },
    operation_description="Exchange authorization code for an access token and authenticate the user"
)
@api_view(['POST'])
def google_callback(request):
    """
    Handle the callback from Google OAuth after the user authorizes the app.
    Exchange the authorization code for an access token and authenticate the user.
    """
    code = request.data.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code != 200:
        return Response({'error': 'Failed to fetch access token from Google.'}, status=status.HTTP_400_BAD_REQUEST)

    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Use the access token to fetch user information from Google
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    userinfo_response = requests.get(userinfo_url, params={'access_token': access_token})

    if userinfo_response.status_code != 200:
        return Response({'error': 'Failed to fetch user information from Google.'}, status=status.HTTP_400_BAD_REQUEST)

    userinfo = userinfo_response.json()
    email = userinfo.get('email')
    first_name = userinfo.get('given_name')
    last_name = userinfo.get('family_name')

    # Check if the user already exists, otherwise create a new user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()  # Since they're logging in via Google, no password is set.
        user.save()

    # Generate or retrieve authentication token for the user
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    })
