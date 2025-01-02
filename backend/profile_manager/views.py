from django.shortcuts import render
from .models import Profile, Bookmark
from .serializers import SimpleProfileSerializer, BookmarkedProfileSerializer
from django.http import JsonResponse

# Create your views here.
def search_profiles(request):
    query = request.GET.get('query', '')
    # 검색 로직 구현 (미구현)
    
    profiles_queryset = Profile.objects.all()[:10]  # 실제 DB에서 4개 조회
    serializer = SimpleProfileSerializer(profiles_queryset, many=True)
    return JsonResponse({'results': serializer.data})

def add_bookmark(request):
    profile = Profile.objects.get(id=request.data['profile_id'])
    Bookmark.objects.create(user=request.user, profile=profile, ai_analysis=request.ai_analysis)
    return JsonResponse({'status': 'success'})

def remove_bookmark(request):
    profile = Profile.objects.get(id=request.data['profile_id'])
    Bookmark.objects.filter(user=request.user, profile=profile).delete()
    return JsonResponse({'status': 'success'})

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    serializer = BookmarkedProfileSerializer(bookmarks, many=True)
    return JsonResponse({'bookmarks': serializer.data})



