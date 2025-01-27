from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import RegisterSerializer, UserProfileSerializer, UserUpdateSerializer, AdminUserUpdateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenVerifyView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

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

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]  # 인증 불필요

    def post(self, request):
        try:
            refresh = request.data.get('refresh')  # 요청 데이터에서 Refresh Token 가져오기
            if not refresh:
                return Response({"error": "Refresh Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Refresh Token 검증 및 Access Token 재발급
            token = RefreshToken(refresh)
            access_token = str(token.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]  # 인증 불필요

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

