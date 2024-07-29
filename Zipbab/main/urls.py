from django.contrib import admin
from django.urls import path

from .views import FridgeDetailView

urlpatterns = [
<<<<<<< HEAD

    path('fridge/<int:user_id>/', FridgeDetailView.as_view(), name='fridge-detail'),

=======
    path('recipe', views.RecipeStoreView.as_view())
>>>>>>> 81f4679c01046ec76d5a186c37e4732258d83f13
]