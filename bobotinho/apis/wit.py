# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bobotinho.apis import aiorequests


@dataclass
class Datetime:
    start: int
    end: int
    body: str
    confidence: float
    value: str

    @property
    def timestamp(self) -> datetime:
        return datetime.fromisoformat(self.value)


@dataclass
class Prediction:
    text: str
    datetime: List[Datetime]

    def __post_init__(self) -> None:
        self.datetime = [Datetime(**dt) for dt in self.datetime]


@dataclass
class Wit:
    token: str
    url: str = "https://api.wit.ai"
    version: str = "20200513"

    async def detect(self, text: str) -> Prediction:
        url = f"{self.url}/message"
        params = {"q": text}
        headers = {
            "authorization": f"Bearer {self.token}",
            "accept": f"application/vnd.wit.{self.version}+json",
        }
        try:
            response = await aiorequests.get(url, headers=headers, params=params)
            return Prediction(
                text=response["text"],
                datetime=[
                    {
                        "start": entity["start"],
                        "end": entity["end"],
                        "body": entity["body"],
                        "confidence": entity["confidence"],
                        "value": entity["value"],
                    }
                    for entity in response["entities"]["wit$datetime:datetime"]
                ],
            )
        except Exception:
            return Prediction(text="", datetime=[])
