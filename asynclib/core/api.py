from .eventQueue import eventQueue
from inspect import isgeneratorfunction


def asyncRun(gen):
    eventQueue.pushCallback(gen)


def asyncfun(coro):
    if not isgeneratorfunction(coro):
        raise TypeError('coro is not a generator function')

    return lambda: asyncRun(coro)
