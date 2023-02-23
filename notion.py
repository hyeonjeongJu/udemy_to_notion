from notion_client import Client
from dotenv import dotenv_values


# notion_client api
config = dotenv_values(".env")
notion = Client(auth=config['NOTION_TOKEN'])

def makeSelectOptions(value_list):
  str_list = []
  for value in value_list:
    str_list.append({"name": f"{value}"})
  return str_list

# print(makeSelectOptions(['1. hi', '2. hello']))


def createNotionDB(parent_id, arr):
  """
    section = "넘버링. 섹션이름"
    id = "강의 넘버링"
    Name = "강의 이름"
    Status = "Not started 고정"
    Created_time = "now()"
    Last_edited_time = "now()"
    참고_url = "빈값"
  """
  select_list = []

  for item in arr:
    if item['section'] != '':
      select_list.append({"name": item['section'].replace(',', '')})

  title=[{
    'type': 'text',
    'text': {
      'content': '테스트 페이지'
    }
  }]
  properties = {
    "Name": {"title": {}},  # This is a required property
    "Section": {
      "select": {
        "options": select_list,
      }
    },
    "Status": {
      "select": {
        "options": [
          {"name": "Not started", "color": "gray"},
          {"name": "In progress", "color": "blue"},
          {"name": "Done", "color": "green"},
        ],
      }
    },
    "ID": {
      "number": {
        "format": "number"
      }
    },
    "CREATED": {"created_time": {}},
    "UPDATED": {"last_edited_time": {}},
    "참고 URL": {"url": {}},
  }
  database = notion.databases.create(
    parent={'type': 'page_id', 'page_id': parent_id}, title=title, properties=properties#, icon=icon
  )
  print(f"생성된 데이터 베이스 아이디: {database['id']}")
  return database['id']



def createNotionRows(database_id, json_list, ids):
  index=0
  for obj in json_list:
    if obj['section'] == '':
      createNotionRow(database_id, obj, ids['status_id'], None)
    else:
      createNotionRow(database_id, obj, ids['status_id'], ids['section_id_list'][index]['id'])
      index += 1

def createNotionRow(database_id, obj, status_id, section_id):
  section = ''
  if section_id == None:
    section = {}
  else:
    section = {
      "Section": {
        "select": {
          "id": section_id
          }
        }
      }
          
  notion.pages.create(
  **{
      "parent": {
        "database_id": database_id,
      },
      
      "properties": { 
          "Name": { 
            "title": [ 
              { 
                "text": { 
                  "content": obj['name']
                },
              }
            ]
          },
          "Status": {
            "select": {
              "id": status_id,
            }
          },
          **section,
          "ID": { 
            "number": obj['id']
          },
        } 
    }
  )

def getNotion():
  print(result := notion.databases.query(
    **{
      "database_id": "697259c551cd40b6ba233ff906d370ad"
    }
  ))

def getProperties(database_id):
  res = notion.databases.retrieve(database_id=database_id)
  return {'status_id': res['properties']['Status']['select']['options'][0]['id'], 'section_id_list': res['properties']['Section']['select']['options']}
