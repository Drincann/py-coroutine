import time
from typing import Any, Callable

from asynclib.core.util import MinHeap
from asynclib.core.promise import Promise
from .eventloop import LoopManager
from .eventQueue import EventQueueManager

"""
MinHeap of Timer
"""


class TimerHeap:
    __single = None

    @classmethod
    def getInstance(cls) -> "TimerHeap":
        if TimerHeap.__single is None:
            TimerHeap.__single = TimerHeap()
        return TimerHeap.__single

    def __init__(self) -> None:
        self.__heap: MinHeap = MinHeap()

    def pushTimer(self, timer: "Timer") -> "TimerHeap":
        return self.__heap.push(timer)

    def popTimer(self) -> "Timer":
        return self.__heap.pop()

    def peekTimer(self) -> "Timer":
        return self.__heap.peek()


_timerHeap = TimerHeap.getInstance()

"""
Coroutine-level timer abstraction
"""


class Timer:
    def __init__(self, timeout: float, callback: Callable, asyncDone: Callable) -> None:
        if not callable(callback):
            return
        self.timeout = timeout
        self.start = time.time()
        self.end = self.start + timeout
        self.callback = callback
        self.asyncDone = asyncDone

    def __lt__(self, other: 'Timer') -> bool:
        return self.end < other.end

    @staticmethod
    @LoopManager.asyncapi
    def setTimeout(timeoutms: float, callback: Callable, asyncDone: Callable) -> None:
        _timerHeap.pushTimer(Timer(timeoutms / 1000, callback, asyncDone))

    @staticmethod
    def sleep(ms) -> None:
        return Promise(lambda resolve: Timer.setTimeout(ms, resolve))

    def isTimeout(self) -> bool:
        return time.time() >= self.end

    def getCallback(self):
        return lambda: (self.callback(), self.asyncDone())

    def __repr__(self) -> str:
        return f"<Timer: {time.time() - self.start}s/{self.timeout}s>"


@LoopManager.asyncapi
def setTimeout(timeoutms, callback, asyncDone):
    _timerHeap.pushTimer(Timer(timeoutms / 1000, callback, asyncDone))
