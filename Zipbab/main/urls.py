from django.contrib import admin
from django.urls import path

from .views import FridgeDetailView

urlpatterns = [

    path('fridge/<int:user_id>', FridgeDetailView.as_view(), name='fridge-detail'),

]