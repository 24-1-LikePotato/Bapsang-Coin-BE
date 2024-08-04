from rest_framework import serializers
from .models import ChangePriceDay, ChangePriceMonth2
from main.models import Ingredient

class ChangePriceDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceDay
        fields = '__all__'

class ChangePriceMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceMonth2
        fields = '__all__'

class TodayIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name')
    unit = serializers.CharField(source='ingredient.unit')

    class Meta:
        model = ChangePriceDay
        fields = ['ingredient_name', 'unit', 'price', 'updown', 'updown_percent']