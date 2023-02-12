from os import getenv
from requests import post as post_r

from models.GameJamModel import GameJamModel

INSERT_URL='https://api.notion.com/v1/pages'

def insert_jam(jam: GameJamModel):
    headers = { 
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer ' + getenv('NOTION_INTEGRATION_ID')
    }
    
    # Buid body
    description = f'{jam.joined} Joined\n'
    description += ('Ranked' if jam.ranked else 'Not ranked') + '\n'
    description += 'Featured' if jam.featured else 'Not featured'
    
    body = {
        'parent': { 'database_id': getenv('NOTION_DATABASE_ID') },
        'icon': {
            'emoji': '🎮'
        },
        'properties': {
            'Name': {
                'title': [
                    {
                        'text': {
                            'content': jam.name
                        }
                    }
                ]
            },
            'Category': {
                'select': {
                    'name': 'Game Jam'
                }
            },
            'Date': {
                'date': {
                    'start': str(jam.start_date),
                    'end': str(jam.end_date)
                }
            },
            'Location': {
                'rich_text': [
                    {
                        'text': {
                            'content': jam.url
                        }
                    }
                ]
            },
            'To note': {
                'rich_text': [
                    {
                        'text': {
                            'content': description
                        }
                    }
                ]
            }
        }
    }
    if jam.bg_image_url is not None:
        print(jam.bg_image_url)
        body['cover'] = {
            'external': {
                'url': jam.bg_image_url
            }
        }
    
    response = post_r(INSERT_URL, headers=headers, json=body)
    if response.status_code != 200:
        raise NotionAPIException(message=response.json()['message'])
    return response.json()['url']

class NotionAPIException(Exception):
    def __init__(self, message: str):
        super().__init__(self, message)