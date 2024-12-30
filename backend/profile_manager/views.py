from django.shortcuts import render
from .models import Profile
from .serializers import SimpleProfileSerializer
from django.http import JsonResponse

# Create your views here.
def search_profiles(request):
    query = request.GET.get('query', '')
    # 검색 로직 구현 (미구현)
    
    # 테스트를 위해 임의의 Profile 객체 4개 생성
    results = []
    for i in range(4):  # 4개로 수정
        profile = Profile()
        profile.profile_id = i + 1
        serializer = SimpleProfileSerializer(profile)
        results.append(serializer.data)
    
    return JsonResponse({'results': results})