from inspect import isgenerator
from typing import Any, Callable, List


class Emitter:
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


class Promise:
    def __init__(self, task=lambda resolve: resolve()):
        self.__callbacks: List[Callable[[Any], Any]] = []
        self.__value: Any = None
        self.__state: str = 'pending'
        self.__task = task(self.__resolve)
        pass

    def __resolve(self, value: Any = None):
        if self.__state == 'resolved':
            return
        self.__value = value
        self.__state = 'resolved'
        for cbk in self.__callbacks:
            cbk(self.__value)
        return self

    def done(self, cbk: Callable[[Any], Any]):
        if self.__state == 'resolved':
            cbk(self.__value)
        self.__callbacks.append(cbk)
        return self

    def __iter__(self):
        if isgenerator(self.__task):
            yield from self.__task
        yield self
        return self.__value

    @classmethod
    def all(cls, tasks: list):
        def waitAll(resolve):
            for idx in range(len(tasks)):
                if isinstance(tasks[idx], Promise):
                    tasks[idx] = yield from tasks[idx]
            resolve(tasks)
        return Promise(waitAll)


# 底层接口, 用户开发者的协程将被该类包装, 执行结束后被执行器触发 done 事件回调
class Coroutine(Emitter):
    def __init__(self, coro) -> None:
        super().__init__()
        self.coro = coro
