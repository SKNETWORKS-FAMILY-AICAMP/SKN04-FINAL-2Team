from django.urls import path
from .views import RegisterAPIView, UserProfileAPIView, UserUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# accounts 앱의 URL 패턴 정의
urlpatterns = [
]