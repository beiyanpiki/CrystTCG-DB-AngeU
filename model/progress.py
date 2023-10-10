from typing import Optional, List, Tuple
from .constants import AbilityType, FrameType


class Link:
    cost: int
    # condition: [Omega, Sigma, Any]
    # example: "Omega, Sigma, Sigma, 2" -> (1, 2, 2)
    condition: Tuple[int, int, int]
    effect: str

    def __init__(self, cost: int, condition: Tuple[int, int, int], effect: str) -> None:
        self.cost = cost
        self.condition = condition
        self.effect = effect

    def __json__(self):
        return {
            "cost": self.cost,
            "condition": {
                FrameType.Omega.value: self.condition[0],
                FrameType.Sigma.value: self.condition[1],
                FrameType.Any.value: self.condition[2],
            },
            "effect": self.effect,
        }


class Ex:
    name: str
    effect: str

    def __init__(self, name: str, effect: str) -> None:
        self.name = name
        self.effect = effect

    def __json__(self):
        return {"name": self.name, "effect": self.effect}


class Ability:
    type: AbilityType
    effect: str

    def __init__(self, type: AbilityType, effect: str) -> None:
        self.type = type
        self.effect = effect

    def __json__(self):
        return {"type": self.type.value, "effect": self.effect}


class ProgressAttr:
    character: str
    abilities: List[Ability]
    link: Optional[Link]
    ex: Optional[Ex]

    def __init__(
        self,
        character: str,
        link: Optional[Link],
        ex: Optional[Ex],
        abilities: List[Ability],
    ) -> None:
        self.character = character
        self.link = link
        self.ex = ex
        self.abilities = abilities

    def __json__(self):
        return {
            "character": self.character,
            "abilities": [ability.__json__() for ability in self.abilities],
            "link": self.link.__json__() if self.link else None,
            "ex": self.ex.__json__() if self.ex else None,
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

        if self.ex:
            text += f"[EX] {self.ex.name} {self.ex.effect}\n"

        if self.link:
            condition = (
                ["Ω" for _ in range(self.link.condition[0])]
                + ["Σ" for _ in range(self.link.condition[1])]
                + [str(self.link.condition[2])]
            )

            text += f"[Link-{self.link.condition}] {condition} {self.link.effect}\n"
        return text
