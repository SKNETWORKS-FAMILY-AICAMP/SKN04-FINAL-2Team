from django.urls import path
from .views import ( RegisterAPIView, UserProfileAPIView, UserUpdateAPIView, 
                    LogoutView, RefreshTokenView, DeleteUserAPIView, SearchUserAPIView, GrantRoleAPIView
                    )
from rest_framework_simplejwt.views import TokenVerifyView
from .views import CustomTokenObtainPairView, CustomTokenVerifyView

# accounts 앱의 URL 패턴 정의
urlpatterns = [

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),  # JWT 갱신
    path('verify/', CustomTokenVerifyView.as_view(), name='token_verify'),  # JWT 토큰 검증
    path('register/', RegisterAPIView.as_view(), name='register'),  # 회원가입
    path('delete/', DeleteUserAPIView.as_view(), name='delete_user'),  # 회원탈퇴
    path('accounts/', UserProfileAPIView.as_view(), name='profile'),  # 사용자 정보 조회
    path('update/', UserUpdateAPIView.as_view(), name='profile_update'),  # 사용자 정보 수정
    path('grant-role/<str:username>/', GrantRoleAPIView.as_view(), name='grant_role'),  # 사용자 권한 부여
    path('users/<str:username>/', SearchUserAPIView.as_view(),),
    
]