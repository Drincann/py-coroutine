from asynclib.core import Future, LoopManager
from asynclib.asynchttp import get as asyncget


@LoopManager.asyncfun
def http():
    responseData = yield from Future(
        lambda resolve:
            asyncget(
                url='http://gaolihai.cool/doc/README.md',
                callback=lambda response: resolve(response)
            )
    )

    return responseData.decode()


for i in range(10):
    http().addCallback(lambda future: print(future.value))
