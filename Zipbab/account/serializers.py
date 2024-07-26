from rest_framework import serializers
from .models import User

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_subscribe'] 

    def update(self, instance, validated_data):
        instance.is_subscribe = True  
        instance.save()
        return instance