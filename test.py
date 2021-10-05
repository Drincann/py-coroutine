import time
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
    start = time.time()
    yield from Promise.all([httpReq() for _ in range(10)])
    print(time.time() - start)

    start = time.time()
    for _ in range(10):
        yield from httpReq()
    print(time.time() - start)


asyncmain()
