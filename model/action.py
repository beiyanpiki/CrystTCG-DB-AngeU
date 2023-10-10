class ActionAttr:
    condition: str
    effect: str

    def __init__(self, conditions: str, effect: str) -> None:
        self.condition = conditions
        self.effect = effect

    def __json__(self):
        return {"condition": self.condition, "effect": self.effect}

    def __text__(self) -> str:
        return f"[条件] {self.condition}\n{self.effect}"
