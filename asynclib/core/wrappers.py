from inspect import isgenerator
from typing import Any, Callable, List
from .eventQueue import EventQueueManager
from .promise import Promise
from .util import Emitter, minheap


"""
The developer's coroutine will be wrapped by this class, 
and the 'done' event callback will be triggered by eventloop 
after execution is completed
"""


class Coroutine(Emitter):
    def __init__(self, coro) -> None:
        super().__init__()
        self.coro = coro


# async api 抽象层, 位于事件循环和 async api 之间
class AsyncapiWrapper(Emitter):
    def __init__(self, asyncapi) -> None:
        super().__init__()
        self.__asyncapi = asyncapi
        self.result = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.emit('start', self)
        EventQueueManager.getCurrentEventQueue().pushCallback(
            lambda:
            self.__asyncapi(
                *args,
                **kwds,
                # 从该层分发异步结果
                asyncDone=self.__done
            )
        )

    def __done(self, result=None):
        self.result = result
        self.emit('done', self)


"""
This is an executable coroutine abstraction layer for
developer, located between event loop and coroutine wrapping.
"""


class AsyncfunWrapper(Emitter):
    def __init__(self, asyncfun) -> None:
        super().__init__()
        self.__asyncfun = asyncfun
        self.result = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.emit('start', self)
        coro = Coroutine(self.__asyncfun(*args, **kwds))
        EventQueueManager.getCurrentEventQueue().pushCallback(coro)
        return Promise(
            lambda resolve, reject: (
                # 从事件循环层接收异步结果 resolve 给开发者用户
                coro.on('done', lambda result: resolve(result)),
                # 从该层分发异步结果
                coro.on('done', self.__done)
            )
        )

    def __done(self, result):
        self.result = result
        self.emit('done', self)
