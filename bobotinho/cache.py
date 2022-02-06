# -*- coding: utf-8 -*-
import time
from collections import OrderedDict
from threading import RLock
from typing import Any


class TTLOrderedDict(OrderedDict):
    def __init__(self) -> None:
        self._lock = RLock()
        super().__init__()

    def _expired(self, key: str, now: float) -> bool:
        with self._lock:
            expire = super().__getitem__(key)[0]
            return expire and expire < now

    def _purge(self) -> None:
        now = time.time()
        for key in list(super().__iter__()):
            if self._expired(key, now):
                self.__delitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        with self._lock:
            expire = None
            super().__setitem__(key, (expire, value))

    def __delitem__(self, key: str) -> None:
        with self._lock:
            super().__delitem__(key)

    def __getitem__(self, key: str) -> Any:
        with self._lock:
            now = time.time()
            if self._expired(key, now):
                self.__delitem__(key)
                raise KeyError
            return super().__getitem__(key)[1]

    def keys(self, pattern: str = None) -> list:
        with self._lock:
            self._purge()
            return super().keys()

    def set(self, key: str, value: Any, ex: int = None, nx: bool = None) -> bool:
        if nx and self.get(key):
            return False
        with self._lock:
            self._purge()
            expire = time.time() + ex if ex else None
            super().__setitem__(key, (expire, value))
            return True

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def getset(self, key: str, value: Any) -> Any:
        current_value = self.get(key)
        self.set(key, value)
        return current_value

    def delete(self, key: str) -> None:
        self.__delitem__(key)

    def close(self) -> None:
        pass
