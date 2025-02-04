from django.shortcuts import render
from .models import Profile, Bookmark, ProfileData
from .serializers import SimpleProfileSerializer, BookmarkedProfileSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .search_process import search_process, get_openai_response
from .utils import process_company_information, candidate_validation

from django.http import JsonResponse
from .models import Profile, ProfileData
from .serializers import SimpleProfileSerializer
from .search_process import search_process, get_openai_response
from .utils import process_company_information, candidate_validation  # ⬅️ utils에서 가져오기

def search_profiles(request):
    query = request.GET.get('query')
    gpt_response = get_openai_response(query)
    search_results, keywords = search_process(gpt_response) if isinstance(search_process(gpt_response), tuple) else (search_process(gpt_response), [])

    if len(search_results) > 15:
        print("🔹 검색된 이력서가 15개 이상이므로 AI 분석을 생략합니다.")
        for profile in search_results:
            profile_data, _ = ProfileData.objects.get_or_create(profile=profile)
            profile_data.ai_analysis = None 
            profile_data.save()

        serializer = SimpleProfileSerializer(search_results, many=True)
        return JsonResponse({'results': serializer.data, 'keywords': keywords, 'ai_analysis_skipped': True})
    
    updated_profiles = []
    for i in search_results:
        profile = Profile.objects.get(profile_id=i.profile_id)
        profile_data, _ = ProfileData.objects.get_or_create(profile=profile)

        processed_data = "{}"
        if profile_data.processed_data:
            try:
                processed_data = process_company_information(profile_data.processed_data)
            except Exception as e:
                print(f"S3 데이터 로드 실패: {str(e)}")

        try:
            ai_result = candidate_validation(query, processed_data)
            profile_data.ai_analysis = ai_result
            profile_data.save()
        except Exception as e:
            print(f"AI 분석 오류: {str(e)}")

        updated_profiles.append(profile)

    serializer = SimpleProfileSerializer(updated_profiles, many=True)
    return JsonResponse({'results': serializer.data, 'keywords': keywords, 'ai_analysis_skipped': True})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bookmark(request):
    try:
        profile = Profile.objects.get(profile_id=request.data['profile_id'])
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_bookmark(request, profile_id): 
    try:
        profile = Profile.objects.get(profile_id=profile_id) 
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