from fastapi.testclient import TestClient
from requests import get as get_r
from datetime import datetime

from main import app

test_client = TestClient(app)

#! GET JAMS TESTS

def test_get_jams_default():
    response = test_client.get('/jams')
    assert response.status_code == 200
    jams_fetched = response.json()
    assert len(jams_fetched) <= 50
    for jam in jams_fetched:
        assert is_jam_valid(jam)

def test_game_jams_w_count():
    response = test_client.get('/jams?count=20')
    assert response.status_code == 200
    jams_fetched = response.json()
    assert len(jams_fetched) <= 20
    for jam in jams_fetched:
        assert is_jam_valid(jam)

def test_game_jams_w_invalid_count():
    response = test_client.get('/jams?count=201')
    assert response.status_code == 400
    assert response.text == 'Invalid count. You can only fetch between 1 and 200 game jams.'
    
#! SAVE JAM TESTS

def test_save_jam():
    response = test_client.post('/jams', json={
        'name': 'Game Jam',
        'url': 'https://test-link.com',
        'bg_image_url': None,
        'start_date': datetime(2023, 1, 1, 16, 0, 0),
        'end_date': datetime(2023, 1, 3, 7, 10, 20),
        'joined': 27,
        'ranked': True,
        'featured': False
    })
    assert response.status_code == 201
    notion_page_url = response.json()
    assert isinstance(notion_page_url, str)
    assert get_r(notion_page_url).status_code == 200

def is_jam_valid(jam_to_validate):
    return (
        jam_to_validate.name != None and
        jam_to_validate.url != None and
        (
            jam_to_validate.bg_image_url == None or 
            isinstance(jam_to_validate.bg_image_url, str)
        ) and
        jam_to_validate.start_date >= datetime.now() and
        jam_to_validate.end_date >= jam_to_validate.start_date and
        jam_to_validate.joined >= 0 and
        (
            jam_to_validate.ranked is True or
            jam_to_validate.ranked is False
        ) and
        (
            jam_to_validate.featured is True or
            jam_to_validate.featured is False
        )
    )