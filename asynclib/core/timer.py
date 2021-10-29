import time
from typing import Any, Callable
from .eventloop import AsyncapiWrapper, Loop, LoopManager
loop = Loop.getInstance()


class Timer:
    def __init__(self, timeout: float, callback: Callable, asyncDone: Callable) -> None:
        if not callable(callback):
            return
        self.timeout = timeout
        self.start = time.time()
        self.callback = callback
        self.asyncDone = asyncDone
        # self.init(self)

    @staticmethod
    @LoopManager.asyncapi
    def setTimeout(timeout: float, callback: Callable, asyncDone: Callable) -> None:
        loop.getEventQueue().pushCallback(Timer(timeout / 1000, callback, asyncDone))

    def __call__(self) -> Any:
        if time.time() - self.start > self.timeout:
            loop.getEventQueue().pushCallback(self.callback)
            loop.getEventQueue().pushCallback(self.asyncDone)
        else:
            loop.getEventQueue().pushCallback(self)
        pass

    def __repr__(self) -> str:
        return f"<Timer: {time.time() - self.start}s/{self.timeout}s>"


@LoopManager.asyncapi
def setTimeout(ms, callback, asyncDone):
    loop.getEventQueue().pushCallback(Timer(ms / 1000, callback, asyncDone))
