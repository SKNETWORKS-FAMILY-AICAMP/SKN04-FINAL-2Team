from typing import Dict, Any, List
from .models import Profile, ProfileData, TechStack, Career, AcademicRecord, Certificate, Language, Company
from datetime import datetime
from django.db.models import F, Q
import json
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
import os          
from collections import defaultdict       
from .utils import process_company_information, candidate_validation                                                           


TOP_TIER_LIST = ["Series C","Series D","Series E","Series F","Series G","Pre-IPO","Post-IPO","IPO"]
def find_early_career_profiles(profiles):
    # 모든 Career와 Company를 가져와서 비교
    early_career_profiles = []

    for profile in profiles:
        try:
            # career_start_date가 None인지 확인
            if not profile.careers.career_start_date:
                print(f"career_start_date가 None입니다: {profile.careers.career_start_date}")
                continue
            # Career의 시작일을 datetime 객체로 변환
            career_start_date = datetime.strptime(profile.careers.career_start_date, "%Y-%m")
            # company 필드를 통해 Company 객체 가져오기
            if not profile.careers.company:
                print(f"Company 객체가 설정되지 않았습니다: {profile.careers.company}")
                continue


            # establishment_date가 None인지 확인
            if not profile.careers.company.establishment_date:
                print(f"establishment_date가 None입니다: {profile.careers.company.establishment_date}")
                continue

            # Company의 설립일을 datetime 객체로 변환
            establishment_date = datetime.strptime(profile.careers.company.establishment_date, "%Y-%m")

            # Career 시작일이 설립일로부터 1년 이내인지 확인
            if establishment_date <= career_start_date <= establishment_date.replace(year=establishment_date.year + 2):
                early_career_profiles.append(profile)

            # 현재 재직 중인 경우를 고려
            if profile.careers.is_currently_employed or not profile.careers.career_end_date:
                print(f"현재 재직 중인 경력: {profile.careers}")
                early_career_profiles.append(profile)

        except ValueError as e:
            print(f"날짜 형식 오류: {e}")
            continue

    return early_career_profiles

def vectordb_filter(etc):
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'save'))
    db = FAISS.load_local(
        folder_path=folder_path,
        index_name='faiss_etc_data_index',
        embeddings=OpenAIEmbeddings(model='text-embedding-3-small'),
        allow_dangerous_deserialization=True,
    )
    result_list = []
    a = db.similarity_search(etc, k=5)
    for page_contents in a:
        print(f"|{page_contents.metadata['key']}: {page_contents.page_content}")
        result_list.append(page_contents.metadata['key'])
    return result_list

def str_to_int_safe(value):
    try:
        return int(value)
    except ValueError:
        return None  # 변환 실패 시 기본값 반환

def search_profiles(search_params: Dict[str, Any]) -> List[Profile]:
    queryset = Profile.objects.all()
    search_params = json.loads(search_params)
    category_list = []
    filter_count = 0  # 적용된 필터 개수
    profile_scores = defaultdict(int)  # 각 Profile의 매칭 점수 저장
    
    def apply_filter(queryset, condition, filter_func, category=None):
        """
        필터를 적용하고, 적용된 경우 filter_count 증가 및 프로필별 점수 증가.
        """
        nonlocal filter_count
        if condition:
            print(f"Filtering by {category}: {condition}")
            filtered_queryset = filter_func(queryset).distinct()
            filter_count += 1
            for profile in filtered_queryset:
                profile_scores[profile.profile_id] += 1
            if category:
                category_list.append(category)
    
    apply_filter(queryset, search_params.get('job_category') not in [None, "None"],
                 lambda x: x.filter(job_category__icontains=search_params.get('job_category')), search_params.get('job_category'))
    
    if search_params.get('career_year') not in [None, "None"]:
        num = str_to_int_safe(search_params.get('career_year'))
        if num > 0:
            apply_filter(queryset, num > 0,
                        lambda x: x.filter(career_year__gte=num), f"{search_params.get('career_year')}년차 이상")
        else:
            apply_filter(queryset, num == 0,
                        lambda x: x.filter(career_year__gte=num), f"{search_params.get('career_year')}년차 이상")
    if 'tech_stack_name' in search_params and search_params['tech_stack_name'] != "None":
        tech_stacks = search_params['tech_stack_name']
        if not isinstance(tech_stacks, list):
            tech_stacks = [tech_stacks]
        for tech_stack in tech_stacks:
            if tech_stack != "None":
                apply_filter(queryset, tech_stack, lambda x: x.filter(tech_stacks__tech_stack_name__iexact=tech_stack), tech_stack)
    
    apply_filter(queryset, search_params.get('major') not in [None, "None"],
                 lambda x: x.filter(academic_records__major__icontains=search_params.get('major')), search_params.get('major'))
    
    apply_filter(queryset, search_params.get('language_name') not in [None, "None"],
                 lambda x: x.filter(languages__language_name__icontains=search_params.get('language_name')), search_params.get('language_name'))
    
    apply_filter(queryset, search_params.get('language_rank') not in [None, "None"],
                 lambda x: x.filter(languages__lank__icontains=search_params.get('language_rank')), f"{search_params.get('language_rank')} 수준")
    
    if 'etc' in search_params and search_params['etc'] != "None":
        etc_result = vectordb_filter(search_params['etc'])
        apply_filter(queryset, search_params['etc'], lambda x: x.filter(profile_id__in=etc_result), search_params['etc'])
    
    apply_filter(queryset, search_params.get('initial_company_experience') == 'True',
                 lambda x: x.filter(profile_id__in=[
                     profile.profile_id for profile in queryset if any(
                         career.career_start_date and career.company and career.company.establishment_date and
                         datetime.strptime(career.company.establishment_date, "%Y-%m") <= datetime.strptime(career.career_start_date, "%Y-%m") <= datetime.strptime(career.company.establishment_date, "%Y-%m").replace(year=datetime.strptime(career.company.establishment_date, "%Y-%m").year + 2)
                         for career in profile.careers.all() if career.career_start_date and career.company and career.company.establishment_date
                     )
                 ]), "초기 회사 경험 있음")
    
    apply_filter(queryset, search_params.get('top_tier_startup') == 'True',
                 lambda x: x.filter(careers__company_name__in=Company.objects.filter(investment_scale__in=TOP_TIER_LIST).values_list('company_name', flat=True)), "탑티어 스타트업 경험 있음")
    
    apply_filter(queryset, search_params.get('conglomerate') == 'True',
                 lambda x: x.filter(careers__company_name__in=Company.objects.filter(is_major_company=True).values_list('company_name', flat=True)), "대기업 경험 있음")
    
    threshold = int(filter_count * 0.9)  # 90% 기준값
    
    filtered_profiles = [profile for profile in queryset if profile_scores[profile.profile_id] >= threshold]

    if len(filtered_profiles) > 15:
            print("🔹 검색된 이력서가 15개 이상이므로 AI 분석을 생략합니다.")
            return Profile.objects.filter(profile_id__in=[p.profile_id for p in filtered_profiles]).distinct(), category_list, True  # AI 분석 생략 여부 반환

    # 🔹 15개 이하일 경우 AI 분석 실행
    updated_profiles = []
    for profile in filtered_profiles:
        profile_data, _ = ProfileData.objects.get_or_create(profile=profile)

        # 🔹 S3에서 데이터 가져오기 (예외 처리 추가)
        processed_data = "{}"
        if profile_data.processed_data:
            try:
                processed_data = process_company_information(profile_data.processed_data)
            except Exception as e:
                print(f"⚠️ S3 데이터 로드 실패: {str(e)}")

        # 🔹 AI 분석 실행 및 저장 (예외 처리 추가)
        try:
            ai_result = candidate_validation(search_params, processed_data)
            profile_data.ai_analysis = ai_result
            profile_data.save()
        except Exception as e:
            print(f"⚠️ AI 분석 오류: {str(e)}")

        updated_profiles.append(profile)

    print("🔹 AI 분석을 완료했습니다.")
    return Profile.objects.filter(profile_id__in=[p.profile_id for p in filtered_profiles]).distinct(), category_list




# def search_profiles(search_params: Dict[str, Any]) -> List[Profile]:
#     queryset = Profile.objects.all()
#     search_params = json.loads(search_params)
#     category_list = []
#     filter_count = 0  # 적용된 필터 개수
#     profile_scores = defaultdict(int)  # 각 Profile의 매칭 점수 저장
    
#     def apply_filter(queryset, condition, filter_func, category=None):
#         """
#         필터를 적용하고, 적용된 경우 filter_count 증가 및 프로필별 점수 증가.
#         """
#         total_profiles = list(queryset)  # 원본 queryset 저장
        
#         nonlocal filter_count
#         if condition:
#             print(f"Filtering by {category}: {condition}")
#             filtered_queryset = filter_func(queryset)
#             print(filtered_queryset.filter(name__icontains="김근형"))
#             print(filtered_queryset.filter(name__icontains="박기웅"))
#             print(filtered_queryset.filter(name__icontains="강민서"))
#             filter_count += 1
#             for profile in filtered_queryset:
#                 profile_scores[profile.profile_id] += 1
                
#             if category:
#                 category_list.append(category)
    
#     apply_filter(queryset, search_params.get('job_category') not in [None, "None"],
#                  lambda x: x.filter(job_category__icontains=search_params.get('job_category')), search_params.get('job_category'))
    
#     if search_params.get('career_year') not in [None, "None"]:
#         num = str_to_int_safe(search_params.get('career_year'))
#         if num > 0:
#             apply_filter(queryset, num > 0,
#                     lambda x: x.filter(career_year__gte=num), f"{search_params.get('career_year')}년차 이상")
#         else:
#             apply_filter(queryset, num == 0,
#                     lambda x: x.filter(career_year__gte=num), f"{search_params.get('career_year')}년차 이상")
#     if 'tech_stack_name' in search_params and search_params['tech_stack_name'] != "None":
#         tech_stacks = search_params['tech_stack_name']
#         if not isinstance(tech_stacks, list):
#             tech_stacks = [tech_stacks]
#         for tech_stack in tech_stacks:
#             if tech_stack != "None":
#                 apply_filter(queryset, tech_stack, lambda x: x.filter(tech_stacks__tech_stack_name__iexact=tech_stack), tech_stack)
    
#     apply_filter(queryset, search_params.get('major') not in [None, "None"],
#                  lambda x: x.filter(academic_records__major__icontains=search_params.get('major')), search_params.get('major'))
    
#     apply_filter(queryset, search_params.get('language_name') not in [None, "None"],
#                  lambda x: x.filter(languages__language_name__icontains=search_params.get('language_name')), search_params.get('language_name'))
    
#     apply_filter(queryset, search_params.get('language_rank') not in [None, "None"],
#                  lambda x: x.filter(languages__lank__icontains=search_params.get('language_rank')), f"{search_params.get('language_rank')} 수준")
    
#     if 'etc' in search_params and search_params['etc'] != "None":
#         etc_result = vectordb_filter(search_params['etc'])
#         apply_filter(queryset, search_params['etc'], lambda x: x.filter(profile_id__in=etc_result), search_params['etc'])
    
#     # 70% 이상 매칭된 Profile 필터링
#     threshold = int(filter_count * 0.8)  # 70% 기준값
    
#     filtered_profiles = [profile for profile in queryset if profile_scores[profile.profile_id] >= threshold]
#     # print(len(filtered_profiles))
#     print(filter_count)
#     for i in filtered_profiles:
#         print(i.profile_id)
#         print(profile_scores[i.profile_id])
    
#     print("search 종료")
#     return Profile.objects.filter(profile_id__in=[p.profile_id for p in filtered_profiles]).distinct(), category_list

# def search_profiles(search_params: Dict[str, Any]) -> List[Profile]:
#     queryset = Profile.objects.all()
#     search_params = json.loads(search_params)
#     category_list = []
#     filter_count = 0  # 적용된 필터 개수
#     profile_scores = defaultdict(int)  # 각 Profile의 매칭 점수 저장
    
#     total_profiles = list(queryset)  # 원본 queryset 저장
    
#     def apply_filter(queryset, condition, filter_func, category=None):
#         """
#         필터를 적용하고, 적용된 경우 filter_count 증가 및 프로필별 점수 증가.
#         """
#         nonlocal filter_count
#         if condition:
#             print(f"Filtering by {category}: {condition}")
#             filtered_queryset = filter_func(queryset, condition)
#             filter_count += 1
#             for profile in filtered_queryset:
#                 profile_scores[profile.profile_id] += 1
#             if category:
#                 category_list.append(category)
    
#     apply_filter(total_profiles, search_params.get('job_category') not in [None, "None"],
#                  lambda qs, v: [p for p in qs if v in p.job_category], search_params.get('job_category'))
    
#     apply_filter(total_profiles, search_params.get('career_year') not in [None, "None", '0'],
#                  lambda qs, v: [p for p in qs if p.career_year >= int(v)], f"{search_params.get('career_year')}년차 이상")
    
#     if 'tech_stack_name' in search_params and search_params['tech_stack_name'] != "None":
#         tech_stacks = search_params['tech_stack_name']
#         if not isinstance(tech_stacks, list):
#             tech_stacks = [tech_stacks]
#         for tech_stack in tech_stacks:
#             if tech_stack != "None":
#                 apply_filter(total_profiles, tech_stack, lambda qs, v: [p for p in qs if any(v in ts for ts in p.tech_stacks)], tech_stack)
    
#     apply_filter(total_profiles, search_params.get('major') not in [None, "None"],
#                  lambda qs, v: [p for p in qs if v in p.major], search_params.get('major'))
    
#     apply_filter(total_profiles, search_params.get('language_name') not in [None, "None"],
#                  lambda qs, v: [p for p in qs if v in p.language_name], search_params.get('language_name'))
    
#     apply_filter(total_profiles, search_params.get('language_lank') not in [None, "None"],
#                  lambda qs, v: [p for p in qs if v in p.language_lank], f"{search_params.get('language_lank')} 수준")
    
#     if 'etc' in search_params and search_params['etc'] != "None":
#         etc_result = vectordb_filter(search_params['etc'])
#         apply_filter(total_profiles, search_params['etc'], lambda qs, v: [p for p in qs if p.profile_id in etc_result], search_params['etc'])
    
#     # 70% 이상 매칭된 Profile 필터링
#     threshold = int(filter_count * 1.0)  # 70% 기준값으로 수정
    
#     filtered_profiles = [profile for profile in total_profiles if profile_scores[profile.profile_id] >= threshold]
    
#     print("search 종료")
#     return Profile.objects.filter(profile_id__in=[p.profile_id for p in filtered_profiles]).distinct(), category_list

    # queryset = Profile.objects.all()
    # search_params = json.loads(search_params)
    # category_list = []
    # score_dict = defaultdict(int)  # 프로필 별 매칭 점수 저장
    # total_weight = 0  # 전체 가중치 합

    # print("search 진입")
    
    # # 필터링 기준별 가중치 설정 (총 10점 만점)
    # weight_dict = {
    #     'job_category': 1.5,
    #     'career_year': 1.5,
    #     'tech_stack_name': 1.5,
    #     'company_name': 1,
    #     'position': 1,
    #     'major': 0.5,
    #     'certificate_name': 0.5,
    #     'language_name': 0.5,
    #     'language_lank': 0.5,
    #     'initial_company_experience': 0.5,
    #     'top_tier_startup': 0.5,
    #     'conglomerate': 0.5,
    # }
    
    # for key, weight in weight_dict.items():
    #     if key in search_params and search_params[key] != "None":
    #         total_weight += weight  # 가중치 총합 업데이트

    # # 직업 카테고리 필터
    # if 'job_category' in search_params and search_params['job_category'] != "None":
    #     print(f"Filtering by job_category: {search_params['job_category']}")
    #     category_list.append(search_params['job_category'])
    #     for profile in queryset:
    #         if search_params['job_category'] in profile.job_category:
    #             score_dict[profile.profile_id] += weight_dict['job_category']

    # # 경력 연수 필터
    # if 'career_year' in search_params and search_params['career_year'] != "None" and search_params['career_year'] != '0':
    #     print(f"Filtering by career_year >= {search_params['career_year']}")
    #     category_list.append(search_params['career_year'] + "년차 이상")
    #     for profile in queryset:
    #         if profile.career_year and profile.career_year >= int(search_params['career_year']):
    #             score_dict[profile.profile_id] += weight_dict['career_year']

    # # 기술 스택 필터
    # if 'tech_stack_name' in search_params and search_params['tech_stack_name'] != "None":
    #     tech_stacks = search_params['tech_stack_name']
    #     print(f"Filtering by tech_stack_name: {tech_stacks}")
    #     if not isinstance(tech_stacks, list):
    #         tech_stacks = [tech_stacks]  # 단일 값이면 리스트로 변환

    #     for tech_stack in tech_stacks:
    #         category_list.append(tech_stack)
    #         for profile in queryset:
    #             if any(tech_stack in skill.tech_stack_name for skill in profile.tech_stacks.all()):
    #                 score_dict[profile.profile_id] += weight_dict['tech_stack_name']

    # # 회사명 필터
    # if 'company_name' in search_params and search_params['company_name'] != "None":
    #     print(f"Filtering by company_name: {search_params['company_name']}")
    #     category_list.append(search_params['company_name'])
    #     for profile in queryset:
    #         if any(search_params['company_name'] in career.company_name for career in profile.careers.all()):
    #             score_dict[profile.profile_id] += weight_dict['company_name']

    # # 직위 필터
    # if 'position' in search_params and search_params['position'] != "None":
    #     print(f"Filtering by position: {search_params['position']}")
    #     for profile in queryset:
    #         if any(search_params['position'] in career.position for career in profile.careers.all()):
    #             score_dict[profile.profile_id] += weight_dict['position']

    # # 전공 필터
    # if 'major' in search_params and search_params['major'] != "None":
    #     print(f"Filtering by major: {search_params['major']}")
    #     for profile in queryset:
    #         if any(search_params['major'] in record.major for record in profile.academic_records.all()):
    #             score_dict[profile.profile_id] += weight_dict['major']

    # # 자격증 필터
    # if 'certificate_name' in search_params and search_params['certificate_name'] != "None":
    #     print(f"Filtering by certificate_name: {search_params['certificate_name']}")
    #     for profile in queryset:
    #         if any(search_params['certificate_name'] in cert.certificate_name for cert in profile.certificates.all()):
    #             score_dict[profile.profile_id] += weight_dict['certificate_name']

    # # 외국어 필터
    # if 'language_name' in search_params and search_params['language_name'] != "None":
    #     print(f"Filtering by language_name: {search_params['language_name']}")
    #     category_list.append(search_params['language_name'])
    #     for profile in queryset:
    #         if any(search_params['language_name'] in lang.language_name for lang in profile.languages.all()):
    #             score_dict[profile.profile_id] += weight_dict['language_name']

    # if 'language_lank' in search_params and search_params['language_lank'] != "None":
    #     print(f"Filtering by language_lank: {search_params['language_lank']}")
    #     category_list.append(search_params['language_lank'] + " 수준")
    #     for profile in queryset:
    #         if any(search_params['language_lank'] in lang.lank for lang in profile.languages.all()):
    #             score_dict[profile.profile_id] += weight_dict['language_lank']
                
    # if 'initial_company_experience' in search_params and search_params['initial_company_experience'] == 'True':
    #     print(f"Filtering by initial_company_experience: {search_params['initial_company_experience']}")
    #     category_list.append("초기 회사 경험 있음")
    #     for profile in queryset:
    #         try:
    #             for career in profile.careers.all():
    #                 if not career.career_start_date or not career.company or not career.company.establishment_date:
    #                     continue
                    
    #                 career_start_date = datetime.strptime(career.career_start_date, "%Y-%m")
    #                 establishment_date = datetime.strptime(career.company.establishment_date, "%Y-%m")

    #                 # 설립 후 2년 이내 입사한 경우
    #                 if establishment_date <= career_start_date <= establishment_date.replace(year=establishment_date.year + 2):
    #                     score_dict[profile.profile_id] += weight_dict['initial_company_experience']
    #                     break  # 조건 충족 시 다음 프로필로 이동
    #         except ValueError as e:
    #             print(f"날짜 형식 오류: {e}")
    #             continue
    
    #     # 탑티어 스타트업 필터 추가
    # if 'top_tier_startup' in search_params and search_params['top_tier_startup'] == 'True':
    #     print(f"Filtering by top_tier_startup: {search_params['top_tier_startup']}")
    #     category_list.append("탑티어 스타트업 경험 있음")
    #     top_tier_company_ids = Company.objects.filter(investment_scale__in=TOP_TIER_LIST).values_list('id', flat=True)
    #     for profile in queryset:
    #         if any(career.company_id in top_tier_company_ids for career in profile.careers.all()):
    #             score_dict[profile.profile_id] += weight_dict['top_tier_startup']

    # # 대기업 경험 필터 추가
    # if 'conglomerate' in search_params and search_params['conglomerate'] == 'True':
    #     print(f"Filtering by conglomerate: {search_params['conglomerate']}")
    #     category_list.append("대기업 경험 있음")
    #     major_company_ids = Company.objects.filter(is_major_company=True).values_list('id', flat=True)
    #     for profile in queryset:
    #         if any(career.company_id in major_company_ids for career in profile.careers.all()):
    #             score_dict[profile.profile_id] += weight_dict['conglomerate']
    # # 70% 이상 매칭된 후보 필터링
    # threshold = total_weight * 0.7  # 70% 이상 매칭 기준
    
    # filtered_profile_ids = [profile.profile_id for profile in queryset if score_dict[profile.profile_id] >= threshold]
    # print(threshold)
    # # QuerySet을 사용하여 필터링
    # filtered_profiles = Profile.objects.filter(profile_id__in=filtered_profile_ids)

    # print("search 종료")
    # return filtered_profiles, category_list