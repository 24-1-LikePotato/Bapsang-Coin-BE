from rest_framework import serializers
from .models import ChangePriceDay, ChangePriceMonth
from main.models import Ingredient

class ChangePriceDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceDay
        fields = '__all__'

class ChangePriceMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceMonth
        fields = '__all__'

class TodayIngredient(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name')

    class Meta:
        model = ChangePriceDay
        fields = ['ingredient_name', 'price', 'updown', 'updown_percent']