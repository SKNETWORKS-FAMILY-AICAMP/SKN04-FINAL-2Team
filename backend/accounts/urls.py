from django.urls import path
from .views import RegisterAPIView, UserProfileAPIView, UserUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView

# accounts 앱의 URL 패턴 정의
urlpatterns = [

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT 갱신
    path('register/', RegisterAPIView.as_view(), name='register'),  # 회원가입
    path('accounts/', UserProfileAPIView.as_view(), name='profile'),  # 사용자 정보 조회
    path('accounts/update/', UserUpdateAPIView.as_view(), name='profile_update'),  # 사용자 정보 수정
    
]