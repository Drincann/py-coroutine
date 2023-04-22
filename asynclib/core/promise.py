from typing import Any, Callable, List
from .util import ReflectUtil


"""
very simple Promise implementation,

see https://www.promisejs.org/
"""


class Promise:
    def __init__(self, task=lambda resolve, reject: resolve()):
        self.__rejected: List[Callable[[Any], Any]] = []
        self.__fulfilled: List[Callable[[Any], Any]] = []
        self.__value: Any = None
        self.__state: str = 'pending'  # | 'fulfilled' | 'rejected'

        self.__wrapToWeaklyTypedFunction(task)(self.__resolve, self.__reject)

    def __wrapToWeaklyTypedFunction(self, cbk: Callable[[Any], Any]):

        def wrapper(*args, **kwds):
            params = ReflectUtil.getParameters(cbk)
            args = list(args)[:len(params)]
            kwds = {key: kwds[key] for key in kwds if key in params}
            return cbk(*args, **kwds)

        return wrapper

    def __appendToRejected(self, cbk: Callable[[Any], Any]):
        if self.__state == 'rejected':
            cbk(self.__value)
        else:
            self.__rejected.append(cbk)

    def __appendToFulfilled(self, cbk: Callable[[Any], Any]):
        if self.__state == 'fulfilled':
            cbk(self.__value)
        else:
            self.__fulfilled.append(cbk)

    def __fulfill(self, value: Any = None):
        self.__state = 'fulfilled'
        self.__value = value
        for cbk in self.__fulfilled:
            cbk(value)

    def __reject(self, value: Any = None):
        self.__state = 'rejected'
        self.__value = value
        for cbk in self.__rejected:
            cbk(value)

    def __resolve(self, value: Any = None):
        if isinstance(value, Promise):
            value.then(self.__resolve).catch(self.__reject)
        else:
            self.__fulfill(value)

    def then(self, onFullfilled: Callable[[Any], Any] = lambda value: value, onRejected: Callable[[Any], Any] = lambda value: value):
        def newResolver(resolve, reject):
            try:
                self.__appendToFulfilled(
                    lambda value: resolve(onFullfilled(value)))
                self.__appendToRejected(
                    lambda value: resolve(onRejected(value)))
            except Exception as e:
                reject(e)
        return Promise(newResolver)

    def catch(self, onRejected: Callable[[Any], Any] = lambda value: value):
        return self.then(lambda value: value, onRejected)

    def __iter__(self):
        yield self
        return self.__value

    @classmethod
    def all(cls, tasks: list):
        def promiseAllResolver(resolve, reject):
            pendingCount = len(tasks)
            results = [None] * pendingCount

            def resolveValueAndCheckIfDone(index, value):
                nonlocal pendingCount
                nonlocal results
                nonlocal resolve
                results[index] = value
                pendingCount -= 1
                if pendingCount == 0:
                    resolve(results)

            try:
                for i, task in enumerate(tasks):
                    if isinstance(task, Promise):
                        def closure(i, task):
                            task.then(
                                lambda value: resolveValueAndCheckIfDone(
                                    i, value)
                            ).catch(
                                lambda value: resolveValueAndCheckIfDone(
                                    i, value)
                            )
                        closure(i, task)
                    else:
                        resolveValueAndCheckIfDone(i, task)

            except Exception as e:
                reject(e)
        return Promise(promiseAllResolver)
