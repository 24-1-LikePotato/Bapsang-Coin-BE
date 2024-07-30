from django.contrib import admin
from django.urls import path
from .views import FridgeDetailView, RecipeStoreView, RecipeIngredientStoreView,TodayRecipeView,RecipeSearchView,MonthSearchView
from . import views




urlpatterns = [
    path('recipe/search',RecipeSearchView.as_view() , name='recipe-search'),
    path('search/', MonthSearchView.as_view(), name='ingredient-search'),
    path('related_recipe/', views.related_recipe, name='related-recipe'),
    path('search/', MonthSearchView.as_view(), name='ingredient-search'),
    path('fridge/<int:user_id>', FridgeDetailView.as_view(), name='fridge-detail'),
    path('recipe/update-all-ingredients', RecipeIngredientStoreView.as_view(), name='update-all-recipe-ingredients'),
    path('recipe',RecipeStoreView.as_view()),
    path('today-recipe', TodayRecipeView.as_view()),
]