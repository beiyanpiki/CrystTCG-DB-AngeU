from typing import Optional, Tuple
from .constants import FrameType


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
            "condition": [FrameType.Omega.value] * self.condition[0]
            + [FrameType.Sigma.value] * self.condition[1]
            + [FrameType.Any.value] * self.condition[2],
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


class ProgressAttr:
    character: str
    link: Optional[Link]
    ex: Optional[Ex]

    def __init__(
        self,
        character: str,
        link: Optional[Link],
        ex: Optional[Ex],
    ) -> None:
        self.character = character
        self.link = link
        self.ex = ex

    def __json__(self):
        return {
            "character": self.character,
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
