from fastapi import APIRouter, Response, status

from scraper.GameJamsScraper import GameJamsScraper
from scraper.When import When
from models.GameJamModel import GameJamModel

from services.notionapi import insert_jam, NotionAPIException

router: APIRouter = APIRouter(
    prefix='/jams',
    tags=['jams'],
    responses={
        404: {'description': 'Resource not found'}
    }
)

@router.get('/', status_code=status.HTTP_200_OK)
def get_jams(
    response: Response,
    count: int = 50,
    when: When = When.UPCOMING
) -> list[GameJamModel]:
    if count < 1 or count > 200:
        response.status_code = 400
        return 'Invalid count. You can only fetch between 1 and 200 game jams.'
        
    scraper: GameJamsScraper = GameJamsScraper(False)
    return scraper.scrap_jams(count, when)

@router.post('/', status_code=status.HTTP_201_CREATED)
def save_jam(jam: GameJamModel, response: Response):
    try:
        created_page_url = insert_jam(jam)
        return created_page_url
    except NotionAPIException:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "An error occured while trying to save the given game jam in the Notion's calendar. Please try again later."