from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import RegisterSerializer, UserProfileSerializer, UserUpdateSerializer, AdminUserUpdateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': '아이디 또는 비밀번호가 일치하지 않습니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

# 사용자 등록을 위한 API 뷰
class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

# 사용자 프로필 조회를 위한 API 뷰
class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# 사용자 프로필 업데이트를 위한 API 뷰
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class AdminUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # 슈퍼유저 권한 체크

    def get_permissions(self):
        if not self.request.user.is_superuser:
            return Response({
                "message": "권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)
        return super().get_permissions()