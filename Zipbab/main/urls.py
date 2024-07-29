from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('ingredient/', views.ingredientpage, name='ingredient-page'),
    path('search/', views.ingredientsearch, name='ingredient-search'),
    path('related_recipe/', views.related_recipe, name='related-recipe'),
    path('recipe/search/', views.recipesearch, name='recipe-search'),
]