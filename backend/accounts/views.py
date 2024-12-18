from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import RegisterSerializer, UserProfileSerializer, UserUpdateSerializer


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