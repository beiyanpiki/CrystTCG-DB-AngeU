from typing import Optional, Tuple
from .constants import FrameType


class Link:
    cost: int
    # condition: [Omega, Sigma, Any]
    # example: "Omega, Sigma, Sigma, 2" -> (1, 2, 2)
    condition: Tuple[int, int, int]
    effect: str
    effect_tran:str

    def __init__(self, cost: int, condition: Tuple[int, int, int], effect: str,effect_tran:str) -> None:
        self.cost = cost
        self.condition = condition
        self.effect = effect
        self.effect_tran = effect_tran

    def __json__(self):
        return {
            "cost": self.cost,
            "condition": [FrameType.Omega.value] * self.condition[0]
            + [FrameType.Sigma.value] * self.condition[1]
            + [FrameType.Any.value] * self.condition[2],
            "effect": self.effect,
            "effect_tran": self.effect_tran,
        }


class Ex:
    name: str
    effect: str
    name_tran:str
    effect_tran: str

    def __init__(self, name: str, effect: str,name_tran:str,effect_tran:str) -> None:
        self.name = name
        self.effect = effect
        self.name_tran = name_tran
        self.effect_tran = effect_tran

    def __json__(self):
        return {"name": self.name, "effect": self.effect,"name_tran":self.name_tran,"effect_tran":self.effect_tran}


class ProgressAttr:
    character: str
    character_tran: str
    link: Optional[Link]
    ex: Optional[Ex]

    def __init__(
        self,
        character: str,
        character_tran: str,
        link: Optional[Link],
        ex: Optional[Ex],
    ) -> None:
        self.character = character
        self.character_tran = character_tran
        self.link = link
        self.ex = ex

    def __json__(self):
        return {
            "character": self.character,
            "character_tran": self.character_tran,
            "link": self.link.__json__() if self.link else None,
            "ex": self.ex.__json__() if self.ex else None,
        }

    def __text__(self) -> str:
        text = ""

        if self.ex:
            text += f"[EX] {self.ex.name} {self.ex.effect}\n"

        if self.link:
            condition = (
                ["Ω" for _ in range(self.link.condition[0])]
                + ["Σ" for _ in range(self.link.condition[1])]
                + [str(self.link.condition[2])]
            )

            text += f"[Link-{self.link.cost}] {condition} {self.link.effect}\n"
        return text
