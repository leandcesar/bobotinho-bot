# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests


@dataclass
class Prediction:
    city: str
    country: str
    humidity: str
    status: str
    feels_like: str
    temp_max: str
    temp_min: str
    temp_now: str
    wind: str


@dataclass
class Weather:
    key: str
    url: str = "https://api.openweathermap.org/data"
    version: str = "2.5"

    async def predict(self, location: str) -> Prediction:
        url = f"{self.url}/{self.version}/weather"
        params = {"appid": self.key, "lang": "pt_br", "units": "metric", "q": location}
        observation = await aiorequests.get(url, params=params)
        return Prediction(
            city=observation["name"],
            country=observation["sys"]["country"],
            humidity=observation["main"]["humidity"],
            status=observation["weather"][0]["description"],
            feels_like=observation["main"]["feels_like"],
            temp_max=observation["main"]["temp_max"],
            temp_min=observation["main"]["temp_min"],
            temp_now=observation["main"]["temp"],
            wind=observation["wind"]["speed"],
        )
