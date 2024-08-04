from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
     path('subcribe/<int:user_id>', ActivateSubscriptionView.as_view(), name='activate-subscription'),
     path('kakao/login', kakao_login, name = 'kakao_login'),
     path('kakao/callback', kakao_callback, name= 'kakao_callback'),
     path('logout',LogoutView.as_view(), name = 'logout'),
     path('token/refresh',TokenRefreshView.as_view(), name= 'token_refresh'),
]