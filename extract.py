import requests
import os
from pprint import pprint
from dotenv import dotenv_values
from pyudemy import Udemy


# pyudemy api
config = dotenv_values(".env")
udemy = Udemy(config['UDEMY_CLIENT_ID'], config['UDEMY_CLIENT_SECRET'])

# 특정 강좌 커리큘럼 추출
def get_curriculum(id):
  results = udemy.public_curriculum(id=id, page=1, page_size=500).get('results')

  num = 1
  cnt = 0

  lst = []

  """
  make : obj variable 
  make : {} instance
  assign : {} => obj 
  """
  # instance 를 자꾸 ... 재활용하고있어서 문제
  section_tmp = ''
  for result in results:
    
    obj = {
      "section": "",
      "id": "",
      "name": "",
    } 
      
    # 0x0011
    # 0x0002
    category, title = result['_class'], result['title']

    if category == 'chapter':
      section_tmp = f"섹션{num}. {title}"
      num += 1
    elif category == 'practice':
      obj['id'], obj['name'] = cnt, title
      obj['section'] = section_tmp
      lst.append(obj)
      section_tmp = ''
    elif category == 'lecture':
      cnt += 1
      obj['id'], obj['name'] = cnt, title
      obj['section'] = section_tmp
      lst.append(obj)
      section_tmp = ''
    else:
      print('title, practice, lecture에 해당되는 _class가 아닙니다.')
      
    # pprint(obj)
    # lst.apped = lst = [0x0002, 0x0002]
    
  # pprint(lst) #[196, 196, ..., ...]
  return lst

# 강좌 검색
def search_courses(keyword):
  results = udemy.courses(search=keyword).get('results')
  if results is None:
    print('해당하는 강좌가 없습니다.')
    print('검색할 강좌의 이름을 써주세요.')
    keyword = input(':')
    search_courses(keyword)
  for result in results:
    print(result.get('id'), result.get('title'))