from dataclasses import dataclass
from dataclasses_json import dataclass_json

from rawg.store_brief import StoreBrief


@dataclass_json
@dataclass
class StoreItem:
    store: StoreBrief
