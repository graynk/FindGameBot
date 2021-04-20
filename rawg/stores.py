from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined

from rawg.store import Store


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Stores:
    results: List[Store]
