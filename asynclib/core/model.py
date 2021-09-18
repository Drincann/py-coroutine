from typing import Any, Callable, Sequence, List
from inspect import isgeneratorfunction, isfunction


class Future:

    def __init__(self, task=lambda resolve: resolve()):
        self.callbacks: List[Callable[[Any], Any]] = []
        self.value: Any = None
        self.state: str = 'pending'
        task(self.resolve)

    def resolve(self, value: Any = None):
        if self.state == 'resolved':
            return
        self.value = value
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
        yield self
        return self.value
