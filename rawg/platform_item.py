from dataclasses import dataclass

from dataclasses_json import dataclass_json

from rawg.platform import Platform


@dataclass_json
@dataclass
class PlatformItem:
    platform: Platform
