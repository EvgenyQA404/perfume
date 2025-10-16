import re
from typing import Optional

PRICE_RE = re.compile(r"[\d\s]+")


def parse_rub(price_text: str) -> Optional[int]:
    if not price_text:
        return None
    m = PRICE_RE.search(price_text)
    if not m:
        return None
    digits = m.group(0).replace(" ", "")
    try:
        return int(digits)
    except ValueError:
        return None