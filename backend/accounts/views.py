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
from django.shortcuts import get_object_or_404


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
class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, username):
        # username을 기반으로 사용자 객체를 가져옵니다.
        user = get_object_or_404(CustomUser, username=username)

        # is_staff 필드를 True로 설정합니다.
        user.is_staff = True
        user.save()

        return Response(status=status.HTTP_200_OK)
    
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
    
class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        username = request.data.get('username')
        print(f'username: {username}')
        if not username:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, username=username)
        # 추가적인 권한 검사를 여기에 추가할 수 있습니다.
        # 예: 관리자가 아닌 사용자가 다른 사용자를 삭제할 수 없도록 제한

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GrantRoleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # 관리자 권한 필요

    def patch(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        user.is_staff = True  # 권한 부여
        user.save()
        return Response({"message": "권한이 성공적으로 부여되었습니다."}, status=status.HTTP_200_OK)



class SearchUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        user_data = {
            "username": user.username,
        }
        
        return Response(user_data, status=status.HTTP_200_OK)
