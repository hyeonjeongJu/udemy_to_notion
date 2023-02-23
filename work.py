from extract import get_curriculum, search_courses
from notion import createNotionDB, createNotionRows, getProperties
# shallow copy, deep copy
# 포인터만 넘겨주는 언어와 포인터+값을 넘겨주는 언어
# 파이썬의 경우 포인터만이라 해당 이슈가 발생


# 검색: (title) -> (강좌 id) 
print('검색할 강좌의 이름을 써주세요')
keyword = input(':')

search_courses(keyword)

# 추출: (강좌 id) -> 커리큘럼 목록 및 가공
json_list = get_curriculum(4857034)

# 생성: 노션에 database 페이지 생성 (arr => 섹션 리스트 생성을 위함)
database_id = createNotionDB(parent_id='3be08357f7b64ed0b55b1a6b6e993c16', arr=json_list)

# 확인: 노션에 생성된 database의 properties를 구하기 위함
ids = getProperties(database_id)

# 생성: 위 database에 커리큘럼 rows 생성
createNotionRows(database_id, json_list, ids)

# 정렬은 현재 updated 기준으로만 지원하기에 수작업 필요
