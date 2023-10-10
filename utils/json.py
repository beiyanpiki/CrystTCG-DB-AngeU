import json
from pathlib import Path
from typing import Any, List

from model import Product


def custom_encoder(obj):
    if hasattr(obj, "__json__"):
        return obj.__json__()
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def convert_to_json(obj, compress=False):
    return (
        json.dumps(obj, default=custom_encoder, indent=4, ensure_ascii=False)
        if not compress
        else json.dumps(obj, default=custom_encoder, separators=(",", ":"))
    )


def to_json(products: List[Product], path: str = "./output"):
    fp = Path(path)
    with open(fp.joinpath("products.json"), "w") as f:
        f.write(
            convert_to_json(
                products,
                compress=False,
            )
        )
    with open(fp.joinpath("products_min.json"), "w") as f:
        f.write(convert_to_json(products, compress=True))


def from_json(path: str) -> str:
    with open(path, "r") as f:
        raw_text = f.read()
        content = json.loads(raw_text)
        f.close()
    return content


def get_safe_value(x: Any, default_value: Any):
    if x:
        return x
    else:
        return default_value


def get_member_from_enum(type, value):
    if value in type.__members__:
        return type[value]
    return None
