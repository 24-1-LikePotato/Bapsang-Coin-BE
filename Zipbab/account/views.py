from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSubscriptionSerializer

class ActivateSubscriptionView(APIView):
    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSubscriptionSerializer(user, data={'is_subscribe': True}, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '구독이 활성화되었습니다.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)