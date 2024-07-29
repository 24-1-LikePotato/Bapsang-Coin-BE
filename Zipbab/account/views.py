from .models import User
from main.models import Fridge
from .serializers import UserSubscriptionSerializer,UserSerializer

from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import requests


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


BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'account/kakao/callback'
SOCIAL_AUTH_KAKAO_CLIENT_ID ='b3b591e0bea504302e17de1dd109dec2'




def kakao_login(request):
    client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=profile_nickname,profile_image,account_email")



@api_view(['GET'])
def kakao_callback(request):
    rest_api_key = SOCIAL_AUTH_KAKAO_CLIENT_ID
    code = request.GET.get("code")
    kakao_token_uri = "https://kauth.kakao.com/oauth/token"
  
    request_data = {
            'grant_type': 'authorization_code',
            'client_id': rest_api_key,
            'redirect_uri': KAKAO_CALLBACK_URI,
            'code': code,
        }

    token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
    
    # 카카오 토큰 받기
    token_req = requests.post(kakao_token_uri, data=request_data, headers=token_headers)
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise ValueError(error)
    access_token = token_req_json["access_token"]
    
    # 카카오 토큰을 헤더에 넣어 프로필 정보 받기 요청
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer ${access_token}",})
    
    if profile_request.status_code == 200:
        profile_json = profile_request.json()
        error = profile_json.get("error")

        if error is not None:
            raise ValueError(error)
        
        user_nickname = profile_json['kakao_account']["profile"].get("nickname")
        user_email = profile_json["kakao_account"].get("email")
   
    else:
        raise ValueError(profile_request.status_code)
        
    
    # 유저 정보가 있으면 그대로 로그인하기
    try:
        user = User.objects.get(email=user_email)
        
        # 토큰 발급하기
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = JsonResponse(
            {
                "user_id":user.pk,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )

        return res
        #redirect_url = f"{FRONTEND_URL}/login?access={access_token}&refresh={refresh_token}"
        #return HttpResponseRedirect(redirect_url)
    
    # 유저 정보가 없으면 회원가입 후 로그인하기
    except User.DoesNotExist:
        user = User.objects.create_user(email=user_email,nickname=user_nickname)
        user.save()

        # 유저 생성할 때 냉장고 자동으로 생성하기
        fridge, created = Fridge.objects.get_or_create(user=user)
        Fridge.save()

        # 토큰 발급하기
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = JsonResponse(
            {
                "user_id":user.pk,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )

        return res
        # redirect_url = f"{FRONTEND_URL}/login?access={access_token}&refresh={refresh_token}"
        # return HttpResponseRedirect(redirect_url)