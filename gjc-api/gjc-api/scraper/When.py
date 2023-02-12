from enum import Enum

class When(Enum):
    """Time filters of game jams scraping.
    """
    
    UPCOMING = 'upcoming'
    IN_PROGRESS = 'in-progress'
    ENDED = 'past'