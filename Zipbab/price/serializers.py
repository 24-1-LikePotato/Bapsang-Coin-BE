from rest_framework import serializers
from .models import ChangePriceDay, ChangePriceMonth

class ChangePriceDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceDay
        fields = '__all__'

class ChangePriceMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangePriceMonth
        fields = '__all__'