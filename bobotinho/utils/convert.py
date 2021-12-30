# -*- coding: utf-8 -*-
import json
import random
import re
from datetime import datetime
from emoji import demojize
from typing import Union, Optional
from unidecode import unidecode

from bobotinho.exceptions import InvalidUser


def datetime2str(target: datetime) -> str:
    return target.isoformat()


def dict2str(target: Optional[dict]) -> str:
    try:
        return json.dumps(target)
    except Exception:
        return ""


def emoji2str(target: str) -> Optional[str]:
    emoji = demojize(target)
    if emoji != target and emoji.count(":") == 2:
        return emoji


def txt2randomline(target: str) -> str:
    with open(target, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return random.choice(lines)


def number2str(target: Union[int, float]) -> Optional[str]:
    if isinstance(target, int):
        return f"{target:,d}".replace(",", ".")
    if isinstance(target, float):
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


def str2ascii(target: str) -> str:
    return unidecode(target).lower().strip()


def str2datetime(target: str) -> datetime:
    return datetime.fromisoformat(target)


def str2dict(target: Optional[str]) -> dict:
    try:
        return json.loads(target)
    except Exception:
        return {}


def str2float(target: Optional[str]) -> Optional[float]:
    try:
        return float(target.replace(",", "."))
    except Exception:
        return None


def str2int(target: Optional[str]) -> Optional[int]:
    try:
        return int(target)
    except Exception:
        return None


def str2hexcode(target: Optional[str]) -> Optional[str]:
    if not target:
        return None
    if match := re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", target):
        return match.group(0)


def str2name(target: str, default: Optional[str] = None) -> Optional[str]:
    if not target and default:
        return default
    if target:
        if target[0] == "@":
            target = target[1:]
        if target[-1] == ",":
            target = target[:-1]
        if target.replace("_", "").isalnum() and unidecode(target) == target:
            return target.lower()
    raise InvalidUser


def str2url(target: str) -> Optional[str]:
    return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", target)
