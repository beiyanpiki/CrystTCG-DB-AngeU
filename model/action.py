class ActionAttr:
    condition: str
    effect: str

    condition_tran: str
    effect_tran: str

    def __init__(self, conditions: str, effect: str, condition_tran:str,effect_tran:str) -> None:
        self.condition = conditions
        self.effect = effect
        self.condition_tran = condition_tran
        self.effect_tran = effect_tran

    def __json__(self):
        return {"condition": self.condition, "effect": self.effect, "condition_tran": self.condition_tran,
                "effect_tran": self.effect_tran}

    def __text__(self) -> str:
        return f"[条件] {self.condition}\n{self.effect}"
