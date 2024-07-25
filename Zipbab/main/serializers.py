from rest_framework import serializers
from .models import Fridge, FridgeIngredient, Ingredient

class FridgeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.SerializerMethodField()
    ingredient_pk = serializers.SerializerMethodField()
    days_until_expiration = serializers.SerializerMethodField()
    is_expiring_soon = serializers.SerializerMethodField()

    class Meta:
        model = FridgeIngredient
        fields = ['id','ingredient_name','ingredient_pk', 'days_until_expiration', 'is_expiring_soon']

    def get_ingredient_name(self, obj):
        return obj.ingredient.name
    
    def get_ingredient_pk(self,obj):
        return obj.ingredient.pk

    def get_days_until_expiration(self, obj):
        return obj.days_until_expiration()

    def get_is_expiring_soon(self, obj):
        return obj.is_expiring_soon()
    
    
class FridgeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Fridge
        fields = ['user', 'ingredients']

    def get_ingredients(self, obj):
        fridge_ingredients = FridgeIngredient.objects.filter(fridge=obj)
        return FridgeIngredientSerializer(fridge_ingredients, many=True).data