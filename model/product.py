from typing import List
from .card import Card


class Product:
    id: str
    name: str
    release_date: str
    main_expansion: bool
    cards_num: int
    cards: List[Card]

    def __init__(
        self, id: str, name: str, release_date: str, main_expansion: bool
    ) -> None:
        self.id = id
        self.name = name
        self.release_date = release_date
        self.main_expansion = main_expansion
        self.cards = []

    def __json__(self) -> str:
        return {
            "id": self.id,
            "name": self.name,
            "release_date": self.release_date,
            "main_expansion": self.main_expansion,
            "cards_num": len(self.cards),
            "cards": [card.__json__() for card in self.cards],
        }
