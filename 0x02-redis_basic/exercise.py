#!/usr/bin/env python3
"""contains a class with a constructor and method"""

import redis
from typing import Union
from uuid import uuid4


class Cache:
    """class that functions as a cache through its methods"""

    def __init__(self) -> None:
        """constructor of class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        generate a random key and store input data in Redis
        using the random key

        Args:
            data: to be stored

        Return: key generated
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)

        return random_key
