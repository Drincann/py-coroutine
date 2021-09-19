from inspect import isgeneratorfunction
from enum import Enum, auto
import threading
from .eventQueue import eventQueue
from .model import Promise, AsyncapiWrapper, AsyncfunWrapper, Coroutine


class Loop:
    class LoopState(Enum):
        RUNNING = auto()
        STOPPED = auto()

    class __GeneratorExecutor:
        def __init__(self, coroutine: Coroutine):
            self.coroutine = coroutine
            self.__next(Promise())

        def __next(self, promise: Promise):
            nextPromise = None
            try:
                nextPromise = self.coroutine.coro.send(promise.value)
            except StopIteration as returnVal:
                self.coroutine.emit('done', returnVal.value)
                return
            nextPromise.done(self.__next)

    __single = None

    @classmethod
    def getInstance(cls):
        if cls.__single is None:
            cls.__single = Loop()
        return cls.__single

    def __init__(self) -> None:
        self.state:  Loop.LoopState = Loop.LoopState.STOPPED
        self.__stop = True

    def stop(self):
        if self.state == Loop.LoopState.STOPPED:
            return
        self.__stop = True
        self.state = Loop.LoopState.STOPPED

    def start(self):
        if self.state == Loop.LoopState.RUNNING:
            return
        self.__stop = False
        self.state = Loop.LoopState.RUNNING

        try:
            while True:
                cbk = eventQueue.getCallback()
                if isinstance(cbk, Coroutine):
                    self.__GeneratorExecutor(cbk)
                elif callable(cbk):
                    cbk()
                else:
                    raise TypeError(
                        'cbk is not callable, generator or generatable')
                if self.__stop:
                    return
        except KeyboardInterrupt:
            exit(0)


class LoopManager:
    asyncTaskCount = 0
    loopobj = Loop.getInstance()

    @classmethod
    def loop(cls):
        threading.Thread(target=Loop.getInstance().start).start()

    @classmethod
    def stopLoop(cls):
        cls.loopobj.stop()

    @classmethod
    def asyncStart(cls):
        cls.asyncTaskCount += 1
        if cls.asyncTaskCount == 1:
            cls.loop()

    @classmethod
    def asyncDone(cls):
        cls.asyncTaskCount -= 1
        if cls.asyncTaskCount == 0:
            cls.stopLoop()

    @classmethod
    def asyncapiStart(cls, asyncapiWrapped):
        cls.asyncStart()

    @classmethod
    def asyncapiDone(cls, asyncapiWrapped):
        cls.asyncDone()

    @classmethod
    def asyncfunStart(cls, asyncfunWrapped):
        cls.asyncStart()

    @classmethod
    def asyncfunDone(cls, asyncfunWrapped):
        cls.asyncDone()

    # async api 的装饰器，用于维护所有异步任务的状态，管理事件循环
    # 只需要额外接收一个关键字参数 asyncTaskDone 即可实现一个对接到事件循环中的 async api
    @classmethod
    def asyncapi(cls, fun):
        return AsyncapiWrapper(fun).on('start', cls.asyncapiStart).on('done', cls.asyncapiDone)

    @classmethod
    def asyncfun(cls, coro):
        if not isgeneratorfunction(coro):
            raise TypeError('coro is not a generator function')

        return AsyncfunWrapper(coro).on('start', cls.asyncfunStart).on('done', cls.asyncfunDone)
