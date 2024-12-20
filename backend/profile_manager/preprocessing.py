from openai import OpenAI
from tqdm import tqdm
from crawling import resume


modification_resume = []
for i in resume:
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': '''너는 관련된 내용을 아래 틀에 맞춰 바꿔주는 봇이야
                {
                    "profile": {
                        "name": "",
                        "job": "",
                        "email": "",
                        "phone": "",
                        "address": "",
                        "birth_date": ""
                    },
                    "profile_detail": {
                        "brief_introduction": "",
                        "introduction": ""
                    },
                    "skills": [
                        {"name": ""}
                    ],
                    "careers": [
                        {
                            "company_name": "",
                            "position": "",
                            "start_date": "",
                            "end_date": "",
                            "employment_type": "",
                            "responsibilities": "",
                            "description": ""
                        }
                    ],
                    "activities": [
                        {
                            "activity_name": "",
                            "organization_name": "",
                            "description": "",
                            "activity_year": ""
                        }
                    ],
                    "academic_backgrounds": [
                        {
                            "school_name": "",
                            "major": "",
                            "status": "",
                            "start_date": "",
                            "end_date": ""
                        }
                    ],
                    "participated_projects": [
                        {
                            "project_name": "",
                            "project_role": "",
                            "organization_name": "",
                            "start_date": "",
                            "end_date": ""
                        }
                    ],
                    "certificates": [
                        {
                            "name": "",
                            "acquisition_date": "",
                            "issuing_org": ""
                        }
                    ],
                    "education_contents": [
                        {
                            "education_name": "",
                            "description": ""
                        }
                    ],
                    "urls": [
                        {
                            "link": ""
                        }
                    ],
                    "languages": [
                        {
                            "description": ""
                        }
                    ]
                }
                사용자 입력 데이터를 위 틀에 맞춰서 바꿔줘 단 틀에 대응되는 값이 없을경우 key는 남겨두고 value에는 None값을 넣어줘
                '''
            },
            {
                'role': 'user',
                'content': i
            }
        ]
    )
    modification_resume.append(completion.choices[0].message.content)