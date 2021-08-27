import asyncio
from asynclib import asyncRun, loop, Future


class container:
    arr = list(range(10))

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        if self.i >= len(self.arr):
            raise StopIteration
        return self.arr[self.i]


obj = container()


def asyncIter(i):
    for ele in obj:
        yield from Future(lambda resolve: (print('协程挂起'), resolve(None)))
        print(f'协程 {i} ------- {ele}')
    return None


asyncRun(asyncIter(1))
print('同步')
asyncRun(asyncIter(2))
asyncRun(asyncIter(3))
asyncRun(asyncIter(4))

loop()
