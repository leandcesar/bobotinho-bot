# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator

__all__ = "Translator"


class Translator:
    @staticmethod
    def translate(text: str, source: str, target: str) -> str:
        return GoogleTranslator(source=source, target=target).translate(text)
