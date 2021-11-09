from collections import deque
import threading


class _EventQueue:
    def __init__(self) -> None:
        self.__deque = deque()
        self.__rlock = threading.RLock()

    def clear(self):
        self.__rlock.acquire()
        self.__deque.clear()
        self.__rlock.release()

    def empty(self) -> bool:
        self.__rlock.acquire()
        empty = len(self.__deque) == 0
        self.__rlock.release()
        return empty

    def pushCallback(self, fn):
        self.__rlock.acquire()
        self.__deque.append(fn)
        self.__rlock.release()
        return self

    def getCallback(self):
        self.__rlock.acquire()
        try:
            return self.__deque.popleft()
        except:
            return None
        finally:
            self.__rlock.release()

    def pushHeadCallback(self, fn):
        self.__rlock.acquire()
        self.__deque.appendleft(fn)
        self.__rlock.release()
        return self

    def getTailCallback(self):
        self.__rlock.acquire()
        try:
            return self.__deque.pop()
        except:
            return None
        finally:
            self.__rlock.release()


class EventQueueManager:
    __eventQueueRLock = threading.RLock()
    __currentEventQueue = _EventQueue()

    @staticmethod
    def getCurrentEventQueue():
        EventQueueManager.__eventQueueRLock.acquire()
        try:
            return EventQueueManager.__currentEventQueue
        finally:
            EventQueueManager.__eventQueueRLock.release()
