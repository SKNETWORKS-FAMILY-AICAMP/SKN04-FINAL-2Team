from first import First_filter
from second import Second_filter


example_text = '3년차 이상의 백엔드 개발자인데 검색 엔진 구축 경험이 있고, 파이썬, 장고의 기술스택을 가진 사람'

answer, keys = Second_filter(First_filter(example_text))

print(answer, keys)


#career_year 3
#job_category: 백엔드 개발자
#etc: 검색 엔진 구축 경험이 있는 사람
#tech_stack_name: python django spring boot
