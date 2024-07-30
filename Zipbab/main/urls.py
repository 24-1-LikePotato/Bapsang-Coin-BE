from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('recipe', views.RecipeStoreView.as_view()),
    path('today-recipe', views.TodayRecipeView.as_view()),
]