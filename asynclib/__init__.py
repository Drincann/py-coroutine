from .eventloop import loop
from .eventQueue import eventQueue
from .Future import Future


def asyncRun(gen):
    eventQueue.pushCallback(gen)
