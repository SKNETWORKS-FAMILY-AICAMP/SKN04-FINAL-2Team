from typing import Dict, Any, List
from .models import Profile, TechStack, Career, AcademicRecord, Certificate, Language
from datetime import datetime
from django.db.models import F, Q
from .models import Career, Company
import json

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

def search_profiles(search_params: Dict[str, Any]) -> List[Profile]:
    queryset = Profile.objects.all()
    search_params = json.loads(search_params)
    print("search 진입")
    if 'job_category' in search_params and search_params['job_category'] != "None":
        print(f"Filtering by job_category: {search_params['job_category']}")
        queryset = queryset.filter(job_category__icontains=search_params['job_category'])
    
    if 'career_year' in search_params and search_params['career_year'] != "None" and search_params['career_year'] != '0':
        print(f"Filtering by career_year >= {search_params['career_year']}")
        queryset = queryset.filter(career_year__gte=search_params['career_year'])
    
    if 'tech_stack_name' in search_params and search_params['tech_stack_name'] != "None":
        tech_stacks = search_params['tech_stack_name'].split(', ')
        print(f"Filtering by tech_stack_name: {tech_stacks}")
        for tech_stack in tech_stacks:
            queryset = queryset.filter(tech_stacks__tech_stack_name__icontains=tech_stack)
            print(queryset)
    if 'company_name' in search_params and search_params['company_name'] != "None":
        print(f"Filtering by company_name: {search_params['company_name']}")
        queryset = queryset.filter(careers__company_name__icontains=search_params['company_name'])
        print(queryset)
    if 'position' in search_params and search_params['position'] != "None":
        print(f"Filtering by position: {search_params['position']}")
        queryset = queryset.filter(careers__position__icontains=search_params['position'])
        print(queryset)
    if 'major' in search_params and search_params['major'] != "None":
        print(f"Filtering by major: {search_params['major']}")
        queryset = queryset.filter(academic_records__major__icontains=search_params['major'])
        print(queryset)
    if 'certificate_name' in search_params and search_params['certificate_name'] != "None":
        print(f"Filtering by certificate_name: {search_params['certificate_name']}")
        queryset = queryset.filter(certificates__name__icontains=search_params['certificate_name'])
        print(queryset)

    if 'language_name' in search_params and search_params['language_name'] != "None":
        print(f"Filtering by language_name: {search_params['language_name']}")
        queryset = queryset.filter(languages__language_name__icontains=search_params['language_name'])
        print(queryset)
    if 'language_lank' in search_params and search_params['language_lank'] != "None":
        print(f"Filtering by language_lank: {search_params['language_lank']}")
        queryset = queryset.filter(languages__lank__icontains=search_params['language_lank'])
        print(queryset)
    if 'initial_company_experience' in search_params and search_params['initial_company_experience'] == 'True':
        print(f"Filtering by initial_company_experience: {search_params['initial_company_experience']}")
        early_career_profiles = []
        for profile in queryset:
            try:
                for career in profile.careers.all():
                    if not career.career_start_date:
                        print(f"career_start_date가 None입니다: {career.career_start_date}")
                        continue
                    career_start_date = datetime.strptime(career.career_start_date, "%Y-%m")
                    if not career.company:
                        print(f"Company 객체가 설정되지 않았습니다: {career.company}")
                        continue
                    if not career.company.establishment_date:
                        print(f"establishment_date가 None입니다: {career.company.establishment_date}")
                        continue
                    establishment_date = datetime.strptime(career.company.establishment_date, "%Y-%m")
                    if establishment_date <= career_start_date <= establishment_date.replace(year=establishment_date.year + 2):
                        early_career_profiles.append(profile)
                        break  # 조건을 만족하는 Career가 있으면 다음 프로필로 이동
                    # 현재 재직 중인 경우 설립일로부터 현재까지 2년이 지났는지 확인
                    if career.is_currently_employed:
                        current_date = datetime.now()
                        if establishment_date <= current_date <= establishment_date.replace(year=establishment_date.year + 2):
                            print(f"현재 재직 중인 경력: {career}")
                            early_career_profiles.append(profile)
                            break
            except ValueError as e:
                print(f"날짜 형식 오류: {e}")
                continue
        queryset = queryset.filter(profile_id__in=[profile.profile_id for profile in early_career_profiles])
    
    if 'top_tier_startup' in search_params and search_params['top_tier_startup'] == 'True':
        print(f"Filtering by top_tier_startup: {search_params['top_tier_startup']}")
        company_ids = Company.objects.filter(investment_scale__in=TOP_TIER_LIST).values_list('id', flat=True)
        queryset = queryset.filter(careers__company__id__in=company_ids)
    
    print("search 종료")
    print(queryset)
    return queryset.distinct()