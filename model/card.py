from typing import Optional

from .collection import CollectionAttr
from .start import StartAttr
from .action import ActionAttr
from .progress import ProgressAttr
from .constants import CardColor, CardType, FrameType


class Card:
    name: str
    type: CardType
    level: int
    color: Optional[CardColor]
    # Will automatic generate
    text: str

    start_attr: Optional[StartAttr]
    progress_attr: Optional[ProgressAttr]
    action_attr: Optional[ActionAttr]
    frame_attr: Optional[FrameType]

    atk_value: Optional[int]
    def_value: Optional[int]
    stk_value: Optional[int]

    flavor_text: Optional[str]

    collection_attr: CollectionAttr

    def __init__(
        self,
        name: str,
        type: CardType,
        level: int,
        color: Optional[CardColor],
        start_attr: Optional[StartAttr],
        progress_attr: Optional[ProgressAttr],
        action_attr: Optional[ActionAttr],
        frame_attr: Optional[FrameType],
        atk_value: Optional[int],
        def_value: Optional[int],
        stk_value: Optional[int],
        flavor_text: Optional[str],
        collection_attr: CollectionAttr,
    ) -> None:
        self.name = name
        self.type = type
        self.level = level
        self.color = color
        self.start_attr = start_attr
        self.progress_attr = progress_attr
        self.action_attr = action_attr
        self.frame_attr = frame_attr
        self.frame_attr = frame_attr
        self.atk_value = atk_value
        self.def_value = def_value
        self.stk_value = stk_value
        self.flavor_text = flavor_text
        self.collection_attr = collection_attr

        if self.start_attr:
            self.text = self.start_attr.__text__()
        elif self.action_attr:
            self.text = self.action_attr.__text__()
        elif self.frame_attr:
            self.text = self.frame_attr.value
        elif self.progress_attr:
            self.text = self.progress_attr.__text__()

    def __json__(self):
        return {
            "name": self.name,
            "type": self.type.value,
            "level": self.level,
            "color": self.color.value if self.color else None,
            "text": self.text,
            "start_attr": self.start_attr.__json__() if self.start_attr else None,
            "progress_attr": self.progress_attr.__json__()
            if self.progress_attr
            else None,
            "action_attr": self.action_attr.__json__() if self.action_attr else None,
            "frame_attr": self.frame_attr.value if self.frame_attr else None,
            "atk": self.atk_value if self.atk_value else None,
            "def": self.def_value if self.def_value else None,
            "stk": self.stk_value if self.stk_value else None,
            "flavor_text": self.flavor_text if self.flavor_text else None,
            "collection_attr": self.collection_attr.__json__(),
        }
