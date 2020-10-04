from telegram.utils.promise import Promise
from typing import Type, TypeVar, Union

TP = TypeVar("TP")


def resolve(promise: Union[Promise, TP], t: Type[TP]) -> TP:
    if isinstance(promise, t):
        return t
    if isinstance(promise, Promise):
        return promise.result()
    return promise
