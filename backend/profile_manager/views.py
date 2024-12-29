from django.shortcuts import render

# Create your views here.
def search_profiles(request):
    query = request.GET.get('query', '')
    # 검색 로직 구현
    results = []  # 검색 결과 리스트
    return JsonResponse({'results': results})