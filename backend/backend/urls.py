from django.urls import path, include
from django.contrib import admin

# 프로젝트의 URL 패턴 정의
urlpatterns = [
    path('auth/', include('accounts.urls')),  # accounts 앱의 URL 포함
    path('profile/', include('profile_manager.urls')),  # profile_manager 앱의 URL 포함
    path('admin/', admin.site.urls), 
]