from typing import List
from .constants import FrameType, AbilityType
from .progress import Ability


class StartAttr:
    abilities: List[Ability]
    frame_attr: FrameType

    def __init__(self, abilities: List[Ability], frame_attr: FrameType) -> None:
        self.abilities = abilities
        self.frame_attr = frame_attr

    def __json__(self):
        return {
            "abilities": [ability.__json__() for ability in self.abilities],
            "frame_attr": self.frame_attr.value,
        }

    def __text__(self) -> str:
        text = ""
        for ability in self.abilities:
            if ability.type == AbilityType.Persistent:
                type_text = "[常]"
            elif ability.type == AbilityType.Automatic:
                type_text = "[自]"
            elif ability.type == AbilityType.Activated:
                type_text = "[起]"
            text += f"{type_text} {ability.effect}\n"
        return text
