from django.contrib import admin
from .models import Fridge, FridgeIngredient, Ingredient, Recipe, RecipeIngredient

admin.site.register(Fridge)
admin.site.register(FridgeIngredient)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)