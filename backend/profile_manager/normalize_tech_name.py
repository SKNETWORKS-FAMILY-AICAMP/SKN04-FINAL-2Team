from django.db import transaction
from backend.profile_manager.models import TechStack

words_to_remove = ['한글', '애자일', ]

translations = {
        'python': [ '파이썬', ''],
        'AI': ['인공지능(AI)', '인공지능'],
        # 추가적인 변경이 필요할 경우 여기에 추가
    }

def find_key_by_value(dictionary, target_value):
    for key, values in dictionary.items():
        if target_value in values:
            return key
    return None

def normalize_tech_name(name):
    key = find_key_by_value(translations, name)
    return key

def normalize_tech_stacks():
    with transaction.atomic():
        for tech_stack in TechStack.objects.all():
            normalized_name = normalize_tech_name(tech_stack.tech_stack_name)
            if tech_stack.tech_stack_name != normalized_name:
                tech_stack.tech_stack_name = normalized_name
                tech_stack.save()

# 스크립트 실행
normalize_tech_stacks()