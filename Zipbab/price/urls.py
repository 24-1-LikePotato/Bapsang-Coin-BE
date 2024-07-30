from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('ingredient-price', views.UpdateIngredientPriceView.as_view(), name='update-ingredient-price'),
]