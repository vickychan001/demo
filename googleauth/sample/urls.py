from django.urls import path
from .views import *

urlpatterns = [
    path('auth/google/', google_login, name='google_login'),
    path('auth/callback/', google_callback, name='google_callback'),
    
]