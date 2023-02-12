from pydantic import BaseModel
from datetime import datetime

class GameJamModel(BaseModel):
    """Game Jam data model
    """
    
    name: str
    url: str
    bg_image_url: str | None
    start_date: datetime | None
    end_date: datetime | None
    joined: int
    ranked: bool
    featured: bool