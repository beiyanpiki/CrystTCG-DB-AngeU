from typing import List, Optional

from .collection import CollectionAttr
from .start import StartAttr
from .action import ActionAttr
from .progress import ProgressAttr
from .constants import AbilityType, CardColor, CardType, FrameType


class Ability:
    type: AbilityType
    effect: str
    effect_tran: str

    def __init__(self, type: AbilityType, effect: str, effect_tran: str) -> None:
        self.type = type
        self.effect = effect
        self.effect_tran = effect_tran

    def __json__(self):
        return {
            "type": self.type.value,
            "effect": self.effect,
            "effect_tran": self.effect_tran,
        }


class Card:
    name: str
    name_tran: str
    type: CardType
    level: int
    color: Optional[CardColor]
    # Will automatic generate
    text: str

    abilities: List[Ability]

    progress_attr: Optional[ProgressAttr]
    action_attr: Optional[ActionAttr]
    frame_attr: Optional[FrameType]

    atk_value: Optional[int]
    def_value: Optional[int]
    stk_value: Optional[int]

    flavor_text: Optional[str]
    flavor_text_tran: Optional[str]

    collection_attr: CollectionAttr

    def __init__(
        self,
        name: str,
        name_tran: str,
        type: CardType,
        level: int,
        color: Optional[CardColor],
        abilities: List[Ability],
        progress_attr: Optional[ProgressAttr],
        action_attr: Optional[ActionAttr],
        frame_attr: Optional[FrameType],
        atk_value: Optional[int],
        def_value: Optional[int],
        stk_value: Optional[int],
        flavor_text: Optional[str],
        flavor_text_tran: Optional[str],
        collection_attr: CollectionAttr,
    ) -> None:
        self.name = name
        self.name_tran = name_tran
        self.type = type
        self.level = level
        self.color = color
        self.abilities = abilities
        self.progress_attr = progress_attr
        self.action_attr = action_attr
        self.frame_attr = frame_attr
        self.frame_attr = frame_attr
        self.atk_value = atk_value
        self.def_value = def_value
        self.stk_value = stk_value
        self.flavor_text = flavor_text
        self.flavor_text_tran = flavor_text_tran
        self.collection_attr = collection_attr

        text = ""

        for ability in self.abilities:
            if ability.type == AbilityType.Persistent:
                type_text = "[常]"
            elif ability.type == AbilityType.Automatic:
                type_text = "[自]"
            elif ability.type == AbilityType.Activated:
                type_text = "[起]"
            text += f"{type_text} {ability.effect}\n"

        if self.action_attr:
            text += self.action_attr.__text__()
        elif self.frame_attr:
            text += self.frame_attr.value
        elif self.progress_attr:
            text += self.progress_attr.__text__()

        self.text = text

    def __json__(self):
        return {
            "name": self.name,
            "name_tran": self.name_tran,
            "type": self.type.value,
            "level": self.level,
            "color": self.color.value if self.color else None,
            "text": self.text,
            "abilities": [ability.__json__() for ability in self.abilities],
            "progress_attr": self.progress_attr.__json__()
            if self.progress_attr
            else None,
            "action_attr": self.action_attr.__json__() if self.action_attr else None,
            "frame_attr": self.frame_attr.value if self.frame_attr else None,
            "atk": self.atk_value if self.atk_value else None,
            "def": self.def_value if self.def_value else None,
            "stk": self.stk_value if self.stk_value else None,
            "flavor_text": self.flavor_text if self.flavor_text else None,
            "flavor_text_tran": self.flavor_text_tran
            if self.flavor_text_tran
            else None,
            "collection_attr": self.collection_attr.__json__(),
        }
