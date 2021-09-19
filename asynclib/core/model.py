from typing import Any, Callable
from .eventQueue import eventQueue


class Emitter:
    def __init__(self) -> None:
        self.eventMap: dict[str, list[Callable]] = {}

    def on(self, event: str, cbk: Callable):
        if event in self.eventMap:
            self.eventMap[event].append(cbk)
        else:
            self.eventMap[event] = [cbk]
        return self

    def emit(self, event: str, *args, **kwds):
        if event in self.eventMap:
            for cbk in self.eventMap[event]:
                cbk(*args, **kwds)
        return self


class Future:

    def __init__(self, task=lambda resolve: resolve()):
        self.callbacks: List[Callable[[Any], Any]] = []
        self.value: Any = None
        self.state: str = 'pending'
        task(self.resolve)

    def resolve(self, value: Any = None):
        if self.state == 'resolved':
            return
        self.value = value
        self.state = 'resolved'
        for cbk in self.callbacks:
            cbk(self)
        return self

    def addCallback(self, cbk: Callable[[Any], Any]):
        if self.state == 'resolved':
            cbk(self)
        self.callbacks.append(cbk)
        return self

    def __iter__(self):
        yield self
        return self.value


# 底层接口, 用户开发者的协程将被该类包装, 执行结束后被执行器触发 done 事件回调
class Coroutine(Emitter):
    def __init__(self, coro) -> None:
        super().__init__()
        self.coro = coro


# async api 抽象层, 位于事件循环和 async api 之间
class AsyncapiWrapper(Emitter):
    def __init__(self, asyncapi) -> None:
        super().__init__()
        self.asyncapi = asyncapi
        self.result = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.emit('start', self)
        self.asyncapi(
            *args,
            **kwds,
            asyncDone=self.__done
        )

    def __done(self, result):
        self.result = result
        self.emit('done', self)


# 这是一个可执行的开发者用户的协程抽象层, 位于事件循环和协程包装(Coroutine)之间
class AsyncfunWrapper(Emitter):
    def __init__(self, asyncfun) -> None:
        super().__init__()
        self.asyncfun = asyncfun
        self.result = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.emit('start', self)
        coro = Coroutine(self.asyncfun(*args, **kwds))
        eventQueue.pushCallback(coro)
        return Future(
            lambda resolve:
            (coro.on('done', lambda result: resolve(result)),
             coro.on('done', self.__done))
        )

    def __done(self, result):
        self.result = result
        self.emit('done', self)
