from inspect import isgenerator, isgeneratorfunction
from .eventQueue import eventQueue
from .model import Future


class Loop:
    class __GeneratorExecutor:
        def __init__(self, coroutine):
            self.coroutine = coroutine
            self.__next(Future())

        def __next(self, future: Future):
            try:
                nextFuture = self.coroutine.send(future.value)
            except StopIteration:
                return
            nextFuture.addCallback(self.__next)

    __single = None

    @classmethod
    def getInstance(cls):
        if cls.__single is None:
            cls.__single = Loop()
        return cls.__single

    def __init__(self) -> None:
        self.__stop = True

    def stop(self):
        self.__stop = True

    def start(self):
        self.__stop = False

        try:
            while True:
                cbk = eventQueue.getCallback()
                if isgenerator(cbk):
                    self.__GeneratorExecutor(cbk)
                elif isgeneratorfunction(cbk):
                    self.__GeneratorExecutor(cbk())
                elif callable(cbk):
                    cbk()
                else:
                    raise TypeError(
                        'cbk is not callable, generator or generatable')
                if self.__stop is True:
                    eventQueue.clear()
                    return
        except KeyboardInterrupt:
            exit(0)


def loop():
    Loop.getInstance().start()
