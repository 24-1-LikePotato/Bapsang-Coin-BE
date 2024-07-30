from django.contrib import admin
from django.urls import path
from .views import FridgeDetailView,RecipeStoreView, RecipeIngredientStoreView, RecipeStoreView

urlpatterns = [
    path('fridge/<int:user_id>', FridgeDetailView.as_view(), name='fridge-detail'),
    path('recipe/update-all-ingredients', RecipeIngredientStoreView.as_view(), name='update-all-recipe-ingredients'),
    path('recipe', RecipeStoreView.as_view()),
    path('today-recipe', views.TodayRecipeView.as_view()),
]