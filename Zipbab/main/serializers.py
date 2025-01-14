from price.models import ChangePriceDay, ChangePriceMonth2
from rest_framework import serializers
from .models import Fridge, FridgeIngredient, Ingredient,Recipe
from django.utils import timezone
from datetime import date

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

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']

class ChangePriceDaySerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = ChangePriceDay
        fields = ['ingredient', 'price', 'updown', 'updown_percent']
 

class ChangePriceMonthSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    
    class Meta:
        model = ChangePriceMonth2
        fields = '__all__'

class FridgeIngredientCreateSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField(max_length=50)
    expiration_date = serializers.DateField()

    def create(self, validated_data):
        ingredient_name = validated_data['ingredient_name']
        expiration_date = validated_data['expiration_date']
        
        # Get the ingredient with the smallest id if it exists, else create a new one
        ingredient = Ingredient.objects.filter(name=ingredient_name).order_by('id').first()
        if not ingredient:
            ingredient = Ingredient.objects.create(name=ingredient_name)
        
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
        # Calculate days until expiration
        expiration_date = instance['expiration_date']
        current_date = date.today()
        days_left = (expiration_date - current_date).days

        # Directly use the validated data for representation with days left
        return {
            'ingredient_name': instance['ingredient_name'],
            'days_left': days_left
        }

      
class TodayRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'image']


