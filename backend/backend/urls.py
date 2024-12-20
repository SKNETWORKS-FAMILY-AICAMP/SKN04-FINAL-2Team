from django.urls import path, include

# 프로젝트의 URL 패턴 정의
urlpatterns = [
    path('auth/', include('accounts.urls')),  # accounts 앱의 URL 포함
]