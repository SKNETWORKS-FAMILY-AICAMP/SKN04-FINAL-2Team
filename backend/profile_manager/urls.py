from django.urls import path
from . import views

# accounts 앱의 URL 패턴 정의
urlpatterns = [
    path('search/', views.search_profiles, name='search_profiles'),
    # path('search/keywords/', views.search_by_keywords, name='search_by_keywords'),
    # path('resume/<int:id>/', views.resume_detail, name='resume_detail'),
    path('bookmark/add/', views.add_bookmark, name='add_bookmark'),
    path('bookmark/remove/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmark/', views.bookmark_list, name='bookmark_list'),
]
