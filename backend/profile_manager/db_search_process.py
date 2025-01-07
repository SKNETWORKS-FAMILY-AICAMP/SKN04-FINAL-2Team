from typing import Dict, Any, List
from .models import Profile, TechStack, Career, AcademicRecord, Certificate, Language

def search_profiles(search_params: Dict[str, Any]) -> List[Profile]:
    queryset = Profile.objects.all()

    if 'job_category' in search_params:
        queryset = queryset.filter(job_category__icontains=search_params['job_category'])
    if 'career_year' in search_params:
        queryset = queryset.filter(career_year=search_params['career_year'])

    # 기술 스택 검색
    if 'tech_stack_name' in search_params:
        queryset = queryset.filter(tech_stacks__tech_stack_name__icontains=search_params['tech_stack_name'])

    # 경력 검색
    if 'company_name' in search_params:
        queryset = queryset.filter(careers__company_name__icontains=search_params['company_name'])
    if 'position' in search_params:
        queryset = queryset.filter(careers__position__icontains=search_params['position'])
    if 'major' in search_params:
        queryset = queryset.filter(academic_records__major__icontains=search_params['major'])

    # 자격증 검색
    if 'certificate_name' in search_params:
        queryset = queryset.filter(certificates__name__icontains=search_params['certificate_name'])

    # 언어 검색
    if 'language_name' in search_params:
        queryset = queryset.filter(languages__language_name__icontains=search_params['language_name'])
    if 'language_level' in search_params:
        queryset = queryset.filter(languages__language_level__icontains=search_params['language_level'])

    return queryset.distinct()