from typing import Any, List
import heapq


class MinHeap:
    def __init__(self):
        self.__data: List[Any] = []

    def push(self, item: Any):
        heapq.heappush(self.__data, item)

    def pop(self):
        if len(self.__data) == 0:
            return None
        return heapq.heappop(self.__data)

    def peek(self):
        if len(self.__data) == 0:
            return None
        return self.__data[0]
