from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
     path('subcribe/<int:user_id>/', ActivateSubscriptionView.as_view(), name='activate-subscription'),
     path('kakao/login', kakao_login, name = 'kakao_login'),
     path('kakao/callback', kakao_callback, name= 'kakao_callback'),
]