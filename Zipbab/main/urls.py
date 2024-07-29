from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('ingredient/', views.ingredientpage, name='ingredient-page')
]