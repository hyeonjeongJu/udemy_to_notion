import os

from notion_client import Client
from notion_client.helpers import get_id
from dotenv import dotenv_values


# notion_client api
config = dotenv_values(".env")
notion = Client(auth=config['NOTION_TOKEN'])

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")

while NOTION_TOKEN == "":
    print("NOTION_TOKEN not found.")
    NOTION_TOKEN = input("Enter your integration token: ").strip()

# Initialize the client
notion = Client(auth=NOTION_TOKEN)


def manual_inputs(parent_id="", db_name="") -> tuple:
    """
    Get values from user input
    """
    if parent_id == "":
        is_page_ok = False
        while not is_page_ok:
            input_text = input("\nEnter the parent page ID or URL: ").strip()
            # Checking if the page exists
            try:
                if input_text[:4] == "http":
                    parent_id = get_id(input_text)
                    print(f"\nThe ID of the target page is: {parent_id}")
                else:
                    parent_id = input_text
                notion.pages.retrieve(parent_id)
                is_page_ok = True
                print("Page found")
            except Exception as e:
                print(e)
                continue
    while db_name == "":
        db_name = input("\n\nName of the database that you want to create: ")

    return (parent_id, db_name)


def create_database(parent_id: str, db_name: str) -> dict:
    """
    parent_id(str): ID of the parent page
    db_name(str): Title of the database
    """
    print(f"\n\nCreate database '{db_name}' in page {parent_id}...")
    properties = {
        # "Description": {"rich_text": {}},
        "섹션": {
            "select": {
                "options": [
                    {"name": "1. 시작하기", "color": "green"},
                    {"name": "2. 기본 구문 및 핵심 기능", "color": "red"},
                    {"name": "3. 조건문 및 루프 작업", "color": "yellow"},
                ]
            }
        },
        "Name": {"title": {}},  # This is a required property
        "id": {"number": {}},
        "완료": {"checkbox": {}},
        "Created time": {"created_time": {}},
        "Last edited time": {"last_edited_time": {}},
        "참고 url": {"url": {}},
        # "Last ordered": {"date": {}},
        # "Photo": {"files": {}},
    }
    title = [{"type": "text", "text": {"content": db_name}}]
    icon = {"type": "emoji", "emoji": "🎉"}
    parent = {"type": "page_id", "page_id": parent_id}
    return notion.databases.create(
        parent=parent, title=title, properties=properties, icon=icon
    )


if __name__ == "__main__":

    parent_id, db_name = manual_inputs()
    newdb = create_database(parent_id=parent_id, db_name=db_name)
    print(f"\n\nDatabase {db_name} created at {newdb['url']}\n")
