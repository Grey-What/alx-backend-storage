#!/usr/bin/env python3
"""contains a class with a constructor and method"""

import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count the amount methods of Cache is called"""
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        """call the method after incrementing it's counter in redis storage"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return caller


class Cache:
    """class that functions as a cache through its methods"""

    def __init__(self) -> None:
        """constructor of class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        generate a random key and store input data in Redis
        using the random key

        Args:
            data: to be stored

        Return: key generated
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, float, int]:
        """retrieves a value from redis storage based on key"""
        data = self._redis.get(key)

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """retireves a string from mRedis storage"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda x: int(x))
