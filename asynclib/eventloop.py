from inspect import isgenerator
from selectors import DefaultSelector
from .eventQueue import eventQueue
from .Future import Future


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


def loop():
    try:
        while True:
            cbk = eventQueue.getCallback()
            if isgenerator(cbk):
                __GeneratorExecutor(cbk)
            elif callable(cbk):
                cbk()
            else:
                raise TypeError('cbk is not callable or generatable')

    except KeyboardInterrupt:
        exit(0)
