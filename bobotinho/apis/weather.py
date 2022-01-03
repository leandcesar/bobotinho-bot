# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Weather"


@dataclass
class Weather:
    key: str
    url: str = "https://api.openweathermap.org/data"
    version: str = "2.5"

    async def predict(self, location: str) -> dict:
        url = f"{self.url}/{self.version}/weather"
        params = {"appid": self.key, "lang": "pt_br", "units": "metric", "q": location}
        response = await aiorequests.get(url, params=params)
        observation = response.json()
        return {
            "city": observation["name"],
            "country": observation["sys"]["country"],
            "humidity": observation["main"]["humidity"],
            "status": observation["weather"][0]["description"],
            "temp_now": observation["main"]["temp"],
            "temp_min": observation["main"]["temp_min"],
            "temp_max": observation["main"]["temp_max"],
            "temp_feels_like": observation["main"]["feels_like"],
            "wind": observation["wind"]["speed"],
        }
