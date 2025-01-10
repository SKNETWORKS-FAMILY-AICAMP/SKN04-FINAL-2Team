from django.shortcuts import render
from .models import Profile, Bookmark
from .serializers import SimpleProfileSerializer, BookmarkedProfileSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .search_process import search_process, get_openai_response

# Create your views here.
def search_profiles(request):
    print(f'request.GET.get("query"): {request.GET.get("query")}')
    gpt_response = get_openai_response(request.GET.get('query'))
    search_results, keywords = search_process(gpt_response)
    print(f'search_results: {search_results}')
    serializer = SimpleProfileSerializer(search_results, many=True)
    return JsonResponse({'results': serializer.data, 'keywords': keywords})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bookmark(request):
    try:
        profile = Profile.objects.get(profile_id=request.data['profile_id'])
        # request.user를 통해 현재 인증된 사용자 정보를 가져옴
        ai_analysis = request.data.get('ai_analysis', None)
        Bookmark.objects.create(
            user=request.user, 
            profile=profile,
            ai_analysis=ai_analysis
        )
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    except Profile.DoesNotExist:
        return Response(
            {'error': '프로필을 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])  # POST에서 DELETE로 변경
@permission_classes([IsAuthenticated])
def remove_bookmark(request, profile_id):  # URL 파라미터로 profile_id를 받도록 수정
    try:
        profile = Profile.objects.get(profile_id=profile_id)  # id 대신 profile_id 사용
        bookmark = Bookmark.objects.filter(user=request.user, profile=profile)
        if bookmark.exists():
            bookmark.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response(
            {'error': '북마크를 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Profile.DoesNotExist:
        return Response(
            {'error': '프로필을 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bookmark_list(request):
    try:
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkedProfileSerializer(bookmarks, many=True)
        return Response({
            'success': True,
            'bookmarks': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)