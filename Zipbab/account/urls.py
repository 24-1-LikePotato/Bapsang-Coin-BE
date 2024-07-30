from django.contrib import admin
from django.urls import path

from .views import ActivateSubscriptionView

urlpatterns = [
     path('subcribe/<int:user_id>/', ActivateSubscriptionView.as_view(), name='activate-subscription'),
]