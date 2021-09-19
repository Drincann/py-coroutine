from asynclib.core import Promise, LoopManager
from asynclib.asynchttp import get as asyncget


@LoopManager.asyncfun
def httpReq():
    responseData = yield from Promise(
        lambda resolve:
            asyncget(
                url='http://gaolihai.cool/doc/README.md',
                callback=lambda response: resolve(response)
            )
    )

    return responseData.decode()


@LoopManager.asyncfun
def asyncmain():
    for i in range(10):
        print((yield from httpReq()))


asyncmain()
