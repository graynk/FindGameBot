import datetime
from typing import List, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from rawg.genre import Genre
from rawg.store_item import StoreItem


@dataclass_json
@dataclass
class GameBrief:
    id: int
    released: Optional[datetime.date]
    tba: bool
    background_image: str
    genres: List[Genre]
    stores: Optional[List[StoreItem]]
