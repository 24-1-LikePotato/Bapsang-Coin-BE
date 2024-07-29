from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('recipe/search/', views.recipesearch, name='recipe-search')

]