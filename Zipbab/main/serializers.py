from rest_framework import serializers
from .models import Fridge, FridgeIngredient, Ingredient
from django.utils import timezone

class FridgeIngredientCreateSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField(max_length=50)
    expiration_date = serializers.DateField()
    def create(self, validated_data):
        ingredient_name = validated_data['ingredient_name']
        expiration_date = validated_data['expiration_date']
        
        # Get or create the ingredient
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        
        # Create the FridgeIngredient
        FridgeIngredient.objects.create(
            fridge=self.context['fridge'],
            ingredient=ingredient,
            expiration_date=expiration_date,
            purchase_date=timezone.now().date()  # Set the current date as purchase_date
        )
        
        # Return validated_data directly, since we are not returning an instance
        return validated_data

    def to_representation(self, instance):
        # Directly use the validated data for representation
        return {
            'ingredient_name': instance['ingredient_name'],
            'expiration_date': instance['expiration_date']
        }