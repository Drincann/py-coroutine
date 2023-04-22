from typing import Any, Callable, List, TypeVar, Union


class Emitter:
    """
    Event emitter implementation.
    """

    def __init__(self) -> None:
        self.__eventMap: dict[str, list[Callable]] = {}

    def on(self, event: str, cbk: Callable):
        if event in self.__eventMap:
            self.__eventMap[event].append(cbk)
        else:
            self.__eventMap[event] = [cbk]
        return self

    def emit(self, event: str, *args, **kwds):
        if event in self.__eventMap:
            for cbk in self.__eventMap[event]:
                cbk(*args, **kwds)
        return self
