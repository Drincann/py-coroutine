from queue import Queue


class __EventQueue:
    def __init__(self) -> None:
        self.__eventQueue = Queue()

    def clear(self):
        while self.__eventQueue.empty() is not True:
            self.__eventQueue.get()

    def isEmpty(self) -> bool:
        return self.__eventQueue.empty()

    def pushCallback(self, fn):
        self.__eventQueue.put(fn, block=True)

    def getCallback(self, *, block=True):
        try:
            return self.__eventQueue.get(block)
        except:
            return None


eventQueue = __EventQueue()
