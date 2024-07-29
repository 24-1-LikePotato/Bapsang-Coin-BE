from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
   path('related_recipe/', views.related_recipe, name='related-recipe')

]