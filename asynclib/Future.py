from typing import Any, Callable, Sequence, List
from inspect import isgeneratorfunction, isgenerator, isfunction


class Future:
    callbacks: List[Callable[[Any], Any]] = []
    value: Any = None
    task: Callable[[Callable[[Any], Any]], Any]
    state: str = 'pending'

    def __init__(self, task=None):
        if isgeneratorfunction(task):
            self.task = task(self.resolve)
        elif isfunction(task):
            self.task = task
        else:
            self.task = lambda resolve: resolve()

    def resolve(self, value: Any = None):
        if self.state == 'resolved':
            return
        self.state = 'resolved'
        for cbk in self.callbacks:
            cbk(self)
        return self

    def addCallback(self, cbk: Callable[[Any], Any]):
        if self.state == 'resolved':
            cbk(self)
        self.callbacks.append(cbk)
        return self

    def __iter__(self):
        if(isfunction(self.task)):
            self.task(self.resolve)
        yield self
        return self.value
