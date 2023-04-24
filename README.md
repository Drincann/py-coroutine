# py-coro-impl

A stackless coroutine implementation in Python.

Contains coroutine-level timer, and a simple non-blocking socket implementation of the coroutine-level HTTP protocol interface.

## run example

```sh
python3 test.py
```

```python
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
```



## reference

- async socket api

  [aosabook a-web-crawler-with-asyncio-coroutines](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

- event loop

  [StackOverflow how-would-you-implement-a-basic-event-loop](https://stackoverflow.com/questions/658403/how-would-you-implement-a-basic-event-loop)

  [MDN Event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)

  [The Node.js Event Loop, Timers, and process.nextTick](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick)
- promise

  <https://www.promisejs.org/implementing/>

- async function in v8

  <https://v8.dev/blog/fast-async>

- book: Operating System: The Three Easy Pieces

  <http://pages.cs.wisc.edu/~remzi/OSTEP/>
