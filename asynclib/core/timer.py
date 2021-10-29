import time
from typing import Any, Callable

from asynclib.core.model import Promise
from .eventloop import LoopManager
from .eventQueue import EventQueueManager


class Timer:
    def __init__(self, timeout: float, callback: Callable, asyncDone: Callable) -> None:
        if not callable(callback):
            return
        self.timeout = timeout
        self.start = time.time()
        self.callback = callback
        self.asyncDone = asyncDone

    @staticmethod
    @LoopManager.asyncapi
    def setTimeout(timeout: float, callback: Callable, asyncDone: Callable) -> None:
        EventQueueManager \
            .getNextEventQueue().pushCallback(
                Timer(timeout / 1000, callback, asyncDone)
            )

    @staticmethod
    def sleep(ms) -> None:
        return Promise(lambda resolve: Timer.setTimeout(ms, resolve))

    def __call__(self) -> Any:
        if time.time() - self.start > self.timeout:
            EventQueueManager.getCurrentEventQueue().pushHeadCallback(self.callback)
            EventQueueManager.getCurrentEventQueue().pushHeadCallback(self.asyncDone)
        else:
            EventQueueManager.getNextEventQueue().pushCallback(self)
        pass

    def __repr__(self) -> str:
        return f"<Timer: {time.time() - self.start}s/{self.timeout}s>"


@LoopManager.asyncapi
def setTimeout(ms, callback, asyncDone):
    EventQueueManager.getEventQueue().pushCallback(
        Timer(ms / 1000, callback, asyncDone)
    )
