from django.contrib import admin
from django.urls import path
from .views import FridgeDetailView, RecipeStoreView, RecipeIngredientStoreView,TodayRecipeView,RecipeSearchView,MonthSearchView,MonthStoreView
from . import views

urlpatterns = [
    path('recipe', views.recipe, name='recipe-info'),
    path('recipe/search',RecipeSearchView.as_view() , name='recipe-search'),
    path('search', MonthSearchView.as_view(), name='ingredient-search'),
    path('related-recipe', views.related_recipe, name='related-recipe'),
    path('ingredient', MonthStoreView.as_view() , name='ingredient-page'),
    path('fridge/<int:user_id>', FridgeDetailView.as_view(), name='fridge-detail'),
    path('recipe/update-all-ingredients', RecipeIngredientStoreView.as_view(), name='update-all-recipe-ingredients'),
    path('recipe/store',RecipeStoreView.as_view()),
    path('today-recipe', TodayRecipeView.as_view()),
    path('recipe/update', views.RecipeUpdateView.as_view(), name='recipe-update'),
]