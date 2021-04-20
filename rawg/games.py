from typing import List, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from rawg.game_brief import GameBrief


@dataclass_json
@dataclass
class Games:
    results: Optional[List[GameBrief]]
