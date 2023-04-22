from typing import Any, Callable, List, TypeVar, Union
import inspect
from inspect import Parameter


class ReflectUtil:
    """
    This class provides some reflection utilities.
    """

    @staticmethod
    def getParameters(func: Callable) -> List[Parameter]:
        return list(inspect.signature(func).parameters.values())
