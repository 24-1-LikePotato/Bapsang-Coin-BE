from django.contrib import admin
from .models import Fridge, FridgeIngredient, Ingredient, Recipe

admin.site.register(Fridge)
admin.site.register(FridgeIngredient)
admin.site.register(Ingredient)
admin.site.register(Recipe)