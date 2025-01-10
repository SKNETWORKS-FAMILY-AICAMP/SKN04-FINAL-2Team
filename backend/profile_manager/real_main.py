from first import First_filter
from second import Second_filter


example_text = '3년차 이상의 백엔드 개발자인데 검색 엔진 구축 경험이 있고, python, django, spring boot의 기술스택을 가진 사람'

answer = First_filter(example_text)
tech_stack, keys = Second_filter(answer)

print(answer, tech_stack, keys)