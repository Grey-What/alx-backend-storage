#!/usr/bin/env python3
"""contains a class with a constructor and method"""

import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """store the history of inputs and utputs for a function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """call the method after storing its input then storing its output"""
        input_list_key = "{}:inputs".format(method.__qualname__)
        output_list_key = "{}:outputs".format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_list_key, str(args))

        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_list_key, output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """count the amount method of Cache is called"""
    @wraps(method)
    def caller(self, *args, **kwargs) -> Any:
        """call the method after incrementing it's counter in redis storage"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return caller


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method."""

    if fn is None or not hasattr(fn, '__self__'):
        return

    redis_inst = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_inst, redis.Redis):
        return

    func_name = fn.__qualname__
    in_key = '{}:inputs'.format(func_name)
    out_key = '{}:outputs'.format(func_name)
    func_call_count = 0

    if redis_inst.exists(func_name) != 0:
        func_call_count = int(redis_inst.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))

    func_inputs = redis_inst.lrange(in_key, 0, -1)
    func_outputs = redis_inst.lrange(out_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(
            func_name,
            func_input.decode("utf-8"),
            func_output,
        ))


class Cache:
    """class that functions as a cache through its methods"""

    def __init__(self) -> None:
        """constructor of class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
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
