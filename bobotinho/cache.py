# -*- coding: utf-8 -*-
import time
from collections import OrderedDict
from threading import RLock


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
        [
            self.__delitem__(key)
            for key in [
                key for key in list(super().__iter__()) if self._expired(key, now)
            ]
        ]

    def __setitem__(self, key: str, value: str) -> None:
        with self._lock:
            expire = None
            super().__setitem__(key, (expire, value))

    def __delitem__(self, key: str) -> None:
        with self._lock:
            super().__delitem__(key)

    def __getitem__(self, key: str) -> str:
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
    def set(self, key: str, value: str, ex: int = None, nx: bool = None) -> bool:
        if nx and self.get(key):
            return False
        with self._lock:
            self._purge()
            expire = time.time() + ex if ex else None
            super().__setitem__(key, (expire, value))
            return True

    def get(self, key: str, default: str = None) -> str:
        try:
            return self[key]
        except KeyError:
            return default

    def getset(self, key: str, value: str) -> str:
        current_value = self.get(key)
        self.set(key, value)
        return current_value

    def delete(self, key: str) -> None:
        self.__delitem__(key)

    def close(self) -> None:
        pass
