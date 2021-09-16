from queue import Queue


class __EventQueue:
    def __init__(self) -> None:
        self.__eventQueue = Queue()

    def pushCallback(self, fn):
        self.__eventQueue.put(fn, block=True)

    def getCallback(self):
        return self.__eventQueue.get(block=True)


eventQueue = __EventQueue()
