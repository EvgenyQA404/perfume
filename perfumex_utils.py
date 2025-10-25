# perfumex_utils.py — утилиты: разбор цены/валюты, загрузка секретов, паузы

import re
from pathlib import Path
from typing import Tuple, Optional, Dict


def parse_price_and_currency(value_text: str, currency_text: str) -> Tuple[int, str]:
    """
    Преобразует '232' + ' USD' → (23200, 'USD') — цена в минимальных единицах (центы).
    Допускает разделители пробел/запятая/точка.
    """
    # value_text может быть "232", "1 234", "1,234.56" и т.д.
    vt = value_text.strip()
    # Заменим пробелы неразрывные и обычные на пусто
    vt = vt.replace('\u00a0', '').replace(' ', '')
    # Если есть запятая и точка — сведём к точке
    vt = vt.replace(',', '.')
    # Оставим цифры и одну точку
    m = re.match(r'^(\d+(\.\d{1,2})?)$', vt)
    if not m:
        # fallback: извлечь первые число/десятичные
        m2 = re.search(r'\d+(?:\.\d{1,2})?', vt)
        if not m2:
            raise ValueError(f'Не удалось разобрать числовую цену: {value_text!r}')
        vt = m2.group(0)

    amount_float = float(vt)
    price_minor = int(round(amount_float * 100))

    # Валюта: оставить только буквы (USD, RUB и т.п.)
    curr = (currency_text or '').strip().upper()
    curr = re.sub(r'[^A-Z]', '', curr) or 'USD'

    return price_minor, curr


def load_env_kv(env_path: Path) -> Dict[str, str]:
    """
    Читает файл формата:
        email=user@example.com
        password=Secret
    Пустые строки и строки с # игнорируются.
    """
    if not env_path.exists():
        raise FileNotFoundError(f'Файл с секретами не найден: {env_path}')
    result: Dict[str, str] = {}
    for line in env_path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if '=' not in s:
            continue
        k, v = s.split('=', 1)
        result[k.strip().lower()] = v.strip()
    return result
