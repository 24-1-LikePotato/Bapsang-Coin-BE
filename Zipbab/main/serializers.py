from rest_framework import serializers
from .models import Fridge, FridgeIngredient, Ingredient
from django.utils import timezone

class FridgeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.SerializerMethodField()
    ingredient_pk = serializers.SerializerMethodField()
    days_until_expiration = serializers.SerializerMethodField()
    is_expiring_soon = serializers.SerializerMethodField()

    class Meta:
        model = FridgeIngredient
        fields = ['ingredient_name','ingredient_pk', 'days_until_expiration', 'is_expiring_soon']

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