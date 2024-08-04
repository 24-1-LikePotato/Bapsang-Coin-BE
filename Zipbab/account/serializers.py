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
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nickname']  # 필요한 필드를 나열합니다.