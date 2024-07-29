from .models import Ingredient,Recipe
from price.models import ChangePriceDay, ChangePriceMonth
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']

class ChangePriceDaySerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = ChangePriceDay
        fields = ['ingredient', 'price', 'updown_percent']
 
class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    
    class Meta:
        model = Recipe
        fields = ['ingredient','name','content','ingredient_list','image','calorie','carb','protein','fat','natrium']

class ChangePriceMonthSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    
    class Meta:
        fields = ['ingredient','forty','thirty','twenty','ten','today']
