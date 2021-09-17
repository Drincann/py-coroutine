from queue import Queue


class __EventQueue:
    def __init__(self) -> None:
        self.__eventQueue = Queue()

    def clear(self):
        while self.__eventQueue.empty() is not True:
            self.__eventQueue.get()

    def pushCallback(self, fn):
        self.__eventQueue.put(fn, block=True)

    def getCallback(self):
        return self.__eventQueue.get(block=True)


eventQueue = __EventQueue()
