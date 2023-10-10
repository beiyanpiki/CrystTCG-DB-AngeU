from typing import Optional


class CollectionAttr:
    series_id: str
    card_index: str

    product_id: str
    product_name: str

    foil: bool
    alternate_art: bool

    artist: Optional[str]

    promo: Optional[str]

    def __init__(
        self,
        series_id: str,
        card_index: str,
        product_id: str,
        product_name: str,
        foil: bool,
        alternate_art: bool,
        artist: Optional[str],
        promo: Optional[str] = None,
    ) -> None:
        self.series_id = series_id
        self.card_index = card_index
        self.product_id = product_id
        self.product_name = product_name
        self.foil = foil
        self.alternate_art = alternate_art
        self.artist = artist
        self.promo = promo

    def __json__(self):
        return {
            "series_id": self.series_id,
            "card_index": self.card_index,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "foil": self.foil,
            "alternate_art": self.alternate_art,
            "artist": self.artist if self.artist else None,
            "promo": self.promo if self.promo else None,
        }
