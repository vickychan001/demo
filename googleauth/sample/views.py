from django.shortcuts import render

# Create your views here.
import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class GoogleLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Google OAuth login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Google OAuth Token'),
            },
            required=['token'],
        ),
        responses={200: "Success", 400: "Bad Request"}
    )
    def post(self, request):
        token = request.data.get("token", None)
        if token is None:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify token with Google
        google_verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(google_verify_url)

        if response.status_code != 200:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        google_data = response.json()

        # Process the returned data
        email = google_data.get('email')
        name = google_data.get('name')

        # Authenticate or create user
        user, created = User.objects.get_or_create(email=email, defaults={"username": name})
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": user.username}, status=status.HTTP_200)

