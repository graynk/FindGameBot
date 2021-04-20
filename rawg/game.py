import datetime
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from rawg.platform_item import PlatformItem
from rawg.genre import Genre
from rawg.developer import Developer


@dataclass_json
@dataclass
class Game:
    id: int
    slug: str
    released: Optional[datetime.date]
    tba: bool
    name: str
    name_original: str
    description_raw: str
    alternative_names: List[str]
    platforms: List[PlatformItem]
    genres: List[Genre]
    developers: List[Developer]
