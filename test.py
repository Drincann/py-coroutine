import time
import math
from asynclib.core import Promise, LoopManager, Timer
from asynclib.asynchttp import get as asyncget


@LoopManager.asyncfun
def httpReq():
    responseData = yield from Promise(
        lambda resolve:
            asyncget(
                url='http://codingfor.life/doc/README.md',
                callback=lambda response: resolve(response)
            ),
    ).catch(lambda e: print(e))
    return responseData


@ LoopManager.asyncfun
def asyncmain():
    # async call
    print('async call start', '\n')
    start = time.time()
    print('async res: ', (yield from Promise.all([httpReq() for _ in range(10)])), '\n')
    print('promise all cost: ' +
          str(math.floor((time.time() - start) * 1000)) + 'ms', '\n')

    # sleep a while using Timer
    print('sleep 2000ms using coroutine timer', '\n')
    yield from Timer.sleep(2000)

    # sync call
    print('sync call start', '\n')
    start = time.time()
    for _ in range(10):
        print(f'sync res {_}: ', (yield from httpReq()), '\n')
    print('sync cost: ' +
          str(math.floor((time.time() - start) * 1000)) + 'ms', '\n')


asyncmain()
