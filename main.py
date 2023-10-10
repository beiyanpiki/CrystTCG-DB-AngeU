from pathlib import Path
from typing import List
import requests
from model import (
    Product,
    Card,
    ActionAttr,
    AbilityType,
    CardColor,
    CardType,
    Ability,
    Ex,
    Link,
    ProgressAttr,
    StartAttr,
    FrameType,
    CollectionAttr,
)
from utils import from_json, get_safe_value, get_member_from_enum, to_json

imgBaseDir = "./output"
imgBaseURL = "https://ange-unite.com/_assets_/hjangeunite"
productsMetaPath = "./meta/product.json"
cardsRawPath = ["./meta/raw/1.json"]

productsMeta = from_json(productsMetaPath)


def save_product_image(product_id: str) -> bool:
    foil = productsMeta[product_id]["foil"]
    productUrl = productsMeta[product_id]["url"]
    for card_index in productsMeta[product_id]["cards_index"]:
        cardFilename = f"{card_index}_foil.png" if foil else f"{card_index}.png"

        image_url = f"{imgBaseURL}/{productUrl}/{cardFilename}"
        image_dir = Path(imgBaseDir).joinpath(product_id)
        image_path = image_dir.joinpath(cardFilename)

        if image_path.exists():
            continue
        else:
            image_dir.mkdir(parents=True, exist_ok=True)

        try:
            response = requests.get(image_url)
            response.raise_for_status()
            f = open(image_path, "wb")
            f.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"{product_id}/{card_index} image is unavailable. {e}")
            return False
        except Exception as e:
            print(f"Error ocured. {e}")
            return False
    return True


if __name__ == "__main__":
    products = ["sideab", "brilliant"]

    output: List[Product] = []

    for product_id in products:
        product = productsMeta[product_id]

        product_name = product["name"]
        product_release_date = product["release_date"]
        product_main_expansion = product["main_expansion"]
        product_series_id = product["series_id"]
        product_cards_index = product["cards_index"]
        product_foil = product["foil"]

        product_cards_meta = from_json(f"./meta/raw/{product_series_id}.json")["cards"]

        save_product_image(product_id)

        outP = Product(
            product_id,
            product_name,
            product_release_date,
            product_main_expansion,
        )

        flag = True
        for i, card_index in enumerate(product_cards_index):
            if card_index in ["omega", "sigma"]:
                card_no = card_index
            else:
                card_no = card_index.split("-")[1]
                if card_no[-1] == "P":
                    card_alternate_art = True
                    card_no = card_no[:-1]
                elif card_no[-1] == "F":
                    card_alternate_art = True
                    card_no = "omega" if flag else "sigma"
                    flag = not flag
                else:
                    card_alternate_art = False
            idx = -1
            for j, match in enumerate(product_cards_meta):
                if match["collection_attr"]["card_index"] == card_no:
                    idx = j
                    break
            if idx == -1:
                print("Error")
                exit(1)
            card_meta = product_cards_meta[idx]

            # print(card_meta, "\n\n")

            card_name = card_meta["name"]
            card_type = get_member_from_enum(
                CardType, get_safe_value(card_meta["type"], "")
            )
            card_level = card_meta["level"]
            card_color = get_member_from_enum(
                CardColor, get_safe_value(card_meta["color"], "")
            )
            card_start_attr, card_progress_attr, card_action_attr, card_frame_attr = (
                None,
                None,
                None,
                None,
            )
            if card_type == CardType.Start:
                card_start_attr = StartAttr(
                    get_member_from_enum(
                        FrameType, card_meta["start_attr"]["frame_attr"]
                    ),
                )
            elif card_type == CardType.Progress:
                card_progress_attr = ProgressAttr(
                    card_meta["progress_attr"]["character"],
                    Link(
                        card_meta["progress_attr"]["link"]["cost"],
                        (
                            card_meta["progress_attr"]["link"]["condition"]["Omega"],
                            card_meta["progress_attr"]["link"]["condition"]["Sigma"],
                            card_meta["progress_attr"]["link"]["condition"]["Any"],
                        ),
                        card_meta["progress_attr"]["link"]["effect"],
                    )
                    if card_meta["progress_attr"]["link"]
                    else None,
                    Ex(
                        card_meta["progress_attr"]["ex"]["name"],
                        card_meta["progress_attr"]["ex"]["effect"],
                    )
                    if card_meta["progress_attr"]["ex"]
                    else None,
                )
            elif card_type == CardType.Action:
                card_action_attr = ActionAttr(
                    card_meta["action_attr"]["condition"],
                    card_meta["action_attr"]["effect"],
                )
            elif card_type == CardType.Frame:
                card_frame_attr = get_member_from_enum(
                    FrameType, card_meta["frame_attr"]
                )

            if card_type == CardType.Start:
                card_abilities = [
                    Ability(
                        get_member_from_enum(
                            AbilityType, get_safe_value(ability["type"], "")
                        ),
                        ability["effect"],
                    )
                    for ability in card_meta["start_attr"]["abilities"]
                ]
            elif card_type == CardType.Progress:
                card_abilities = [
                    Ability(
                        get_member_from_enum(
                            AbilityType, get_safe_value(ability["type"], "")
                        ),
                        ability["effect"],
                    )
                    for ability in card_meta["progress_attr"]["abilities"]
                ]

            else:
                card_abilities = []

            card_atk = card_meta["atk"] if card_meta["atk"] else None
            card_def = card_meta["def"] if card_meta["def"] else None
            card_stk = card_meta["stk"] if card_meta["stk"] else None
            card_flavor_text = (
                card_meta["flavor_text"] if card_meta["flavor_text"] else None
            )

            card_collection_attr = CollectionAttr(
                product_series_id,
                card_index,
                card_no,
                product_id,
                product_name,
                product_foil,
                card_meta["collection_attr"]["alternate_art"]
                if card_meta["collection_attr"]["alternate_art"]
                else False,
                card_meta["collection_attr"]["artist"]
                if card_meta["collection_attr"]["artist"]
                else None,
                card_meta["collection_attr"]["promo"]
                if card_meta["collection_attr"]["promo"]
                else None,
            )
            outC = Card(
                card_name,
                card_type,
                card_level,
                card_color,
                card_abilities,
                card_start_attr,
                card_progress_attr,
                card_action_attr,
                card_frame_attr,
                card_atk,
                card_def,
                card_stk,
                card_flavor_text,
                card_collection_attr,
            )
            outP.cards.append(outC)
        output.append(outP)

    to_json(
        output,
    )
