import copy
import json

from model import Product, Ex
from model.action import ActionAttr
from model.card import Ability, Card
from model.collection import CollectionAttr
from model.constants import AbilityType, CardColor, CardType, FrameType
from model.progress import Link, ProgressAttr
from utils.json import get_member_from_enum, to_json


with open("./data.json", "r") as f:
    data = json.load(f)


sideab = data[0]
brilliant = data[1]

output = []
outP = Product(
    sideab["id"],
    sideab["name"],
    sideab["release_date"],
    sideab["main_expansion"],
)

for card in sideab["cards"]:
    outC = Card(
        card["name"],
        card["name_tran"],
        get_member_from_enum(CardType, card["type"]),
        card["level"],
        get_member_from_enum(CardColor, card["color"]) if card["color"] else None,
        [
            Ability(
                get_member_from_enum(AbilityType, ability["type"]),
                ability["effect"],
                ability["effect_tran"],
            )
            for ability in card["abilities"]
        ],
        ProgressAttr(
            card["progress_attr"]["character"],
            card["progress_attr"]["character_tran"],
            Link(
                card["progress_attr"]["link"]["cost"],
                (
                    card["progress_attr"]["link"]["omega"],
                    card["progress_attr"]["link"]["sigma"],
                    card["progress_attr"]["link"]["any"],
                ),
                card["progress_attr"]["link"]["effect"],
                card["progress_attr"]["link"]["effect_tran"],
            )
            if card["progress_attr"]["link"]
            else None,
            Ex(
                card["progress_attr"]["ex"]["name"],
                card["progress_attr"]["ex"]["effect"],
                card["progress_attr"]["ex"]["name_tran"],
                card["progress_attr"]["ex"]["effect_tran"],
            )
            if card["progress_attr"]["ex"]
            else None,
        )
        if card["progress_attr"]
        else None,
        ActionAttr(
            card["action_attr"]["condition"],
            card["action_attr"]["effect"],
            card["action_attr"]["condition_tran"],
            card["action_attr"]["effect_tran"],
        )
        if card["action_attr"]
        else None,
        get_member_from_enum(FrameType, card["frame_attr"])
        if card["frame_attr"]
        else None,
        card["atk"] if card["atk"] else None,
        card["def"] if card["def"] else None,
        card["stk"] if card["stk"] else None,
        card["flavor_text"] if card["flavor_text"] else None,
        card["flavor_text_tran"] if card["flavor_text_tran"] else None,
        CollectionAttr(
            card["collection_attr"]["series_id"],
            card["collection_attr"]["card_index"],
            card["collection_attr"]["effect_index"],
            card["collection_attr"]["product_id"],
            card["collection_attr"]["product_name"],
            card["collection_attr"]["foil"],
            card["collection_attr"]["alternate_art"],
            card["collection_attr"]["artist"],
            card["collection_attr"]["promo"],
        ),
    )
    outP.cards.append(outC)

output.append(outP)

outP = Product(
    brilliant["id"],
    brilliant["name"],
    brilliant["release_date"],
    brilliant["main_expansion"],
)


f = False
for card in brilliant["cards"]:
    card_index = card["collection_attr"]["card_index"]
    if card_index[-1] == "P":
        effect_index = card_index[:-1]
        alternate_art = True
    elif card_index[-1] == "F":
        effect_index = "Sigma" if f else "Omega"
        alternate_art = True
        f = True
    else:
        effect_index = card_index
        alternate_art = False

    for c in output[0].cards:
        if c.collection_attr.effect_index == card["collection_attr"]["effect_index"]:
            outC = copy.deepcopy(c) 
            outC.collection_attr = CollectionAttr(
                "1",
                card_index,
                effect_index,
                "brilliant",
                "アンジュ・ユナイト ブリリアントパック Vol.1",
                True,
                alternate_art,
                card["collection_attr"]["artist"]
                if card["collection_attr"]["artist"]
                else None,
                None,
            )
            outP.cards.append(outC)
            break
output.append(outP)
to_json(output, path="./test")
